from typing import Protocol

class DoctorRepository(Protocol):
    def upload_cv(self, doctor_id: int, cv_path: str) -> None:
        pass
