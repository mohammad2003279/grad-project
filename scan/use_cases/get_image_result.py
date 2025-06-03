from scan.repositories.scan_image_repository import ScanImageRepository
from fastapi import UploadFile, File
import httpx
from core.exceptions.exceptions import UnSupportedFormat, AppException, ImageNotSupported
import os
from dotenv import load_dotenv
from scan.entities.test_record_entity import TestRecordEntity
from uuid import uuid4

class GetImageResult:
    def __init__(self, repo: ScanImageRepository):
        self.repo = repo

    async def execute(self, user_id: int, file: UploadFile = File(...)):
        if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise UnSupportedFormat()
        load_dotenv()
        path = os.getenv("UPLOAD_DIR")
        path = os.getenv("UPLOAD_SAMPLES_DIR")
        ext = file.filename.split(".")[-1] #type: ignore
        unique_filename = f"{uuid4()}.{ext}"
        file_path = os.path.join(path, unique_filename) #type: ignore
        '''
        1-save the image into the system
        2-send the path to the AI server and get the result
        3-if the result is not dermo, raise Exception type image is not accepted
        4-if image is dermo response = requests.get(f"http://localhost:8001/predict/{img_id}/{extension}")
        5-save the record into the database
        6-update the name according to the test result
        '''
        try:
            with open(file_path, "wb") as buffer:
                while chunk := await file.read(1024):
                    buffer.write(chunk)
        except Exception:
            raise AppException()
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8008/get-scan-result/{file.filename}")
        if response.status_code == 200:
            result_info = response.json()
            if result_info["response"] == "not dermo":
                raise ImageNotSupported()
            test_record_entity = TestRecordEntity(
                user_id=user_id,
                test_result=result_info["response"],
                img_name=unique_filename,
                test_ratio = result_info["ratio"]
            )
            
            self.repo.add(test_record_entity)
            #self.repo.update(user_id)
            return result_info
        else:
            raise AppException()