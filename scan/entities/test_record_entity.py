from datetime import datetime

class TestRecordEntity:
    def __init__(self, user_id: int, test_result: str, img_name: str, test_ratio: float):
        self.user_id = user_id
        self.test_result = test_result
        self.img_name = img_name
        self.test_ratio = test_ratio