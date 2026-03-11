<template>
  <div class="py-8" v-if="studentCard">
    <div class="mb-6">
      <UButton color="neutral" variant="ghost" @click="navigateTo('/students')" class="mb-4">
        <UIcon name="i-heroicons-arrow-left" class="w-5 h-5 mr-2" />
        Назад к списку
      </UButton>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
        {{ studentCard.student.last_name }} {{ studentCard.student.first_name }} {{ studentCard.student.middle_name || '' }}
      </h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        Группа: {{ studentCard.study_group || 'Не указана' }} | Год поступления: {{ studentCard.student.enrollment_year }}
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Оценки по семестрам -->
      <UCard v-for="(grades, semester) in studentCard.grades_by_semester" :key="semester">
        <template #header>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ semester }}</h3>
        </template>
        <UTable :columns="gradeColumns" :data="grades.map((g: any) => ({
          discipline: g.discipline,
          grade: g.grade,
          type: g.type,
          date: g.date
        }))" />
      </UCard>
    </div>

    <!-- Зачеты -->
    <UCard class="mt-6" v-if="Object.keys(studentCard.credits_by_semester).length">
      <template #header>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Зачеты</h3>
      </template>
      <div v-for="(credits, semester) in studentCard.credits_by_semester" :key="semester" class="mb-4">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-2">{{ semester }}</h4>
        <UTable :columns="creditColumns" :data="credits.map((c: any) => ({
          discipline: c.discipline,
          passed: c.passed ? 'Зачтено' : 'Не зачтено',
          date: c.date
        }))" />
      </div>
    </UCard>

    <!-- Экзамены -->
    <UCard class="mt-6" v-if="Object.keys(studentCard.exams_by_semester).length">
      <template #header>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Экзамены</h3>
      </template>
      <div v-for="(exams, semester) in studentCard.exams_by_semester" :key="semester" class="mb-4">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-2">{{ semester }}</h4>
        <UTable :columns="examColumns" :data="exams.map((e: any) => ({
          discipline: e.discipline,
          grade: e.grade,
          date: e.date
        }))" />
      </div>
    </UCard>

    <div class="mt-6 flex gap-2">
      <UButton color="primary" @click="printCard">
        <UIcon name="i-heroicons-printer" class="w-5 h-5 mr-2" />
        Печать карточки
      </UButton>
    </div>
  </div>

  <div v-else class="py-8 text-center">
    <UIcon name="i-heroicons-circle-stack" class="w-16 h-16 mx-auto text-gray-400" />
    <p class="text-gray-500 mt-4">Загрузка...</p>
  </div>
</template>

<script setup lang="ts">
import type { StudentCard } from '~/types/academic'

definePageMeta({ middleware: ['auth'] })

const route = useRoute()
const { getStudentCard } = useAcademic()
const studentCard = ref<StudentCard | null>(null)

const gradeColumns = [
  { key: 'discipline', label: 'Дисциплина', id: 'discipline' },
  { key: 'grade', label: 'Оценка', id: 'grade' },
  { key: 'type', label: 'Тип', id: 'type' },
  { key: 'date', label: 'Дата', id: 'date' }
]
const creditColumns = [
  { key: 'discipline', label: 'Дисциплина', id: 'discipline' },
  { key: 'passed', label: 'Статус', id: 'passed' },
  { key: 'date', label: 'Дата', id: 'date' }
]
const examColumns = [
  { key: 'discipline', label: 'Дисциплина', id: 'discipline' },
  { key: 'grade', label: 'Оценка', id: 'grade' },
  { key: 'date', label: 'Дата', id: 'date' }
]

const loadCard = async () => {
  try {
    studentCard.value = await getStudentCard(Number(route.params.id))
  } catch (e: any) {
    console.error(e)
  }
}

const printCard = () => {
  window.open(`/api/v1/analytics/student/${route.params.id}/card/print`, '_blank')
}

onMounted(loadCard)
</script>
