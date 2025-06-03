from enum import Enum

class ReportType(Enum):
    abuse = "abuse"
    terms_violation = "terms_violation"
    spam = "spam"
    application_error = "application error"
    other = "other"


class StatusType(Enum):
    pending = "pending"
    reviewed = "in progress"
    resolved = "resolved"