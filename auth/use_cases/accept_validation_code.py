from auth.repositories.verification_request_accepted import VerificationRequestAccepted

class AcceptCode:
    def __init__(self, repo: VerificationRequestAccepted):
        self.repo = repo

    def execute(self, email: str):
        self.repo.add(email)