from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class PerformanceStatsSchema(BaseModel):
    total_students: int
    excellent: int
    good: int
    satisfactory: int
    unsatisfactory: int
    quality_percentage: float
    success_rate_percentage: float

class StudentCardSchema(BaseModel):
    student: Dict[str, Any]
    study_group: Optional[str]
    grades_by_semester: Dict[str, List[Dict[str, Any]]]
    credits_by_semester: Dict[str, List[Dict[str, Any]]]
    exams_by_semester: Dict[str, List[Dict[str, Any]]]
