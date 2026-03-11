# University Performance System - Frontend

Система учёта успеваемости студентов - Frontend приложение на Nuxt.js 4 + Nuxt UI.

## Стек технологий

- **Framework**: Nuxt.js 4
- **UI Library**: Nuxt UI (Tailwind CSS)
- **Language**: TypeScript
- **Validation**: Valibot
- **State**: Vue Reactivity (ref, reactive, computed)

## Структура проекта

```
frontend/src/app/
├── components/          # Vue компоненты
│   ├── LayoutHeader/    # Шапка с навигацией
│   └── LayoutFooter/    # Подвал
├── composables/         # Composables функции
│   ├── useAuth.ts       # Аутентификация и авторизация
│   ├── useUniversity.ts # API университетских сущностей
│   └── useAcademic.ts   # API академических сущностей
├── layouts/             # Layouts
│   ├── default.vue      # Основной layout
│   └── noAuthenticated.vue # Layout без авторизации
├── middleware/          # Middleware
│   └── auth.ts          # Проверка авторизации
├── pages/               # Страницы приложения
│   ├── auth/            # Страницы авторизации
│   ├── faculties/       # Факультеты
│   ├── departments/     # Кафедры
│   ├── directions/      # Направления
│   ├── groups/          # Группы
│   ├── semesters/       # Семестры
│   ├── disciplines/     # Дисциплины
│   ├── students/        # Студенты
│   ├── teachers/        # Преподаватели
│   ├── gradebooks/      # Ведомости
│   ├── analytics/       # Аналитика
│   └── profile/         # Профиль пользователя
├── plugins/             # Плагины Nuxt
│   └── api.ts           # API клиент
├── types/               # TypeScript типы
│   ├── auth.ts          # Типы авторизации
│   ├── routes.ts        # Маршруты
│   ├── university.ts    # Типы университетских сущностей
│   └── academic.ts      # Типы академических сущностей
└── app.config.ts        # Конфигурация приложения
```

## Роли пользователей

| Роль | Код | Доступ |
|------|-----|--------|
| Admin | `ADMIN` | Полный доступ |
| Rector | `RECTOR` | Аналитика, факультеты |
| Dean | `DEAN` | Факультет, направления, студенты |
| Head Teacher | `HEAD_TEACHER` | Кафедра, преподаватели |
| Teacher | `TEACHER` | Ведомости, оценки |
| Student | `STUDENT` | Карточка, оценки |

## Страницы приложения

### Авторизация
- `/auth/login` - Вход (email + пароль + 2FA)
- `/auth/mfa-required` - Настройка 2FA (TOTP/OTP)

### Университет
- `/faculties` - Факультеты (CRUD)
- `/departments` - Кафедры (CRUD)
- `/directions` - Направления обучения (CRUD)
- `/groups` - Учебные группы (CRUD)
- `/semesters` - Семестры (CRUD)
- `/disciplines` - Дисциплины (CRUD)

### Участники
- `/students` - Студенты (список, карточка)
- `/students/[id]` - Карточка студента (оценки, зачеты, экзамены)
- `/teachers` - Преподаватели (CRUD)

### Успеваемость
- `/gradebooks` - Ведомости (CRUD)
- `/gradebooks/[id]/grades` - Оценки в ведомости

### Аналитика
- `/analytics` - Дашборд успеваемости

### Профиль
- `/profile` - Информация о пользователе
- `/profile/security` - Безопасность (2FA, пароль)

## API Client

API клиент настроен в `plugins/api.ts`:

```typescript
// Базовый URL берется из nuxt.config.ts
baseURL: '/api'

// Автоматическое добавление токена
headers: { Authorization: `Bearer ${token}` }

// Обработка ошибок
onResponseError: handleApiError()
```

## Composables

### useAuth()
```typescript
const {
  user,              // Ref<User | null>
  isAuthenticated,   // Ref<boolean>
  isLoading,         // Ref<boolean>
  login,             // (data) => Promise<LoginResponse>
  verifyTotp,        // (code) => Promise<VerifyCodeResponse>
  sendOtp,           // () => Promise<OtpSendResponse>
  verifyOtp,         // (code) => Promise<VerifyCodeResponse>
  logout,            // () => Promise<void>
  getMfaStatus,      // () => Promise<MfaStatus>
  setupTotp,         // () => Promise<TotpSetupResponse>
  enableTotp,        // (code) => Promise<void>
  enableOtp,         // () => Promise<void>
  disableMfa,        // (password) => Promise<void>
  hasPermission,     // (permission) => boolean
  hasRole,           // (roles) => boolean
} = useAuth()
```

### useUniversity()
CRUD функции для: Faculty, Department, StudyDirection, Discipline, Course, Semester, StudyGroup

### useAcademic()
CRUD функции для: Student, Teacher, GradeBook, Grade + Analytics

## Аутентификация

### Двухфакторная аутентификация

**TOTP (Google Authenticator):**
1. Пользователь сканирует QR код
2. Вводит 6-значный код из приложения
3. Получает access + refresh токены

**OTP (Email):**
1. Пользователь выбирает метод OTP
2. Получает код на почту
3. Вводит код для подтверждения

**Обязательность 2FA:**
- ADMIN, RECTOR, DEAN, HEAD_TEACHER, TEACHER - обязательно
- STUDENT - опционально

## Темы оформления

Поддерживаются светлая и темная темы через Nuxt UI ColorMode.

```typescript
// app.config.ts
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'emerald',
      neutral: 'slate',
    },
  },
})
```

## Запуск разработки

```bash
cd frontend/src
pnpm install
pnpm dev
```

Приложение доступно на http://localhost:3000

## Сборка для production

```bash
pnpm build
pnpm preview
```

## Тестовые учетные данные

| Роль | Email | Пароль | 2FA |
|------|-------|--------|-----|
| Admin | admin@university.ru | admin123 | OTP |
| Dean | dean@university.ru | dean123 | OTP |
| Teacher | teacher@university.ru | teacher123 | OTP |
| Student | student@university.ru | student123 | Отключена |

Проверка почты: http://localhost:8025 (Mailhog)
