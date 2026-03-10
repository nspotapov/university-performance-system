from fastapi import APIRouter

from .auth.router import router as auth
from .users.router import router as users
from .faculties.router import router as faculties
from .departments.router import router as departments
from .study_directions.router import router as study_directions
from .disciplines.router import router as disciplines
from .curricula.router import router as curricula
from .courses.router import router as courses
from .semesters.router import router as semesters
from .study_groups.router import router as study_groups
from .students.router import router as students
from .teachers.router import router as teachers
from .gradebooks.router import router as gradebooks
from .grades.router import router as grades
from .credits.router import router as credits
from .exams.router import router as exams
from .analytics.router import router as analytics

router = APIRouter(prefix="/v1")

routers = (
    auth,
    users,
    faculties,
    departments,
    study_directions,
    disciplines,
    curricula,
    courses,
    semesters,
    study_groups,
    students,
    teachers,
    gradebooks,
    grades,
    credits,
    exams,
    analytics,
)

for item in routers:
    router.include_router(item)

__all__ = ("router",)
