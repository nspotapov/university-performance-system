from datetime import date
from typing import Optional, List, Dict, Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import Page
from app.api.v1.academic.schemas import (
    StudentReadResponseSchema,
    TeacherReadResponseSchema,
    StudentGroupReadResponseSchema,
    GradeBookReadResponseSchema,
    GradeReadResponseSchema,
    CreditReadResponseSchema,
    ExamReadResponseSchema,
)
from app.api.v1.university.schemas import StudyGroupReadResponseSchema
from app.models import (
    Student,
    Teacher,
    StudentGroup,
    GradeBook,
    Grade,
    Credit,
    Exam,
    GradeValue,
    StudyGroup as StudyGroupModel,
    Semester,
    Discipline,
    Faculty,
    StudyDirection,
    Course,
)
from app.repositories import (
    StudentRepository,
    TeacherRepository,
    StudentGroupRepository,
    GradeBookRepository,
    GradeRepository,
    CreditRepository,
    ExamRepository,
    StudyGroupRepository as StudyGroupModelRepository,
)


class StudentService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = StudentRepository(db_session)

    async def get_student(self, student_id: int) -> Optional[StudentReadResponseSchema]:
        model = await self.__repository.read(student_id)
        return StudentReadResponseSchema.model_validate(model) if model else None

    async def get_students(
        self,
        size: int = 50,
        page: int = 1,
        user_id: Optional[int] = None,
        is_expelled: Optional[bool] = None
    ) -> Page[StudentReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            user_id=user_id,
            is_expelled=is_expelled
        )
        return Page[StudentReadResponseSchema](
            items=[StudentReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_student(self, data: dict) -> StudentReadResponseSchema:
        model = await self.__repository.create(data)
        return StudentReadResponseSchema.model_validate(model)

    async def update_student(self, student_id: int, data: dict) -> Optional[StudentReadResponseSchema]:
        model = await self.__repository.update(student_id, data)
        return StudentReadResponseSchema.model_validate(model) if model else None

    async def delete_student(self, student_id: int) -> Optional[StudentReadResponseSchema]:
        model = await self.__repository.delete(student_id)
        return StudentReadResponseSchema.model_validate(model) if model else None

    async def get_student_by_user_id(self, user_id: int) -> Optional[StudentReadResponseSchema]:
        model = await self.__repository.find_one(user_id=user_id)
        return StudentReadResponseSchema.model_validate(model) if model else None


class TeacherService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = TeacherRepository(db_session)

    async def get_teacher(self, teacher_id: int) -> Optional[TeacherReadResponseSchema]:
        model = await self.__repository.read(teacher_id)
        return TeacherReadResponseSchema.model_validate(model) if model else None

    async def get_teachers(
        self,
        size: int = 50,
        page: int = 1,
        user_id: Optional[int] = None,
        department_id: Optional[int] = None,
        is_fired: Optional[bool] = None
    ) -> Page[TeacherReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            user_id=user_id,
            department_id=department_id,
            is_fired=is_fired
        )
        return Page[TeacherReadResponseSchema](
            items=[TeacherReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_teacher(self, data: dict) -> TeacherReadResponseSchema:
        model = await self.__repository.create(data)
        return TeacherReadResponseSchema.model_validate(model)

    async def update_teacher(self, teacher_id: int, data: dict) -> Optional[TeacherReadResponseSchema]:
        model = await self.__repository.update(teacher_id, data)
        return TeacherReadResponseSchema.model_validate(model) if model else None

    async def delete_teacher(self, teacher_id: int) -> Optional[TeacherReadResponseSchema]:
        model = await self.__repository.delete(teacher_id)
        return TeacherReadResponseSchema.model_validate(model) if model else None

    async def get_teacher_by_user_id(self, user_id: int) -> Optional[TeacherReadResponseSchema]:
        model = await self.__repository.find_one(user_id=user_id)
        return TeacherReadResponseSchema.model_validate(model) if model else None


class StudentGroupService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = StudentGroupRepository(db_session)

    async def get_student_group(self, id: int) -> Optional[StudentGroupReadResponseSchema]:
        model = await self.__repository.read(id)
        return StudentGroupReadResponseSchema.model_validate(model) if model else None

    async def get_student_groups(
        self,
        size: int = 50,
        page: int = 1,
        student_id: Optional[int] = None,
        study_group_id: Optional[int] = None,
        is_current: Optional[bool] = None
    ) -> Page[StudentGroupReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            student_id=student_id,
            study_group_id=study_group_id,
            is_current=is_current
        )
        return Page[StudentGroupReadResponseSchema](
            items=[StudentGroupReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_student_group(self, data: dict) -> StudentGroupReadResponseSchema:
        model = await self.__repository.create(data)
        return StudentGroupReadResponseSchema.model_validate(model)

    async def update_student_group(self, id: int, data: dict) -> Optional[StudentGroupReadResponseSchema]:
        model = await self.__repository.update(id, data)
        return StudentGroupReadResponseSchema.model_validate(model) if model else None

    async def delete_student_group(self, id: int) -> Optional[StudentGroupReadResponseSchema]:
        model = await self.__repository.delete(id)
        return StudentGroupReadResponseSchema.model_validate(model) if model else None


class GradeBookService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = GradeBookRepository(db_session)

    async def get_gradebook(self, gradebook_id: int) -> Optional[GradeBookReadResponseSchema]:
        model = await self.__repository.read(gradebook_id)
        return GradeBookReadResponseSchema.model_validate(model) if model else None

    async def get_gradebooks(
        self,
        size: int = 50,
        page: int = 1,
        semester_id: Optional[int] = None,
        study_group_id: Optional[int] = None,
        discipline_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        is_closed: Optional[bool] = None
    ) -> Page[GradeBookReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            semester_id=semester_id,
            study_group_id=study_group_id,
            discipline_id=discipline_id,
            teacher_id=teacher_id,
            is_closed=is_closed
        )
        return Page[GradeBookReadResponseSchema](
            items=[GradeBookReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_gradebook(self, data: dict) -> GradeBookReadResponseSchema:
        model = await self.__repository.create(data)
        return GradeBookReadResponseSchema.model_validate(model)

    async def update_gradebook(self, gradebook_id: int, data: dict) -> Optional[GradeBookReadResponseSchema]:
        model = await self.__repository.update(gradebook_id, data)
        return GradeBookReadResponseSchema.model_validate(model) if model else None

    async def delete_gradebook(self, gradebook_id: int) -> Optional[GradeBookReadResponseSchema]:
        model = await self.__repository.delete(gradebook_id)
        return GradeBookReadResponseSchema.model_validate(model) if model else None


class GradeService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = GradeRepository(db_session)

    async def get_grade(self, grade_id: int) -> Optional[GradeReadResponseSchema]:
        model = await self.__repository.read(grade_id)
        return GradeReadResponseSchema.model_validate(model) if model else None

    async def get_grades(
        self,
        size: int = 50,
        page: int = 1,
        gradebook_id: Optional[int] = None,
        student_id: Optional[int] = None
    ) -> Page[GradeReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            gradebook_id=gradebook_id,
            student_id=student_id
        )
        return Page[GradeReadResponseSchema](
            items=[GradeReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_grade(self, data: dict) -> GradeReadResponseSchema:
        model = await self.__repository.create(data)
        return GradeReadResponseSchema.model_validate(model)

    async def update_grade(self, grade_id: int, data: dict) -> Optional[GradeReadResponseSchema]:
        model = await self.__repository.update(grade_id, data)
        return GradeReadResponseSchema.model_validate(model) if model else None

    async def delete_grade(self, grade_id: int) -> Optional[GradeReadResponseSchema]:
        model = await self.__repository.delete(grade_id)
        return GradeReadResponseSchema.model_validate(model) if model else None


class CreditService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = CreditRepository(db_session)

    async def get_credit(self, credit_id: int) -> Optional[CreditReadResponseSchema]:
        model = await self.__repository.read(credit_id)
        return CreditReadResponseSchema.model_validate(model) if model else None

    async def get_credits(
        self,
        size: int = 50,
        page: int = 1,
        student_id: Optional[int] = None,
        discipline_id: Optional[int] = None,
        semester_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        is_passed: Optional[bool] = None
    ) -> Page[CreditReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            student_id=student_id,
            discipline_id=discipline_id,
            semester_id=semester_id,
            teacher_id=teacher_id,
            is_passed=is_passed
        )
        return Page[CreditReadResponseSchema](
            items=[CreditReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_credit(self, data: dict) -> CreditReadResponseSchema:
        model = await self.__repository.create(data)
        return CreditReadResponseSchema.model_validate(model)

    async def update_credit(self, credit_id: int, data: dict) -> Optional[CreditReadResponseSchema]:
        model = await self.__repository.update(credit_id, data)
        return CreditReadResponseSchema.model_validate(model) if model else None

    async def delete_credit(self, credit_id: int) -> Optional[CreditReadResponseSchema]:
        model = await self.__repository.delete(credit_id)
        return CreditReadResponseSchema.model_validate(model) if model else None


class ExamService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = ExamRepository(db_session)

    async def get_exam(self, exam_id: int) -> Optional[ExamReadResponseSchema]:
        model = await self.__repository.read(exam_id)
        return ExamReadResponseSchema.model_validate(model) if model else None

    async def get_exams(
        self,
        size: int = 50,
        page: int = 1,
        student_id: Optional[int] = None,
        discipline_id: Optional[int] = None,
        semester_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
    ) -> Page[ExamReadResponseSchema]:
        models, total = await self.__repository.find_all(
            size=size,
            page=page,
            student_id=student_id,
            discipline_id=discipline_id,
            semester_id=semester_id,
            teacher_id=teacher_id,
        )
        return Page[ExamReadResponseSchema](
            items=[ExamReadResponseSchema.model_validate(m) for m in models],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_exam(self, data: dict) -> ExamReadResponseSchema:
        model = await self.__repository.create(data)
        return ExamReadResponseSchema.model_validate(model)

    async def update_exam(self, exam_id: int, data: dict) -> Optional[ExamReadResponseSchema]:
        model = await self.__repository.update(exam_id, data)
        return ExamReadResponseSchema.model_validate(model) if model else None

    async def delete_exam(self, exam_id: int) -> Optional[ExamReadResponseSchema]:
        model = await self.__repository.delete(exam_id)
        return ExamReadResponseSchema.model_validate(model) if model else None


class PerformanceAnalyticsService:
    """Сервис аналитики успеваемости"""
    
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session

    async def get_faculty_performance(self, faculty_id: int, semester_id: int) -> Dict[str, Any]:
        """Аналитика успеваемости по факультету за семестр"""
        query = (
            select(
                func.count(Student.id).label('total_students'),
                func.sum(func.case((Grade.grade_value == GradeValue.EXCELLENT, 1), else_=0)).label('excellent'),
                func.sum(func.case((Grade.grade_value == GradeValue.GOOD, 1), else_=0)).label('good'),
                func.sum(func.case((Grade.grade_value == GradeValue.SATISFACTORY, 1), else_=0)).label('satisfactory'),
                func.sum(func.case((Grade.grade_value == GradeValue.UNSATISFACTORY, 1), else_=0)).label('unsatisfactory'),
            )
            .join(StudentGroup, Student.id == StudentGroup.student_id)
            .join(StudyGroupModel, StudentGroup.study_group_id == StudyGroupModel.id)
            .join(StudyDirection, StudyGroupModel.study_direction_id == StudyDirection.id)
            .join(Grade, Student.id == Grade.student_id)
            .join(GradeBook, Grade.gradebook_id == GradeBook.id)
            .where(
                StudyDirection.faculty_id == faculty_id,
                GradeBook.semester_id == semester_id,
                StudentGroup.is_current == True,
                Student.is_expelled == False
            )
        )
        result = await self.__db_session.execute(query)
        row = result.first()
        
        total = row.total_students or 0
        excellent = row.excellent or 0
        good = row.good or 0
        satisfactory = row.satisfactory or 0
        unsatisfactory = row.unsatisfactory or 0
        
        quality = ((excellent + good) / total * 100) if total > 0 else 0
        success_rate = ((excellent + good + satisfactory) / total * 100) if total > 0 else 0
        
        return {
            'total_students': total,
            'excellent': excellent,
            'good': good,
            'satisfactory': satisfactory,
            'unsatisfactory': unsatisfactory,
            'quality_percentage': round(quality, 2),
            'success_rate_percentage': round(success_rate, 2),
        }

    async def get_study_direction_performance(self, direction_id: int, semester_id: int) -> Dict[str, Any]:
        """Аналитика успеваемости по направлению обучения за семестр"""
        query = (
            select(
                func.count(Student.id).label('total_students'),
                func.sum(func.case((Grade.grade_value == GradeValue.EXCELLENT, 1), else_=0)).label('excellent'),
                func.sum(func.case((Grade.grade_value == GradeValue.GOOD, 1), else_=0)).label('good'),
                func.sum(func.case((Grade.grade_value == GradeValue.SATISFACTORY, 1), else_=0)).label('satisfactory'),
                func.sum(func.case((Grade.grade_value == GradeValue.UNSATISFACTORY, 1), else_=0)).label('unsatisfactory'),
            )
            .join(StudentGroup, Student.id == StudentGroup.student_id)
            .join(StudyGroupModel, StudentGroup.study_group_id == StudyGroupModel.id)
            .join(Grade, Student.id == Grade.student_id)
            .join(GradeBook, Grade.gradebook_id == GradeBook.id)
            .where(
                StudyGroupModel.study_direction_id == direction_id,
                GradeBook.semester_id == semester_id,
                StudentGroup.is_current == True,
                Student.is_expelled == False
            )
        )
        result = await self.__db_session.execute(query)
        row = result.first()
        
        total = row.total_students or 0
        excellent = row.excellent or 0
        good = row.good or 0
        satisfactory = row.satisfactory or 0
        unsatisfactory = row.unsatisfactory or 0
        
        quality = ((excellent + good) / total * 100) if total > 0 else 0
        success_rate = ((excellent + good + satisfactory) / total * 100) if total > 0 else 0
        
        return {
            'total_students': total,
            'excellent': excellent,
            'good': good,
            'satisfactory': satisfactory,
            'unsatisfactory': unsatisfactory,
            'quality_percentage': round(quality, 2),
            'success_rate_percentage': round(success_rate, 2),
        }

    async def get_course_performance(self, course_id: int, semester_id: int) -> Dict[str, Any]:
        """Аналитика успеваемости по курсу за семестр"""
        query = (
            select(
                func.count(Student.id).label('total_students'),
                func.sum(func.case((Grade.grade_value == GradeValue.EXCELLENT, 1), else_=0)).label('excellent'),
                func.sum(func.case((Grade.grade_value == GradeValue.GOOD, 1), else_=0)).label('good'),
                func.sum(func.case((Grade.grade_value == GradeValue.SATISFACTORY, 1), else_=0)).label('satisfactory'),
                func.sum(func.case((Grade.grade_value == GradeValue.UNSATISFACTORY, 1), else_=0)).label('unsatisfactory'),
            )
            .join(StudentGroup, Student.id == StudentGroup.student_id)
            .join(StudyGroupModel, StudentGroup.study_group_id == StudyGroupModel.id)
            .join(Grade, Student.id == Grade.student_id)
            .join(GradeBook, Grade.gradebook_id == GradeBook.id)
            .where(
                StudyGroupModel.course_id == course_id,
                GradeBook.semester_id == semester_id,
                StudentGroup.is_current == True,
                Student.is_expelled == False
            )
        )
        result = await self.__db_session.execute(query)
        row = result.first()
        
        total = row.total_students or 0
        excellent = row.excellent or 0
        good = row.good or 0
        satisfactory = row.satisfactory or 0
        unsatisfactory = row.unsatisfactory or 0
        
        quality = ((excellent + good) / total * 100) if total > 0 else 0
        success_rate = ((excellent + good + satisfactory) / total * 100) if total > 0 else 0
        
        return {
            'total_students': total,
            'excellent': excellent,
            'good': good,
            'satisfactory': satisfactory,
            'unsatisfactory': unsatisfactory,
            'quality_percentage': round(quality, 2),
            'success_rate_percentage': round(success_rate, 2),
        }

    async def get_group_performance(self, group_id: int, semester_id: int) -> Dict[str, Any]:
        """Аналитика успеваемости по учебной группе за семестр"""
        query = (
            select(
                func.count(Student.id).label('total_students'),
                func.sum(func.case((Grade.grade_value == GradeValue.EXCELLENT, 1), else_=0)).label('excellent'),
                func.sum(func.case((Grade.grade_value == GradeValue.GOOD, 1), else_=0)).label('good'),
                func.sum(func.case((Grade.grade_value == GradeValue.SATISFACTORY, 1), else_=0)).label('satisfactory'),
                func.sum(func.case((Grade.grade_value == GradeValue.UNSATISFACTORY, 1), else_=0)).label('unsatisfactory'),
            )
            .join(StudentGroup, Student.id == StudentGroup.student_id)
            .join(Grade, Student.id == Grade.student_id)
            .join(GradeBook, Grade.gradebook_id == GradeBook.id)
            .where(
                StudentGroup.study_group_id == group_id,
                GradeBook.semester_id == semester_id,
                StudentGroup.is_current == True,
                Student.is_expelled == False
            )
        )
        result = await self.__db_session.execute(query)
        row = result.first()
        
        total = row.total_students or 0
        excellent = row.excellent or 0
        good = row.good or 0
        satisfactory = row.satisfactory or 0
        unsatisfactory = row.unsatisfactory or 0
        
        quality = ((excellent + good) / total * 100) if total > 0 else 0
        success_rate = ((excellent + good + satisfactory) / total * 100) if total > 0 else 0
        
        return {
            'total_students': total,
            'excellent': excellent,
            'good': good,
            'satisfactory': satisfactory,
            'unsatisfactory': unsatisfactory,
            'quality_percentage': round(quality, 2),
            'success_rate_percentage': round(success_rate, 2),
        }

    async def get_student_card(self, student_id: int) -> Dict[str, Any]:
        """Карточка студента по успеваемости"""
        student_repo = StudentRepository(self.__db_session)
        student = await student_repo.read(student_id)
        
        if not student:
            return None
        
        student_group_repo = StudentGroupRepository(self.__db_session)
        student_groups = await student_group_repo.find_many(limit=10, student_id=student_id, is_current=True)
        
        study_group_name = None
        if student_groups:
            study_group = student_groups[0]
            study_group_repo = StudyGroupModelRepository(self.__db_session)
            group = await study_group_repo.read(study_group.study_group_id)
            study_group_name = group.name if group else None
        
        query = (
            select(
                Grade,
                Discipline.name.label('discipline_name'),
                GradeBook.grade_type.label('grade_type'),
                Semester.name.label('semester_name'),
            )
            .join(GradeBook, Grade.gradebook_id == GradeBook.id)
            .join(Discipline, GradeBook.discipline_id == Discipline.id)
            .join(Semester, GradeBook.semester_id == Semester.id)
            .where(Grade.student_id == student_id)
            .order_by(Semester.id, Discipline.name)
        )
        result = await self.__db_session.execute(query)
        
        grades_by_semester = {}
        for row in result.all():
            semester_name = row.semester_name
            if semester_name not in grades_by_semester:
                grades_by_semester[semester_name] = []
            grades_by_semester[semester_name].append({
                'discipline': row.discipline_name,
                'grade': row.Grade.grade_value,
                'type': row.grade_type,
                'date': row.Grade.grade_date,
            })
        
        credit_query = (
            select(
                Credit,
                Discipline.name.label('discipline_name'),
                Semester.name.label('semester_name'),
            )
            .join(Discipline, Credit.discipline_id == Discipline.id)
            .join(Semester, Credit.semester_id == Semester.id)
            .where(Credit.student_id == student_id)
            .order_by(Semester.id)
        )
        credit_result = await self.__db_session.execute(credit_query)
        
        credits_by_semester = {}
        for row in credit_result.all():
            semester_name = row.semester_name
            if semester_name not in credits_by_semester:
                credits_by_semester[semester_name] = []
            credits_by_semester[semester_name].append({
                'discipline': row.discipline_name,
                'passed': row.Credit.is_passed,
                'date': row.Credit.credit_date,
            })
        
        exam_query = (
            select(
                Exam,
                Discipline.name.label('discipline_name'),
                Semester.name.label('semester_name'),
            )
            .join(Discipline, Exam.discipline_id == Discipline.id)
            .join(Semester, Exam.semester_id == Semester.id)
            .where(Exam.student_id == student_id)
            .order_by(Semester.id)
        )
        exam_result = await self.__db_session.execute(exam_query)
        
        exams_by_semester = {}
        for row in exam_result.all():
            semester_name = row.semester_name
            if semester_name not in exams_by_semester:
                exams_by_semester[semester_name] = []
            exams_by_semester[semester_name].append({
                'discipline': row.discipline_name,
                'grade': row.Exam.grade_value,
                'date': row.Exam.exam_date,
            })
        
        return {
            'student': {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'middle_name': student.middle_name,
                'birth_date': student.birth_date.isoformat() if student.birth_date else None,
                'enrollment_year': student.enrollment_year,
                'is_expelled': student.is_expelled,
            },
            'study_group': study_group_name,
            'grades_by_semester': grades_by_semester,
            'credits_by_semester': credits_by_semester,
            'exams_by_semester': exams_by_semester,
        }
