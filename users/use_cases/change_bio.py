from users.repositories.change_bio_repository import ChangeBioRepository
from core.exceptions.exceptions import UnAuthorizedAccess 

class ChangeBio:
    def __init__(self, repo: ChangeBioRepository):
        self.repo = repo
    
    def execute(self, bio: str, user_id: int):
        user_entity = self.repo.get_by_email(user_id)
        if not user_entity.role.casefold() == 'doctor':
            raise UnAuthorizedAccess()
        self.repo.update(bio, user_id)