from pydantic import BaseModel

class ReviewFinding(BaseModel):
    file: str
    issue_type: str
    severity: str
    confidence: float
    reason: str
    suggested_fix: str
    line_start: int
    line_end: int