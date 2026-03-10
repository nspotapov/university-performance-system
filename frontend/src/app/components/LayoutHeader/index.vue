<template>
  <header class="border-b border-gray-200 bg-white">
    <div class="container mx-auto px-5">
      <div class="flex items-center justify-between h-16">
        <!-- Логотип и название -->
        <div class="flex items-center gap-4">
          <NuxtLink to="/" class="flex items-center gap-2">
            <UIcon name="i-heroicons-academic-cap" class="w-8 h-8 text-primary" />
            <span class="font-bold text-lg hidden sm:block">Университет</span>
          </NuxtLink>
          
          <!-- Навигация -->
          <nav v-if="isAuthenticated" class="hidden md:flex items-center gap-1 ml-8">
            <UButton
              v-for="item in navigation"
              :key="item.to"
              :to="item.to"
              :label="item.label"
              variant="ghost"
              size="sm"
            />
          </nav>
        </div>

        <!-- Профиль пользователя -->
        <div class="flex items-center gap-4">
          <UDropdown
            :items="userMenuItems"
            :popper="{ placement: 'bottom-end' }"
          >
            <UButton
              :label="user?.email"
              icon="i-heroicons-user-circle"
              color="neutral"
              variant="ghost"
            />
          </UDropdown>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { UserRole } from '~/types/auth'
import { RoutePaths } from '~/types/routes'

const { user, isAuthenticated, logout, hasRole } = useAuth()

// Навигация в зависимости от роли
const navigation = computed(() => {
  const items: Array<{ to: string; label: string }> = []
  
  if (!user.value) return items
  
  // Общие для всех
  items.push({ to: RoutePaths.Main, label: 'Главная' })
  
  // Администратор
  if (hasRole([UserRole.ADMIN])) {
    items.push(
      { to: RoutePaths.Faculties.List, label: 'Факультеты' },
      { to: RoutePaths.Departments.List, label: 'Кафедры' },
      { to: RoutePaths.Directions.List, label: 'Направления' },
      { to: RoutePaths.Students.List, label: 'Студенты' },
      { to: RoutePaths.Teachers.List, label: 'Преподаватели' },
      { to: RoutePaths.Analytics.Dashboard, label: 'Аналитика' },
    )
  }
  
  // Декан
  if (hasRole([UserRole.DEAN])) {
    items.push(
      { to: RoutePaths.Faculties.List, label: 'Факультет' },
      { to: RoutePaths.Directions.List, label: 'Направления' },
      { to: RoutePaths.Students.List, label: 'Студенты' },
      { to: RoutePaths.Analytics.Dashboard, label: 'Аналитика' },
    )
  }
  
  // Преподаватель
  if (hasRole([UserRole.TEACHER])) {
    items.push(
      { to: RoutePaths.Gradebooks.List, label: 'Ведомости' },
      { to: RoutePaths.Analytics.Dashboard, label: 'Аналитика' },
    )
  }
  
  // Студент
  if (hasRole([UserRole.STUDENT])) {
    items.push(
      { to: RoutePaths.Students.Card(user.value.id), label: 'Моя карточка' },
      { to: RoutePaths.Analytics.Dashboard, label: 'Успеваемость' },
    )
  }
  
  return items
})

// Меню пользователя
const userMenuItems = computed(() => [
  [
    {
      label: user.value?.email || 'Гость',
      icon: 'i-heroicons-user',
      disabled: true,
    },
  ],
  [
    {
      label: 'Профиль',
      icon: 'i-heroicons-user-circle',
      to: RoutePaths.Profile.Settings,
    },
    {
      label: 'Безопасность',
      icon: 'i-heroicons-shield-check',
      to: RoutePaths.Profile.Security,
    },
  ],
  [
    {
      label: 'Выйти',
      icon: 'i-heroicons-arrow-right-on-rectangle',
      click: logout,
    },
  ],
])
</script>
