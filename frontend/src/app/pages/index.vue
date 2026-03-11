<template>
  <div class="flex-1 flex flex-col">
    <div class="py-8">
      <h1 class="text-3xl font-bold mb-2">Добро пожаловать!</h1>
      <p class="text-gray-600">
        {{ welcomeMessage }}
      </p>
    </div>

    <!-- Карточки быстрого доступа -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <UCard
        v-for="card in quickAccessCards"
        :key="card.title"
        :to="card.to"
        class="hover:shadow-lg transition-shadow cursor-pointer"
      >
        <template #header>
          <div class="flex items-center gap-3">
            <UIcon :name="card.icon" class="w-8 h-8 text-primary" />
            <h3 class="font-semibold text-lg">{{ card.title }}</h3>
          </div>
        </template>
        
        <p class="text-gray-600 text-sm">
          {{ card.description }}
        </p>
      </UCard>
    </div>

    <!-- Статистика -->
    <div v-if="showStats" class="mt-8">
      <h2 class="text-xl font-bold mb-4">Статистика успеваемости</h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <UCard v-for="stat in stats" :key="stat.label" class="p-4">
          <div class="text-center">
            <p class="text-sm text-gray-500">{{ stat.label }}</p>
            <p class="text-2xl font-bold mt-1" :class="`text-${stat.color}-600`">{{ stat.value }}</p>
          </div>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { UserRole } from '~/types/auth'
import { RoutePaths } from '~/types/routes'

const { user, hasRole } = useAuth()

// Приветственное сообщение в зависимости от роли
const welcomeMessage = computed(() => {
  if (!user.value) return 'Система учёта успеваемости студентов'
  
  const messages: Record<UserRole, string> = {
    [UserRole.ADMIN]: 'Панель администратора системы',
    [UserRole.RECTOR]: 'Панель ректора',
    [UserRole.DEAN]: 'Панель декана факультета',
    [UserRole.HEAD_TEACHER]: 'Панель заведующего кафедрой',
    [UserRole.TEACHER]: 'Панель преподавателя',
    [UserRole.STUDENT]: 'Личный кабинет студента',
  }
  
  return messages[user.value.role] || 'Добро пожаловать в систему'
})

// Карточки быстрого доступа в зависимости от роли
const quickAccessCards = computed(() => {
  if (!user.value) return []
  
  const cards: Array<{ title: string; description: string; icon: string; to: string }> = []
  
  if (hasRole([UserRole.ADMIN])) {
    cards.push(
      { title: 'Факультеты', description: 'Управление факультетами', icon: 'i-heroicons-building-library', to: RoutePaths.Faculties.List },
      { title: 'Студенты', description: 'Список студентов', icon: 'i-heroicons-users', to: RoutePaths.Students.List },
      { title: 'Преподаватели', description: 'Список преподавателей', icon: 'i-heroicons-user-group', to: RoutePaths.Teachers.List },
      { title: 'Аналитика', description: 'Отчёты и статистика', icon: 'i-heroicons-chart-bar', to: RoutePaths.Analytics.Dashboard },
    )
  }
  
  if (hasRole([UserRole.DEAN])) {
    cards.push(
      { title: 'Направления', description: 'Направления обучения', icon: 'i-heroicons-book-open', to: RoutePaths.Directions.List },
      { title: 'Студенты', description: 'Студенты факультета', icon: 'i-heroicons-users', to: RoutePaths.Students.List },
      { title: 'Аналитика', description: 'Успеваемость по факультету', icon: 'i-heroicons-chart-bar', to: RoutePaths.Analytics.Dashboard },
    )
  }
  
  if (hasRole([UserRole.TEACHER])) {
    cards.push(
      { title: 'Ведомости', description: 'Мои ведомости', icon: 'i-heroicons-clipboard-document-list', to: RoutePaths.Gradebooks.List },
      { title: 'Студенты', description: 'Список студентов', icon: 'i-heroicons-users', to: RoutePaths.Students.List },
    )
  }
  
  if (hasRole([UserRole.STUDENT])) {
    cards.push(
      { title: 'Моя карточка', description: 'Успеваемость и оценки', icon: 'i-heroicons-academic-cap', to: RoutePaths.Students.Card(user.value.id) },
      { title: 'Расписание', description: 'Расписание занятий', icon: 'i-heroicons-calendar-days', to: '#' },
    )
  }
  
  return cards
})

// Показывать ли статистику
const showStats = computed(() => {
  return hasRole([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER])
})

// Статистика (заглушка, потом загрузим из API)
const stats = ref([
  { label: 'Всего студентов', value: '0', color: 'primary' },
  { label: 'Средний балл', value: '0', color: 'success' },
  { label: 'Успеваемость', value: '0%', color: 'warning' },
  { label: 'Качество', value: '0%', color: 'info' },
])
</script>
