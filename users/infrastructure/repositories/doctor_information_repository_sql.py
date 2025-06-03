from users.repositories.doctor_information_repository import DoctorInformationRepository, DoctorsRepository
from sqlalchemy.orm import Session
from utils.models import Role_doctor, User
from users.entities.user_entites import UserEntity, DoctorEntity
import redis
import json
from core.exceptions.exceptions import UserNotFound

class DoctorInformationRepositorySQL(DoctorInformationRepository):
    def __init__(self, session: Session):
        self.session = session
        self.redis_server = redis.Redis(host="localhost", port=6379, db=0)

    def get_by_email(self, doctor_id):
        db_model = self.session.query(User).filter_by(user_id=doctor_id).first()
        return UserEntity(
            user_id = db_model.user_id, #type: ignore
            role = db_model.role #type: ignore
        )
        
    def get_acceptation_result(self, doctor_id):
        cache_key = f"doctorID:{doctor_id}"
        cached_data = self.redis_server.get(cache_key)
        if cached_data:
            data_body = dict(json.loads(cached_data)) # type: ignore
            return bool(data_body["accepted"]) #type: ignore
        db_model = self.session.query(Role_doctor).filter_by(doctor_id=doctor_id).first()
        data_body = {"bio": db_model.bio, "rating_avg": db_model.rating_avg, # type: ignore
                      "accepted": db_model.accepted, "review": db_model.number_of_review, "rating sum": db_model.rating_sum} # type: ignore
        self.redis_server.set(cache_key, json.dumps(data_body), ex=300) #type: ignore
        return bool(db_model.accepted) #type: ignore
    
    def get_doctor_bio(self, doctor_id):
        cache_key = f"doctorID:{doctor_id}"
        cached_data = self.redis_server.get(cache_key)
        if cached_data:
            data_body = dict(json.loads(cached_data)) # type: ignore
            return str(data_body["bio"])
        db_model = self.session.query(Role_doctor).filter_by(doctor_id=doctor_id).first()
        data_body = {"bio": db_model.bio, "rating_avg": db_model.rating_avg, # type: ignore
                      "accepted": db_model.accepted, "review": db_model.number_of_review, "rating sum": db_model.rating_sum} # type: ignore
        self.redis_server.set(cache_key, json.dumps(data_body), ex=300) #type: ignore
        return str(db_model.bio) #type: ignore
    
    def rate_doctor(self, doctor_id, rate):
        cache_key = f"doctorID:{doctor_id}"
        cached_data = self.redis_server.get(cache_key)
        if cached_data:
            data_body = dict(json.loads(cached_data)) # type: ignore
            review = int(data_body["review"]) + 1
            rating_sum = int(data_body["rating sum"]) + rate
            doctor_rating = rating_sum / review
            data_body["review"], data_body["rating sum"], data_body["rating_avg"] = review, rating_sum, doctor_rating
            self.redis_server.set(cache_key, json.dumps(data_body), ex=300)
            #TODO query the database update request
            return
        db_model = self.session.query(Role_doctor).filter(Role_doctor.doctor_id == doctor_id).first()
        if db_model is None:
            raise UserNotFound()
        review = db_model.number_of_review + 1 # type: ignore
        rating_sum = db_model.rating_sum + rate # type: ignore
        doctor_rating = rating_sum / review
        db_model.number_of_review, db_model.rating_sum, db_model.rating_avg = review, rating_sum, doctor_rating # type: ignore
        self.session.commit()
        self.session.refresh(db_model)
        data_body = {"bio": db_model.bio, "rating_avg": db_model.rating_avg, # type: ignore
                      "accepted": db_model.accepted, "review": db_model.number_of_review, "rating sum": db_model.rating_sum} # type: ignore
        self.redis_server.set(cache_key, json.dumps(data_body), ex=300)

class DoctorsRepositorySQL(DoctorsRepository):
    def __init__(self, session: Session):
        self.redis_server = redis.Redis(host="localhost", port=6379, db=0)
        self.session = session

    def get_top_rated_doctors(self, limit:int = 5):
        db_model = self.session.query(Role_doctor).order_by(Role_doctor.rating_avg.desc()).limit(limit).all()
        top_doctors = []
        for doctor in db_model:
            top_doctors.append(DoctorEntity(
                doctor.doctor_id, #type: ignore
                doctor.bio, #type: ignore
                doctor.rating_avg #type: ignore
            ))
        return top_doctors