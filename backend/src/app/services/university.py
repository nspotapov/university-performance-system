from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import Page
from app.api.v1.university.schemas import (
    FacultyReadResponseSchema,
    DepartmentReadResponseSchema,
    StudyDirectionReadResponseSchema,
    DisciplineReadResponseSchema,
    CurriculumReadResponseSchema,
    CourseReadResponseSchema,
    SemesterReadResponseSchema,
    StudyGroupReadResponseSchema,
)
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

    async def get_faculty(self, faculty_id: int) -> Optional[FacultyReadResponseSchema]:
        model = await self.__repository.read(faculty_id)
        return FacultyReadResponseSchema.model_validate(model) if model else None

    async def get_faculties(self, size: int = 50, page: int = 1) -> Page[FacultyReadResponseSchema]:
        models, total = await self.__repository.find_all(size=size, page=page)
        return Page[FacultyReadResponseSchema](
            items=[FacultyReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_faculty(self, data: dict) -> FacultyReadResponseSchema:
        model = await self.__repository.create(data)
        return FacultyReadResponseSchema.model_validate(model)

    async def update_faculty(self, faculty_id: int, data: dict) -> Optional[FacultyReadResponseSchema]:
        model = await self.__repository.update(faculty_id, data)
        return FacultyReadResponseSchema.model_validate(model) if model else None

    async def delete_faculty(self, faculty_id: int) -> Optional[FacultyReadResponseSchema]:
        model = await self.__repository.delete(faculty_id)
        return FacultyReadResponseSchema.model_validate(model) if model else None


class DepartmentService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = DepartmentRepository(db_session)

    async def get_department(self, department_id: int) -> Optional[DepartmentReadResponseSchema]:
        model = await self.__repository.read(department_id)
        return DepartmentReadResponseSchema.model_validate(model) if model else None

    async def get_departments(
        self,
        size: int = 50,
        page: int = 1,
        faculty_id: Optional[int] = None
    ) -> Page[DepartmentReadResponseSchema]:
        models, total = await self.__repository.find_all(size=size, page=page, faculty_id=faculty_id)
        return Page[DepartmentReadResponseSchema](
            items=[DepartmentReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_department(self, data: dict) -> DepartmentReadResponseSchema:
        model = await self.__repository.create(data)
        return DepartmentReadResponseSchema.model_validate(model)

    async def update_department(self, department_id: int, data: dict) -> Optional[DepartmentReadResponseSchema]:
        model = await self.__repository.update(department_id, data)
        return DepartmentReadResponseSchema.model_validate(model) if model else None

    async def delete_department(self, department_id: int) -> Optional[DepartmentReadResponseSchema]:
        model = await self.__repository.delete(department_id)
        return DepartmentReadResponseSchema.model_validate(model) if model else None


class StudyDirectionService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = StudyDirectionRepository(db_session)

    async def get_study_direction(self, direction_id: int) -> Optional[StudyDirectionReadResponseSchema]:
        model = await self.__repository.read(direction_id)
        return StudyDirectionReadResponseSchema.model_validate(model) if model else None

    async def get_study_directions(
        self,
        size: int = 50,
        page: int = 1,
        faculty_id: Optional[int] = None
    ) -> Page[StudyDirectionReadResponseSchema]:
        models, total = await self.__repository.find_all(size=size, page=page, faculty_id=faculty_id)
        return Page[StudyDirectionReadResponseSchema](
            items=[StudyDirectionReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_study_direction(self, data: dict) -> StudyDirectionReadResponseSchema:
        model = await self.__repository.create(data)
        return StudyDirectionReadResponseSchema.model_validate(model)

    async def update_study_direction(self, direction_id: int, data: dict) -> Optional[StudyDirectionReadResponseSchema]:
        model = await self.__repository.update(direction_id, data)
        return StudyDirectionReadResponseSchema.model_validate(model) if model else None

    async def delete_study_direction(self, direction_id: int) -> Optional[StudyDirectionReadResponseSchema]:
        model = await self.__repository.delete(direction_id)
        return StudyDirectionReadResponseSchema.model_validate(model) if model else None


class DisciplineService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = DisciplineRepository(db_session)

    async def get_discipline(self, discipline_id: int) -> Optional[DisciplineReadResponseSchema]:
        model = await self.__repository.read(discipline_id)
        return DisciplineReadResponseSchema.model_validate(model) if model else None

    async def get_disciplines(
        self,
        size: int = 50,
        page: int = 1,
        study_direction_id: Optional[int] = None,
        department_id: Optional[int] = None
    ) -> Page[DisciplineReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            study_direction_id=study_direction_id,
            department_id=department_id
        )
        return Page[DisciplineReadResponseSchema](
            items=[DisciplineReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_discipline(self, data: dict) -> DisciplineReadResponseSchema:
        model = await self.__repository.create(data)
        return DisciplineReadResponseSchema.model_validate(model)

    async def update_discipline(self, discipline_id: int, data: dict) -> Optional[DisciplineReadResponseSchema]:
        model = await self.__repository.update(discipline_id, data)
        return DisciplineReadResponseSchema.model_validate(model) if model else None

    async def delete_discipline(self, discipline_id: int) -> Optional[DisciplineReadResponseSchema]:
        model = await self.__repository.delete(discipline_id)
        return DisciplineReadResponseSchema.model_validate(model) if model else None


class CurriculumService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = CurriculumRepository(db_session)

    async def get_curriculum(self, curriculum_id: int) -> Optional[CurriculumReadResponseSchema]:
        model = await self.__repository.read(curriculum_id)
        return CurriculumReadResponseSchema.model_validate(model) if model else None

    async def get_curricula(
        self,
        size: int = 50,
        page: int = 1,
        study_direction_id: Optional[int] = None
    ) -> Page[CurriculumReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            study_direction_id=study_direction_id
        )
        return Page[CurriculumReadResponseSchema](
            items=[CurriculumReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_curriculum(self, data: dict) -> CurriculumReadResponseSchema:
        model = await self.__repository.create(data)
        return CurriculumReadResponseSchema.model_validate(model)

    async def update_curriculum(self, curriculum_id: int, data: dict) -> Optional[CurriculumReadResponseSchema]:
        model = await self.__repository.update(curriculum_id, data)
        return CurriculumReadResponseSchema.model_validate(model) if model else None

    async def delete_curriculum(self, curriculum_id: int) -> Optional[CurriculumReadResponseSchema]:
        model = await self.__repository.delete(curriculum_id)
        return CurriculumReadResponseSchema.model_validate(model) if model else None


class CourseService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = CourseRepository(db_session)

    async def get_course(self, course_id: int) -> Optional[CourseReadResponseSchema]:
        model = await self.__repository.read(course_id)
        return CourseReadResponseSchema.model_validate(model) if model else None

    async def get_courses(self, size: int = 50, page: int = 1) -> Page[CourseReadResponseSchema]:
        models, total = await self.__repository.find_all(size=size, page=page)
        return Page[CourseReadResponseSchema](
            items=[CourseReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_course(self, data: dict) -> CourseReadResponseSchema:
        model = await self.__repository.create(data)
        return CourseReadResponseSchema.model_validate(model)

    async def update_course(self, course_id: int, data: dict) -> Optional[CourseReadResponseSchema]:
        model = await self.__repository.update(course_id, data)
        return CourseReadResponseSchema.model_validate(model) if model else None

    async def delete_course(self, course_id: int) -> Optional[CourseReadResponseSchema]:
        model = await self.__repository.delete(course_id)
        return CourseReadResponseSchema.model_validate(model) if model else None


class SemesterService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = SemesterRepository(db_session)

    async def get_semester(self, semester_id: int) -> Optional[SemesterReadResponseSchema]:
        model = await self.__repository.read(semester_id)
        return SemesterReadResponseSchema.model_validate(model) if model else None

    async def get_semesters(
        self,
        size: int = 50,
        page: int = 1,
        course_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> Page[SemesterReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            course_id=course_id,
            is_active=is_active
        )
        return Page[SemesterReadResponseSchema](
            items=[SemesterReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_semester(self, data: dict) -> SemesterReadResponseSchema:
        model = await self.__repository.create(data)
        return SemesterReadResponseSchema.model_validate(model)

    async def update_semester(self, semester_id: int, data: dict) -> Optional[SemesterReadResponseSchema]:
        model = await self.__repository.update(semester_id, data)
        return SemesterReadResponseSchema.model_validate(model) if model else None

    async def delete_semester(self, semester_id: int) -> Optional[SemesterReadResponseSchema]:
        model = await self.__repository.delete(semester_id)
        return SemesterReadResponseSchema.model_validate(model) if model else None

    async def get_active_semester(self) -> Optional[SemesterReadResponseSchema]:
        model = await self.__repository.find_one(is_active=True)
        return SemesterReadResponseSchema.model_validate(model) if model else None


class StudyGroupService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = StudyGroupRepository(db_session)

    async def get_study_group(self, group_id: int) -> Optional[StudyGroupReadResponseSchema]:
        model = await self.__repository.read(group_id)
        return StudyGroupReadResponseSchema.model_validate(model) if model else None

    async def get_study_groups(
        self,
        size: int = 50,
        page: int = 1,
        study_direction_id: Optional[int] = None,
        course_id: Optional[int] = None
    ) -> Page[StudyGroupReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            study_direction_id=study_direction_id,
            course_id=course_id
        )
        return Page[StudyGroupReadResponseSchema](
            items=[StudyGroupReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_study_group(self, data: dict) -> StudyGroupReadResponseSchema:
        model = await self.__repository.create(data)
        return StudyGroupReadResponseSchema.model_validate(model)

    async def update_study_group(self, group_id: int, data: dict) -> Optional[StudyGroupReadResponseSchema]:
        model = await self.__repository.update(group_id, data)
        return StudyGroupReadResponseSchema.model_validate(model) if model else None

    async def delete_study_group(self, group_id: int) -> Optional[StudyGroupReadResponseSchema]:
        model = await self.__repository.delete(group_id)
        return StudyGroupReadResponseSchema.model_validate(model) if model else None
