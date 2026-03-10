"""
Скрипт для наполнения БД тестовыми данными
"""
import asyncio
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models import (
    User, UserRole, MFAMethod,
    Faculty, Department, StudyDirection, Discipline, Curriculum,
    Course, Semester, StudyGroup,
    Student, Teacher, StudentGroup as StudentGroupLink,
    GradeBook, Grade, Credit, Exam, GradeType, GradeValue
)
from app.core.security import get_password_hash


async def seed():
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session_maker() as session:
        # Создаем пользователей
        # ADMIN, RECTOR, DEAN, HEAD_TEACHER, TEACHER - с включенной OTP (обязательно для ролей)
        admin = User(email="admin@university.ru", hashed_password=get_password_hash("admin123"), role=UserRole.ADMIN, is_active=True, is_mfa_enabled=True, mfa_method=MFAMethod.OTP)
        dean = User(email="dean@university.ru", hashed_password=get_password_hash("dean123"), role=UserRole.DEAN, is_active=True, is_mfa_enabled=True, mfa_method=MFAMethod.OTP)
        head_teacher = User(email="head@university.ru", hashed_password=get_password_hash("head123"), role=UserRole.HEAD_TEACHER, is_active=True, is_mfa_enabled=True, mfa_method=MFAMethod.OTP)
        teacher_user = User(email="teacher@university.ru", hashed_password=get_password_hash("teacher123"), role=UserRole.TEACHER, is_active=True, is_mfa_enabled=True, mfa_method=MFAMethod.OTP)
        
        # STUDENT - без 2FA (опционально)
        student_user = User(email="student@university.ru", hashed_password=get_password_hash("student123"), role=UserRole.STUDENT, is_active=True, is_mfa_enabled=False, mfa_method=MFAMethod.OTP)
        
        session.add_all([admin, dean, head_teacher, teacher_user, student_user])
        await session.flush()
        
        # Создаем факультет
        faculty = Faculty(name="Факультет информационных технологий", short_name="ФИТ", description="Факультет информационных технологий и систем")
        session.add(faculty)
        await session.flush()
        
        # Создаем кафедру
        department = Department(faculty_id=faculty.id, name="Кафедра информационных систем", short_name="Кафедра ИС", description="Кафедра информационных систем и технологий")
        session.add(department)
        await session.flush()
        
        # Создаем направление обучения
        study_direction = StudyDirection(faculty_id=faculty.id, name="Информатика и вычислительная техника", code="09.03.01", level="Бакалавриат", description="Направление подготовки бакалавров по информатике")
        session.add(study_direction)
        await session.flush()
        
        # Создаем дисциплину
        discipline = Discipline(study_direction_id=study_direction.id, department_id=department.id, name="Базы данных", code="БД-001", hours=144, description="Курс по проектированию и использованию баз данных")
        session.add(discipline)
        
        # Создаем учебный план
        curriculum = Curriculum(study_direction_id=study_direction.id, name="Учебный план 2024", year=2024, description="Основной учебный план")
        session.add(curriculum)
        
        # Создаем курсы
        course1 = Course(number=1, description="Первый курс")
        session.add(course1)
        await session.flush()
        
        # Создаем семестры
        semester1 = Semester(course_id=course1.id, number=1, name="Осенний семестр 2024", start_date="2024-09-01", end_date="2025-01-31", is_active=False)
        semester2 = Semester(course_id=course1.id, number=2, name="Весенний семестр 2025", start_date="2025-02-01", end_date="2025-06-30", is_active=True)
        session.add_all([semester1, semester2])
        await session.flush()
        
        # Создаем учебную группу
        study_group = StudyGroup(study_direction_id=study_direction.id, course_id=course1.id, name="ИВТ-101", year=2024, description="Группа ИВТ первого курса")
        session.add(study_group)
        await session.flush()
        
        # Создаем студента
        student = Student(user_id=student_user.id, first_name="Иван", last_name="Иванов", middle_name="Иванович", birth_date=date(2005, 1, 15), enrollment_year=2024, is_expelled=False)
        session.add(student)
        
        # Создаем преподавателя
        teacher = Teacher(user_id=teacher_user.id, department_id=department.id, first_name="Петр", last_name="Петров", middle_name="Петрович", position="Доцент", academic_degree="Кандидат технических наук", academic_title="Доцент", hire_date=date(2020, 9, 1), is_fired=False)
        session.add(teacher)
        await session.flush()
        
        # Привязываем студента к группе
        student_group_link = StudentGroupLink(student_id=student.id, study_group_id=study_group.id, start_date=date(2024, 9, 1), is_current=True)
        session.add(student_group_link)
        await session.flush()
        
        # Создаем ведомость
        gradebook = GradeBook(semester_id=semester1.id, study_group_id=study_group.id, discipline_id=discipline.id, teacher_id=teacher.id, grade_type=GradeType.EXAM, name="Экзамен по БД", created_at=date(2025, 1, 15), is_closed=False)
        session.add(gradebook)
        await session.flush()
        
        # Создаем оценку
        grade = Grade(gradebook_id=gradebook.id, student_id=student.id, grade_value=GradeValue.EXCELLENT, grade_date=date(2025, 1, 20), comment="Отличная работа")
        session.add(grade)
        
        # Создаем зачет
        credit = Credit(student_id=student.id, discipline_id=discipline.id, semester_id=semester1.id, teacher_id=teacher.id, is_passed=True, credit_date=date(2024, 12, 15), attempt_number=1)
        session.add(credit)
        
        # Создаем экзамен
        exam = Exam(student_id=student.id, discipline_id=discipline.id, semester_id=semester1.id, teacher_id=teacher.id, grade_value=GradeValue.EXCELLENT, exam_date=date(2025, 1, 20), attempt_number=1)
        session.add(exam)
        
        await session.commit()
        
        print("✓ Тестовые данные успешно добавлены!")
        print("\nУчетные данные для входа:")
        print("  Admin:    admin@university.ru / admin123 (OTP включен)")
        print("  Dean:     dean@university.ru / dean123 (OTP включен)")
        print("  Head:     head@university.ru / head123 (OTP включен)")
        print("  Teacher:  teacher@university.ru / teacher123 (OTP включен)")
        print("  Student:  student@university.ru / student123 (2FA опционально)")
        print("\nДля сотрудников с включенной OTP:")
        print("  1. Войдите с email и паролем")
        print("  2. Получите код на почту (Mailhog: http://localhost:8025)")
        print("  3. Введите код для входа")


if __name__ == "__main__":
    asyncio.run(seed())
