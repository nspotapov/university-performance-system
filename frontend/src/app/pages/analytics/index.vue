<template>
  <div class="py-8">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Аналитика успеваемости</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <UCard v-if="stats">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Всего студентов</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.total_students }}</p>
          </div>
          <UIcon name="i-heroicons-users" class="w-10 h-10 text-primary" />
        </div>
      </UCard>

      <UCard v-if="stats">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Отличники</p>
            <p class="text-2xl font-bold text-green-600">{{ stats.excellent }}</p>
          </div>
          <UIcon name="i-heroicons-star" class="w-10 h-10 text-green-600" />
        </div>
      </UCard>

      <UCard v-if="stats">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Успеваемость</p>
            <p class="text-2xl font-bold text-blue-600">{{ stats.success_rate_percentage }}%</p>
          </div>
          <UIcon name="i-heroicons-chart-bar" class="w-10 h-10 text-blue-600" />
        </div>
      </UCard>

      <UCard v-if="stats">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Качество</p>
            <p class="text-2xl font-bold text-purple-600">{{ stats.quality_percentage }}%</p>
          </div>
          <UIcon name="i-heroicons-academic-cap" class="w-10 h-10 text-purple-600" />
        </div>
      </UCard>
    </div>

    <UCard>
      <template #header>
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Параметры отчета</h2>
      </template>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <UFormField label="Факультет">
          <USelect v-model="filters.faculty_id" :options="facultyOptions" option-attribute="label" value-attribute="value" placeholder="Все факультеты" class="w-full" @change="loadAnalytics" />
        </UFormField>
        <UFormField label="Направление">
          <USelect v-model="filters.direction_id" :options="directionOptions" option-attribute="label" value-attribute="value" placeholder="Все направления" class="w-full" @change="loadAnalytics" />
        </UFormField>
        <UFormField label="Курс">
          <USelect v-model="filters.course_id" :options="courseOptions" option-attribute="label" value-attribute="value" placeholder="Все курсы" class="w-full" @change="loadAnalytics" />
        </UFormField>
      </div>
    </UCard>

    <div v-if="stats" class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <UCard>
        <template #header>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Распределение оценок</h3>
        </template>
        <div class="space-y-4">
          <div v-for="item in gradeDistribution" :key="item.label" class="flex items-center gap-4">
            <span class="w-24 text-sm text-gray-600 dark:text-gray-400">{{ item.label }}</span>
            <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-4">
              <div :class="['h-4 rounded-full', item.color]" :style="{ width: item.percent + '%' }" />
            </div>
            <span class="w-12 text-sm text-right">{{ item.count }}</span>
          </div>
        </div>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Общая статистика</h3>
        </template>
        <div class="space-y-4">
          <div class="flex justify-between">
            <span class="text-gray-600 dark:text-gray-400">Успеваемость</span>
            <span class="font-semibold">{{ stats.success_rate_percentage }}%</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600 dark:text-gray-400">Качество знаний</span>
            <span class="font-semibold">{{ stats.quality_percentage }}%</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600 dark:text-gray-400">Неудовлетворительно</span>
            <span class="font-semibold text-red-600">{{ stats.unsatisfactory }}</span>
          </div>
        </div>
      </UCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PerformanceStats } from '~/types/academic'

definePageMeta({ middleware: ['auth'] })

const { getFacultyPerformance, getFaculties, getStudyDirections, getCourses } = useAcademic()
const toast = useToast()

const stats = ref<PerformanceStats | null>(null)
const facultyOptions = ref<any[]>([])
const directionOptions = ref<any[]>([])
const courseOptions = ref<any[]>([])

const filters = reactive({ faculty_id: '', direction_id: '', course_id: '' })

const gradeDistribution = computed(() => {
  if (!stats.value) return []
  const total = stats.value.total_students || 1
  return [
    { label: 'Отлично', count: stats.value.excellent, percent: (stats.value.excellent / total) * 100, color: 'bg-green-500' },
    { label: 'Хорошо', count: stats.value.good, percent: (stats.value.good / total) * 100, color: 'bg-blue-500' },
    { label: 'Удовл.', count: stats.value.satisfactory, percent: (stats.value.satisfactory / total) * 100, color: 'bg-yellow-500' },
    { label: 'Неуд.', count: stats.value.unsatisfactory, percent: (stats.value.unsatisfactory / total) * 100, color: 'bg-red-500' },
  ]
})

const loadAnalytics = async () => {
  try {
    if (filters.faculty_id) {
      stats.value = await getFacultyPerformance(Number(filters.faculty_id), 1)
    }
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' })
  }
}

const loadOptions = async () => {
  try {
    const [faculties, directions, courses] = await Promise.all([getFaculties(), getStudyDirections(), getCourses()])
    facultyOptions.value = [{ value: '', label: 'Все факультеты' }, ...faculties.items.map((f: any) => ({ value: f.id, label: f.name }))]
    directionOptions.value = [{ value: '', label: 'Все направления' }, ...directions.items.map((d: any) => ({ value: d.id, label: d.name }))]
    courseOptions.value = [{ value: '', label: 'Все курсы' }, ...courses.items.map((c: any) => ({ value: c.id, label: `${c.number} курс` }))]
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' })
  }
}

onMounted(() => { loadOptions(); loadAnalytics() })
</script>
