<template>
  <div class="py-8" v-if="gradebook">
    <div class="mb-6">
      <UButton color="neutral" variant="ghost" @click="navigateTo('/gradebooks')" class="mb-4">
        <UIcon name="i-heroicons-arrow-left" class="w-5 h-5 mr-2" />
        Назад к ведомостям
      </UButton>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ gradebook.name }}</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        {{ gradebook.grade_type === 'EXAM' ? 'Экзамен' : 'Зачет' }} | {{ gradebook.is_closed ? 'Закрыта' : 'Открыта' }}
      </p>
    </div>

    <UCard>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Оценки</h2>
        <UButton color="primary" size="sm" @click="showAddModal = true" :disabled="gradebook.is_closed">
          <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
          Добавить оценку
        </UButton>
      </div>

      <UTable :columns="columns" :rows="grades" :loading="isLoading" />

      <div class="flex justify-between items-center mt-4">
        <span class="text-sm text-gray-500">Всего: {{ pagination.total }}</span>
        <UPagination v-model="pagination.page" :total="pagination.total" :page-size="pagination.size" @update:model-value="loadGrades" />
      </div>
    </UCard>

    <UModal v-model:open="showAddModal">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">Добавить оценку</h2>
        </template>
        <UForm :schema="schema" :state="formState" @submit="onSubmit">
          <UFormField label="Студент" name="student_id">
            <USelect v-model="formState.student_id" :options="studentOptions" option-attribute="label" value-attribute="value" class="w-full" />
          </UFormField>
          <UFormField label="Оценка" name="grade_value">
            <USelect v-model="formState.grade_value" :options="gradeOptions" option-attribute="label" value-attribute="value" class="w-full" />
          </UFormField>
          <UFormField label="Дата" name="grade_date">
            <UInput v-model="formState.grade_date" type="date" class="w-full" />
          </UFormField>
          <UFormField label="Комментарий" name="comment">
            <UTextarea v-model="formState.comment" class="w-full" />
          </UFormField>
          <div class="flex gap-2 justify-end mt-4">
            <UButton color="neutral" variant="ghost" @click="showAddModal = false">Отмена</UButton>
            <UButton type="submit" color="primary" :loading="isSubmitting">Добавить</UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { Grade, GradeBook } from '~/types/academic'

definePageMeta({ middleware: ['auth'] })

const route = useRoute()
const { getGradeBooks, getGrades, createGrade, getStudents } = useAcademic()
const toast = useToast()

const gradebook = ref<GradeBook | null>(null)
const grades = ref<Grade[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showAddModal = ref(false)
const studentOptions = ref<any[]>([])

const gradeOptions = [
  { value: '5', label: '5 (Отлично)' },
  { value: '4', label: '4 (Хорошо)' },
  { value: '3', label: '3 (Удовл.)' },
  { value: '2', label: '2 (Неуд.)' },
  { value: 'PASS', label: 'Зачтено' },
  { value: 'FAIL', label: 'Не зачтено' },
]

const columns = [{ key: 'student_id', label: 'Студент' }, { key: 'grade_value', label: 'Оценка' }, { key: 'grade_date', label: 'Дата' }, { key: 'comment', label: 'Комментарий' }]

const pagination = reactive({ page: 1, size: 50, total: 0 })

const schema = v.object({
  student_id: v.pipe(v.string(), v.minLength(1, 'Выберите студента')),
  grade_value: v.pipe(v.string(), v.minLength(1, 'Выберите оценку')),
  grade_date: v.pipe(v.string(), v.minLength(1, 'Выберите дату')),
  comment: v.optional(v.string()),
})

const formState = reactive({ student_id: '', grade_value: '5', grade_date: new Date().toISOString().split('T')[0], comment: '' })

const loadGradebook = async () => {
  try {
    const res = await getGradeBooks(1, 100)
    gradebook.value = res.items.find((g: GradeBook) => g.id === Number(route.params.id)) || null
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' })
  }
}

const loadGrades = async () => {
  isLoading.value = true
  try {
    const [gradesRes, studentsRes] = await Promise.all([
      getGrades(Number(route.params.id)),
      getStudents()
    ])
    grades.value = gradesRes.items.map((g: Grade) => ({
      ...g,
      student_id: studentsRes.items.find((s: any) => s.id === g.student_id)?.last_name + ' ' + s.first_name || g.student_id
    }))
    pagination.total = gradesRes.total
    studentOptions.value = studentsRes.items.map((s: any) => ({ value: s.id, label: `${s.last_name} ${s.first_name}` }))
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' })
  } finally { isLoading.value = false }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    await createGrade({ gradebook_id: Number(route.params.id), student_id: Number(formState.student_id), grade_value: formState.grade_value as any, grade_date: formState.grade_date, comment: formState.comment })
    showAddModal.value = false
    Object.keys(formState).forEach(k => formState[k] = k === 'grade_value' ? '5' : k === 'grade_date' ? new Date().toISOString().split('T')[0] : '')
    await loadGrades()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isSubmitting.value = false }
}

onMounted(() => { loadGradebook(); loadGrades() })
</script>
