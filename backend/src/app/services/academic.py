from datetime import date
from typing import Optional, List, Dict, Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import Page
from app.models import (
    Student,
    Teacher,
    StudentGroup,
    GradeBook,
    Grade,
    Credit,
    Exam,
    GradeValue,
    StudyGroup,
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
)


class StudentService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = StudentRepository(db_session)

    async def get_student(self, student_id: int) -> Optional[Student]:
        return await self.__repository.read(student_id)

    async def get_students(
        self,
        size: int = 50,
        page: int = 1,
        user_id: Optional[int] = None,
        is_expelled: Optional[bool] = None
    ) -> Page[Student]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            user_id=user_id,
            is_expelled=is_expelled
        )
        return Page[Student](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_student(self, data: dict) -> Student:
        return await self.__repository.create(data)

    async def update_student(self, student_id: int, data: dict) -> Optional[Student]:
        return await self.__repository.update(student_id, data)

    async def delete_student(self, student_id: int) -> Optional[Student]:
        return await self.__repository.delete(student_id)

    async def get_student_by_user_id(self, user_id: int) -> Optional[Student]:
        return await self.__repository.find_one(user_id=user_id)

    async def get_student_groups(self, student_id: int) -> List[StudentGroup]:
        items = await self.__repository.find_many(
            limit=100,
            student_id=student_id
        )
        return items

    async def get_current_study_group(self, student_id: int) -> Optional[StudyGroup]:
        """Получить текущую учебную группу студента"""
        query = (
            select(StudyGroup)
            .join(StudentGroup, StudyGroup.id == StudentGroup.study_group_id)
            .where(StudentGroup.student_id == student_id, StudentGroup.is_current == True)
        )
        result = await self.__db_session.execute(query)
        return result.scalar_one_or_none()


class TeacherService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = TeacherRepository(db_session)

    async def get_teacher(self, teacher_id: int) -> Optional[Teacher]:
        return await self.__repository.read(teacher_id)

    async def get_teachers(
        self,
        size: int = 50,
        page: int = 1,
        user_id: Optional[int] = None,
        department_id: Optional[int] = None,
        is_fired: Optional[bool] = None
    ) -> Page[Teacher]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            user_id=user_id,
            department_id=department_id,
            is_fired=is_fired
        )
        return Page[Teacher](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_teacher(self, data: dict) -> Teacher:
        return await self.__repository.create(data)

    async def update_teacher(self, teacher_id: int, data: dict) -> Optional[Teacher]:
        return await self.__repository.update(teacher_id, data)

    async def delete_teacher(self, teacher_id: int) -> Optional[Teacher]:
        return await self.__repository.delete(teacher_id)

    async def get_teacher_by_user_id(self, user_id: int) -> Optional[Teacher]:
        return await self.__repository.find_one(user_id=user_id)


class StudentGroupService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = StudentGroupRepository(db_session)

    async def get_student_group(self, id: int) -> Optional[StudentGroup]:
        return await self.__repository.read(id)

    async def get_student_groups(
        self,
        size: int = 50,
        page: int = 1,
        student_id: Optional[int] = None,
        study_group_id: Optional[int] = None,
        is_current: Optional[bool] = None
    ) -> Page[StudentGroup]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            student_id=student_id,
            study_group_id=study_group_id,
            is_current=is_current
        )
        return Page[StudentGroup](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_student_group(self, data: dict) -> StudentGroup:
        return await self.__repository.create(data)

    async def update_student_group(self, id: int, data: dict) -> Optional[StudentGroup]:
        return await self.__repository.update(id, data)

    async def delete_student_group(self, id: int) -> Optional[StudentGroup]:
        return await self.__repository.delete(id)


class GradeBookService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = GradeBookRepository(db_session)

    async def get_gradebook(self, gradebook_id: int) -> Optional[GradeBook]:
        return await self.__repository.read(gradebook_id)

    async def get_gradebooks(
        self,
        size: int = 50,
        page: int = 1,
        semester_id: Optional[int] = None,
        study_group_id: Optional[int] = None,
        discipline_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        is_closed: Optional[bool] = None
    ) -> Page[GradeBook]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            semester_id=semester_id,
            study_group_id=study_group_id,
            discipline_id=discipline_id,
            teacher_id=teacher_id,
            is_closed=is_closed
        )
        return Page[GradeBook](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_gradebook(self, data: dict) -> GradeBook:
        return await self.__repository.create(data)

    async def update_gradebook(self, gradebook_id: int, data: dict) -> Optional[GradeBook]:
        return await self.__repository.update(gradebook_id, data)

    async def delete_gradebook(self, gradebook_id: int) -> Optional[GradeBook]:
        return await self.__repository.delete(gradebook_id)


class GradeService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = GradeRepository(db_session)

    async def get_grade(self, grade_id: int) -> Optional[Grade]:
        return await self.__repository.read(grade_id)

    async def get_grades(
        self,
        size: int = 50,
        page: int = 1,
        gradebook_id: Optional[int] = None,
        student_id: Optional[int] = None
    ) -> Page[Grade]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            gradebook_id=gradebook_id,
            student_id=student_id
        )
        return Page[Grade](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_grade(self, data: dict) -> Grade:
        return await self.__repository.create(data)

    async def update_grade(self, grade_id: int, data: dict) -> Optional[Grade]:
        return await self.__repository.update(grade_id, data)

    async def delete_grade(self, grade_id: int) -> Optional[Grade]:
        return await self.__repository.delete(grade_id)

    async def get_student_grades_for_semester(
        self,
        student_id: int,
        semester_id: int
    ) -> List[Dict[str, Any]]:
        """Получить все оценки студента за семестр"""
        query = (
            select(
                Grade,
                Discipline.name.label('discipline_name'),
                GradeBook.grade_type.label('grade_type'),
            )
            .join(GradeBook, Grade.gradebook_id == GradeBook.id)
            .join(Discipline, GradeBook.discipline_id == Discipline.id)
            .where(
                Grade.student_id == student_id,
                GradeBook.semester_id == semester_id
            )
        )
        result = await self.__db_session.execute(query)
        grades = []
        for row in result.all():
            grades.append({
                'id': row.Grade.id,
                'grade_value': row.Grade.grade_value,
                'grade_date': row.Grade.grade_date,
                'comment': row.Grade.comment,
                'discipline_name': row.discipline_name,
                'grade_type': row.grade_type,
            })
        return grades


class CreditService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = CreditRepository(db_session)

    async def get_credit(self, credit_id: int) -> Optional[Credit]:
        return await self.__repository.read(credit_id)

    async def get_credits(
        self,
        size: int = 50,
        page: int = 1,
        student_id: Optional[int] = None,
        discipline_id: Optional[int] = None,
        semester_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        is_passed: Optional[bool] = None
    ) -> Page[Credit]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            student_id=student_id,
            discipline_id=discipline_id,
            semester_id=semester_id,
            teacher_id=teacher_id,
            is_passed=is_passed
        )
        return Page[Credit](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_credit(self, data: dict) -> Credit:
        return await self.__repository.create(data)

    async def update_credit(self, credit_id: int, data: dict) -> Optional[Credit]:
        return await self.__repository.update(credit_id, data)

    async def delete_credit(self, credit_id: int) -> Optional[Credit]:
        return await self.__repository.delete(credit_id)


class ExamService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__repository = ExamRepository(db_session)

    async def get_exam(self, exam_id: int) -> Optional[Exam]:
        return await self.__repository.read(exam_id)

    async def get_exams(
        self,
        size: int = 50,
        page: int = 1,
        student_id: Optional[int] = None,
        discipline_id: Optional[int] = None,
        semester_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
    ) -> Page[Exam]:
        items, total = await self.__repository.find_all(
            size=size,
            page=page,
            student_id=student_id,
            discipline_id=discipline_id,
            semester_id=semester_id,
            teacher_id=teacher_id,
        )
        return Page[Exam](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_exam(self, data: dict) -> Exam:
        return await self.__repository.create(data)

    async def update_exam(self, exam_id: int, data: dict) -> Optional[Exam]:
        return await self.__repository.update(exam_id, data)

    async def delete_exam(self, exam_id: int) -> Optional[Exam]:
        return await self.__repository.delete(exam_id)


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
            .join(StudyGroup, StudentGroup.study_group_id == StudyGroup.id)
            .join(StudyDirection, StudyGroup.study_direction_id == StudyDirection.id)
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
        success_rate = (((excellent + good + satisfactory) / total) * 100) if total > 0 else 0
        
        return {
            'total_students': total,
            'excellent': excellent,
            'good': good,
            'satisfactory': satisfactory,
            'unsatisfactory': unsatisfactory,
            'quality_percentage': round(quality, 2),
            'success_rate_percentage': round(success_rate, 2),
        }

    async def get_study_direction_performance(
        self,
        direction_id: int,
        semester_id: int
    ) -> Dict[str, Any]:
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
            .join(StudyGroup, StudentGroup.study_group_id == StudyGroup.id)
            .join(Grade, Student.id == Grade.student_id)
            .join(GradeBook, Grade.gradebook_id == GradeBook.id)
            .where(
                StudyGroup.study_direction_id == direction_id,
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
        success_rate = (((excellent + good + satisfactory) / total) * 100) if total > 0 else 0
        
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
            .join(StudyGroup, StudentGroup.study_group_id == StudyGroup.id)
            .join(Grade, Student.id == Grade.student_id)
            .join(GradeBook, Grade.gradebook_id == GradeBook.id)
            .where(
                StudyGroup.course_id == course_id,
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
        success_rate = (((excellent + good + satisfactory) / total) * 100) if total > 0 else 0
        
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
        # Получаем данные студента
        student_repo = StudentRepository(self.__db_session)
        student = await student_repo.read(student_id)
        
        if not student:
            return None
        
        # Получаем текущую группу
        student_group_repo = StudentGroupRepository(self.__db_session)
        student_groups = await student_group_repo.find_many(
            limit=10,
            student_id=student_id,
            is_current=True
        )
        
        study_group_name = None
        if student_groups:
            study_group = student_groups[0]
            study_group_repo = StudyGroupRepository(self.__db_session)
            group = await study_group_repo.read(study_group.study_group_id)
            study_group_name = group.name if group else None
        
        # Получаем все оценки студента
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
        
        # Получаем зачеты
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
        
        # Получаем экзамены
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
                'birth_date': student.birth_date,
                'enrollment_year': student.enrollment_year,
                'is_expelled': student.is_expelled,
            },
            'study_group': study_group_name,
            'grades_by_semester': grades_by_semester,
            'credits_by_semester': credits_by_semester,
            'exams_by_semester': exams_by_semester,
        }
