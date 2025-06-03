from users.repositories.cv_doctor import DoctorRepository
from dotenv import load_dotenv
from fastapi import File, UploadFile
from core.exceptions.exceptions import UnSupportedFormat, FailedToSaveFile
import os


class UploadCVUseCase:
    def __init__(self, repo: DoctorRepository):
        self.repo = repo

    async def execute(self, doctor_id: int, file: UploadFile = File(...)):
        load_dotenv()
        if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise UnSupportedFormat()
        UPLOAD_DIR = os.getenv("CV_UPLOAD_DIR")
        ext = file.filename.split(".")[-1] #type: ignore
        unique_filename = f"{doctor_id}_CV.{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename) # type: ignore
        try:
            with open(file_path, "wb") as buffer:
                while chunk := await file.read(1024):
                    buffer.write(chunk)
        except Exception:
            raise FailedToSaveFile()
        self.repo.upload_cv(doctor_id, unique_filename)
