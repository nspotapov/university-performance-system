# Система учёта успеваемости студентов (University Performance System)

Система для управления учебным процессом и учёта успеваемости студентов в университете.

## Стек технологий

- **Backend**: Python 3, FastAPI, SQLAlchemy (async), Alembic
- **Frontend**: TypeScript, Nuxt.js 4, Nuxt UI
- **База данных**: PostgreSQL 17.9
- **Кэширование**: Redis
- **Контейнеризация**: Docker, Docker Compose

## Роли пользователей

| Роль | Код | Описание |
|------|-----|----------|
| Администратор системы | `ADMIN` | Полный доступ ко всем функциям системы |
| Ректор | `RECTOR` | Доступ к аналитике и управлению факультетами |
| Декан факультета | `DEAN` | Управление факультетом, направлениями, кафедрами |
| Заведующий кафедрой | `HEAD_TEACHER` | Управление кафедрой и преподавателями |
| Преподаватель | `TEACHER` | Ведение ведомостей, выставление оценок |
| Студент | `STUDENT` | Просмотр своих оценок и карточки успеваемости |

## Основные сущности

### Организационная структура
- **Факультеты** (Faculties)
- **Кафедры** (Departments)
- **Направления обучения** (Study Directions)

### Учебный процесс
- **Дисциплины** (Disciplines)
- **Учебные планы** (Curricula)
- **Курсы** (Courses)
- **Семестры** (Semesters)
- **Учебные группы** (Study Groups)

### Участники
- **Студенты** (Students)
- **Преподаватели** (Teachers)

### Успеваемость
- **Ведомости** (GradeBooks)
- **Оценки** (Grades)
- **Зачеты** (Credits)
- **Экзамены** (Exams)

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd university-performance-system
```

### 2. Настройка переменных окружения

```bash
# Backend
cp backend/.env.example backend/.env
# Отредактируйте backend/.env, указав необходимые параметры

# Frontend
cp frontend/.env.example frontend/.env
```

### 3. Запуск через Docker Compose

```bash
docker-compose up -d
```

### 4. Применение миграций

```bash
docker-compose exec backend alembic upgrade head
```

### 5. Наполнение тестовыми данными

```bash
docker-compose exec backend python -m app.scripts.seed_data
```

## API Документация

После запуска backend сервера документация Swagger доступна по адресу:
- **Swagger UI**: http://localhost:8000/api/docs

### Основные endpoints

#### Аутентификация
- `POST /api/v1/auth/login` - Вход в систему
- `POST /api/v1/auth/logout` - Выход из системы
- `POST /api/v1/auth/refresh` - Обновление токена
- `GET /api/v1/auth/mfa/method` - Получение метода MFA
- `POST /api/v1/auth/mfa/totp/verify` - Проверка TOTP кода
- `GET /api/v1/auth/current-user` - Получение данных текущего пользователя

#### Управление пользователями (ADMIN)
- `GET /api/v1/users` - Список пользователей
- `GET /api/v1/users/{id}` - Данные пользователя
- `POST /api/v1/users` - Создание пользователя
- `PATCH /api/v1/users/{id}` - Обновление пользователя
- `DELETE /api/v1/users/{id}` - Удаление пользователя

#### Факультеты
- `GET /api/v1/faculties` - Список факультетов
- `GET /api/v1/faculties/{id}` - Данные факультета
- `POST /api/v1/faculties` - Создание факультета
- `PATCH /api/v1/faculties/{id}` - Обновление факультета
- `DELETE /api/v1/faculties/{id}` - Удаление факультета

#### Кафедры
- `GET /api/v1/departments` - Список кафедр
- `GET /api/v1/departments/{id}` - Данные кафедры
- `POST /api/v1/departments` - Создание кафедры
- `PATCH /api/v1/departments/{id}` - Обновление кафедры
- `DELETE /api/v1/departments/{id}` - Удаление кафедры

#### Направления обучения
- `GET /api/v1/study-directions` - Список направлений
- `GET /api/v1/study-directions/{id}` - Данные направления
- `POST /api/v1/study-directions` - Создание направления
- `PATCH /api/v1/study-directions/{id}` - Обновление направления
- `DELETE /api/v1/study-directions/{id}` - Удаление направления

#### Дисциплины
- `GET /api/v1/disciplines` - Список дисциплин
- `GET /api/v1/disciplines/{id}` - Данные дисциплины
- `POST /api/v1/disciplines` - Создание дисциплины
- `PATCH /api/v1/disciplines/{id}` - Обновление дисциплины
- `DELETE /api/v1/disciplines/{id}` - Удаление дисциплины

#### Семестры
- `GET /api/v1/semesters` - Список семестров
- `GET /api/v1/semesters/{id}` - Данные семестра
- `GET /api/v1/semesters/active/current` - Текущий активный семестр
- `POST /api/v1/semesters` - Создание семестра
- `PATCH /api/v1/semesters/{id}` - Обновление семестра
- `DELETE /api/v1/semesters/{id}` - Удаление семестра

#### Учебные группы
- `GET /api/v1/study-groups` - Список учебных групп
- `GET /api/v1/study-groups/{id}` - Данные группы
- `POST /api/v1/study-groups` - Создание группы
- `PATCH /api/v1/study-groups/{id}` - Обновление группы
- `DELETE /api/v1/study-groups/{id}` - Удаление группы

#### Студенты
- `GET /api/v1/students` - Список студентов
- `GET /api/v1/students/{id}` - Данные студента
- `POST /api/v1/students` - Создание студента
- `PATCH /api/v1/students/{id}` - Обновление студента
- `DELETE /api/v1/students/{id}` - Удаление студента

#### Преподаватели
- `GET /api/v1/teachers` - Список преподавателей
- `GET /api/v1/teachers/{id}` - Данные преподавателя
- `POST /api/v1/teachers` - Создание преподавателя
- `PATCH /api/v1/teachers/{id}` - Обновление преподавателя
- `DELETE /api/v1/teachers/{id}` - Удаление преподавателя

#### Ведомости
- `GET /api/v1/gradebooks` - Список ведомостей
- `GET /api/v1/gradebooks/{id}` - Данные ведомости
- `POST /api/v1/gradebooks` - Создание ведомости
- `PATCH /api/v1/gradebooks/{id}` - Обновление ведомости
- `DELETE /api/v1/gradebooks/{id}` - Удаление ведомости

#### Оценки
- `GET /api/v1/grades` - Список оценок
- `GET /api/v1/grades/{id}` - Данные оценки
- `POST /api/v1/grades` - Создание оценки
- `PATCH /api/v1/grades/{id}` - Обновление оценки
- `DELETE /api/v1/grades/{id}` - Удаление оценки

#### Зачеты
- `GET /api/v1/credits` - Список зачетов
- `GET /api/v1/credits/{id}` - Данные зачета
- `POST /api/v1/credits` - Создание зачета
- `PATCH /api/v1/credits/{id}` - Обновление зачета
- `DELETE /api/v1/credits/{id}` - Удаление зачета

#### Экзамены
- `GET /api/v1/exams` - Список экзаменов
- `GET /api/v1/exams/{id}` - Данные экзамена
- `POST /api/v1/exams` - Создание экзамена
- `PATCH /api/v1/exams/{id}` - Обновление экзамена
- `DELETE /api/v1/exams/{id}` - Удаление экзамена

#### Аналитика
- `GET /api/v1/analytics/performance/faculty/{faculty_id}` - Успеваемость по факультету
- `GET /api/v1/analytics/performance/direction/{direction_id}` - Успеваемость по направлению
- `GET /api/v1/analytics/performance/course/{course_id}` - Успеваемость по курсу
- `GET /api/v1/analytics/performance/group/{group_id}` - Успеваемость по группе
- `GET /api/v1/analytics/student/{student_id}/card` - Карточка студента (JSON)
- `GET /api/v1/analytics/student/{student_id}/card/print` - Карточка студента (HTML для печати)

## Тестовые учетные данные

После выполнения скрипта `seed_data` доступны следующие учетные записи:

| Роль | Email | Пароль |
|------|-------|--------|
| Admin | admin@university.ru | admin123 |
| Dean | dean@university.ru | dean123 |
| Head Teacher | head@university.ru | head123 |
| Teacher | teacher@university.ru | teacher123 |
| Student | student@university.ru | student123 |

## Сервисы Docker Compose

| Сервис | Порт | Описание |
|--------|------|----------|
| backend | 8000 | FastAPI сервер |
| frontend | 3000 | Nuxt.js приложение |
| db (PostgreSQL) | 5432 | База данных |
| redis | 6379 | Кэш-сервер |
| mailhog | 8025, 1025 | Тестовый SMTP сервер |
| adminer | 8080 | Веб-интерфейс для БД |
| redisinsight | 5540 | Веб-интерфейс для Redis |

## Разработка

### Backend

```bash
cd backend
# Установка зависимостей
pip install -r requirements.txt

# Запуск миграций
alembic upgrade head

# Создание новой миграции
alembic revision --autogenerate -m "Description"

# Запуск сервера разработки
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
# Установка зависимостей
npm install

# Запуск сервера разработки
npm run dev

# Сборка для production
npm run build
```

## Структура проекта

```
university-performance-system/
├── backend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/          # API endpoints
│   │   │   ├── core/         # Конфигурация, безопасность
│   │   │   ├── db/           # Подключение к БД
│   │   │   ├── enums/        # Перечисления
│   │   │   ├── models/       # SQLAlchemy модели
│   │   │   ├── repositories/ # Репозитории
│   │   │   ├── scripts/      # Скрипты (seed и т.д.)
│   │   │   ├── services/     # Бизнес-логика
│   │   │   └── main.py       # Точка входа
│   │   └── alembic/          # Миграции БД
│   └── requirements.txt
├── frontend/
│   └── src/
│       └── app/
│           ├── pages/        # Страницы Nuxt
│           ├── components/   # Vue компоненты
│           ├── composables/  # Composables
│           ├── middleware/   # Middleware
│           ├── plugins/      # Плагины
│           └── types/        # TypeScript типы
└── docker-compose.yaml
```

## Лицензия

MIT
