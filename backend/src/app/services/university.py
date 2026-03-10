from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import Page
from app.models import (
    Faculty,
    Department,
    StudyDirection,
    Discipline,
    Curriculum,
    Course,
    Semester,
    StudyGroup,
)
from app.repositories import (
    FacultyRepository,
    DepartmentRepository,
    StudyDirectionRepository,
    DisciplineRepository,
    CurriculumRepository,
    CourseRepository,
    SemesterRepository,
    StudyGroupRepository,
)


class FacultyService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = FacultyRepository(db_session)

    async def get_faculty(self, faculty_id: int) -> Optional[Faculty]:
        return await self.__repository.read(faculty_id)

    async def get_faculties(self, size: int = 50, page: int = 1) -> Page[Faculty]:
        items, total = await self.__repository.find_all(size=size, page=page)
        return Page[Faculty](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_faculty(self, data: dict) -> Faculty:
        return await self.__repository.create(data)

    async def update_faculty(self, faculty_id: int, data: dict) -> Optional[Faculty]:
        return await self.__repository.update(faculty_id, data)

    async def delete_faculty(self, faculty_id: int) -> Optional[Faculty]:
        return await self.__repository.delete(faculty_id)


class DepartmentService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = DepartmentRepository(db_session)

    async def get_department(self, department_id: int) -> Optional[Department]:
        return await self.__repository.read(department_id)

    async def get_departments(
        self,
        size: int = 50,
        page: int = 1,
        faculty_id: Optional[int] = None
    ) -> Page[Department]:
        items, total = await self.__repository.find_all(size=size, page=page, faculty_id=faculty_id)
        return Page[Department](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_department(self, data: dict) -> Department:
        return await self.__repository.create(data)

    async def update_department(self, department_id: int, data: dict) -> Optional[Department]:
        return await self.__repository.update(department_id, data)

    async def delete_department(self, department_id: int) -> Optional[Department]:
        return await self.__repository.delete(department_id)


class StudyDirectionService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = StudyDirectionRepository(db_session)

    async def get_study_direction(self, direction_id: int) -> Optional[StudyDirection]:
        return await self.__repository.read(direction_id)

    async def get_study_directions(
        self,
        size: int = 50,
        page: int = 1,
        faculty_id: Optional[int] = None
    ) -> Page[StudyDirection]:
        items, total = await self.__repository.find_all(size=size, page=page, faculty_id=faculty_id)
        return Page[StudyDirection](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_study_direction(self, data: dict) -> StudyDirection:
        return await self.__repository.create(data)

    async def update_study_direction(self, direction_id: int, data: dict) -> Optional[StudyDirection]:
        return await self.__repository.update(direction_id, data)

    async def delete_study_direction(self, direction_id: int) -> Optional[StudyDirection]:
        return await self.__repository.delete(direction_id)


class DisciplineService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = DisciplineRepository(db_session)

    async def get_discipline(self, discipline_id: int) -> Optional[Discipline]:
        return await self.__repository.read(discipline_id)

    async def get_disciplines(
        self,
        size: int = 50,
        page: int = 1,
        study_direction_id: Optional[int] = None,
        department_id: Optional[int] = None
    ) -> Page[Discipline]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            study_direction_id=study_direction_id,
            department_id=department_id
        )
        return Page[Discipline](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_discipline(self, data: dict) -> Discipline:
        return await self.__repository.create(data)

    async def update_discipline(self, discipline_id: int, data: dict) -> Optional[Discipline]:
        return await self.__repository.update(discipline_id, data)

    async def delete_discipline(self, discipline_id: int) -> Optional[Discipline]:
        return await self.__repository.delete(discipline_id)


class CurriculumService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = CurriculumRepository(db_session)

    async def get_curriculum(self, curriculum_id: int) -> Optional[Curriculum]:
        return await self.__repository.read(curriculum_id)

    async def get_curricula(
        self,
        size: int = 50,
        page: int = 1,
        study_direction_id: Optional[int] = None
    ) -> Page[Curriculum]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            study_direction_id=study_direction_id
        )
        return Page[Curriculum](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_curriculum(self, data: dict) -> Curriculum:
        return await self.__repository.create(data)

    async def update_curriculum(self, curriculum_id: int, data: dict) -> Optional[Curriculum]:
        return await self.__repository.update(curriculum_id, data)

    async def delete_curriculum(self, curriculum_id: int) -> Optional[Curriculum]:
        return await self.__repository.delete(curriculum_id)


class CourseService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = CourseRepository(db_session)

    async def get_course(self, course_id: int) -> Optional[Course]:
        return await self.__repository.read(course_id)

    async def get_courses(self, size: int = 50, page: int = 1) -> Page[Course]:
        items, total = await self.__repository.find_all(size=size, page=page)
        return Page[Course](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_course(self, data: dict) -> Course:
        return await self.__repository.create(data)

    async def update_course(self, course_id: int, data: dict) -> Optional[Course]:
        return await self.__repository.update(course_id, data)

    async def delete_course(self, course_id: int) -> Optional[Course]:
        return await self.__repository.delete(course_id)


class SemesterService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = SemesterRepository(db_session)

    async def get_semester(self, semester_id: int) -> Optional[Semester]:
        return await self.__repository.read(semester_id)

    async def get_semesters(
        self,
        size: int = 50,
        page: int = 1,
        course_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> Page[Semester]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            course_id=course_id,
            is_active=is_active
        )
        return Page[Semester](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_semester(self, data: dict) -> Semester:
        return await self.__repository.create(data)

    async def update_semester(self, semester_id: int, data: dict) -> Optional[Semester]:
        return await self.__repository.update(semester_id, data)

    async def delete_semester(self, semester_id: int) -> Optional[Semester]:
        return await self.__repository.delete(semester_id)

    async def get_active_semester(self) -> Optional[Semester]:
        return await self.__repository.find_one(is_active=True)


class StudyGroupService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = StudyGroupRepository(db_session)

    async def get_study_group(self, group_id: int) -> Optional[StudyGroup]:
        return await self.__repository.read(group_id)

    async def get_study_groups(
        self,
        size: int = 50,
        page: int = 1,
        study_direction_id: Optional[int] = None,
        course_id: Optional[int] = None
    ) -> Page[StudyGroup]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            study_direction_id=study_direction_id,
            course_id=course_id
        )
        return Page[StudyGroup](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_study_group(self, data: dict) -> StudyGroup:
        return await self.__repository.create(data)

    async def update_study_group(self, group_id: int, data: dict) -> Optional[StudyGroup]:
        return await self.__repository.update(group_id, data)

    async def delete_study_group(self, group_id: int) -> Optional[StudyGroup]:
        return await self.__repository.delete(group_id)
