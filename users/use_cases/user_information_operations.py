from uuid import uuid4
from users.repositories.user_information_repository import UserInformationRepository
from fastapi import UploadFile, File
from core.exceptions.exceptions import UnSupportedFormat, AppException, EntityNotFound, UserNotFound
import os
from dotenv import load_dotenv

class PostUserPicture:
    def __init__(self, repo: UserInformationRepository):
        self.repo = repo
        
    async def execute(self, user_id: int, file: UploadFile = File(...)):
        if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise UnSupportedFormat()
        load_dotenv()
        path = os.getenv("UPLOAD_DIR")
        old_profile_picture = self.repo.get_profile_pic(user_id)
        if old_profile_picture is not None:
            file_path = os.path.join(path, old_profile_picture) #type: ignore
            os.remove(file_path)
        
        ext = file.filename.split(".")[-1] #type: ignore
        unique_filename = f"{uuid4()}.{ext}"
        file_path = os.path.join(path, unique_filename) #type: ignore

        try:
            with open(file_path, "wb") as buffer:
                while chunk := await file.read(1024):
                    buffer.write(chunk)
        except AppException:
            raise AppException()
        self.repo.add(user_id, unique_filename)
        
class GetUserPicture:
    def __init__(self, repo: UserInformationRepository):
        self.repo = repo
        
    def execute(self, user_id: int) -> str:
        load_dotenv()
        try:
            path = os.getenv("UPLOAD_DIR")
            image_name = self.repo.get_profile_pic(user_id)
            if image_name is None:
                raise AppException()
            image_path = os.path.join(path, image_name) #type: ignore
            return image_path
        except AppException:
            raise EntityNotFound()
        


class GetBasicInformation:
    def __init__(self, repo: UserInformationRepository):
        self.repo = repo

    def execute(self, user_id: int):
        user_info = self.repo.get_basic_info(user_id)
        if user_info is None:
            raise UserNotFound()
        return user_info