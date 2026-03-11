<template>
  <div class="py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Студенты</h1>
      <UButton color="primary" @click="showCreateModal = true">
        <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
        Добавить студента
      </UButton>
    </div>

    <UCard>
      <UTable :columns="columns" :rows="students" :loading="isLoading">
        <template #full_name-data="{ row }">
          <NuxtLink :to="`/students/${row.id}`" class="text-primary hover:underline">
            {{ row.last_name }} {{ row.first_name }} {{ row.middle_name || '' }}
          </NuxtLink>
        </template>
        <template #actions-data="{ row }">
          <div class="flex gap-2">
            <UButton color="neutral" variant="ghost" size="sm" icon="i-heroicons-eye" @click="viewStudent(row)" />
            <UButton color="neutral" variant="ghost" size="sm" icon="i-heroicons-pencil" @click="editStudent(row)" />
            <UButton color="error" variant="ghost" size="sm" icon="i-heroicons-trash" @click="deleteStudent(row)" />
          </div>
        </template>
      </UTable>

      <div class="flex justify-between items-center mt-4">
        <span class="text-sm text-gray-500">Всего: {{ pagination.total }}</span>
        <UPagination v-model="pagination.page" :total="pagination.total" :page-size="pagination.size" @update:model-value="loadStudents" />
      </div>
    </UCard>

    <!-- Модалка создания/редактирования -->
    <UModal v-model:open="showCreateModal">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ editingStudent ? 'Редактировать' : 'Добавить студента' }}</h2>
        </template>
        <UForm :schema="schema" :state="formState" @submit="onSubmit">
          <UFormField label="Email" name="user_email">
            <UInput v-model="formState.user_email" type="email" class="w-full" placeholder="student@university.ru" />
          </UFormField>
          <UFormField label="Пароль" name="password" v-if="!editingStudent">
            <UInput v-model="formState.password" type="password" class="w-full" />
          </UFormField>
          <div class="grid grid-cols-3 gap-4">
            <UFormField label="Фамилия" name="last_name">
              <UInput v-model="formState.last_name" class="w-full" />
            </UFormField>
            <UFormField label="Имя" name="first_name">
              <UInput v-model="formState.first_name" class="w-full" />
            </UFormField>
            <UFormField label="Отчество" name="middle_name">
              <UInput v-model="formState.middle_name" class="w-full" />
            </UFormField>
          </div>
          <UFormField label="Дата рождения" name="birth_date">
            <UInput v-model="formState.birth_date" type="date" class="w-full" />
          </UFormField>
          <UFormField label="Год поступления" name="enrollment_year">
            <UInput v-model="formState.enrollment_year" type="number" class="w-full" />
          </UFormField>
          <div class="flex gap-2 justify-end mt-4">
            <UButton color="neutral" variant="ghost" @click="showCreateModal = false">Отмена</UButton>
            <UButton type="submit" color="primary" :loading="isSubmitting">{{ editingStudent ? 'Сохранить' : 'Добавить' }}</UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { Student } from '~/types/academic'
import { RoutePaths } from '~/types/routes'

definePageMeta({ middleware: ['auth'] })

const { getStudents, createStudent, updateStudent, deleteStudent: deleteApi } = useAcademic()
const toast = useToast()

const columns = [
  { key: 'full_name', label: 'ФИО' },
  { key: 'birth_date', label: 'Дата рождения' },
  { key: 'enrollment_year', label: 'Год поступления' },
  { key: 'actions', label: 'Действия' },
]

const students = ref<Student[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showCreateModal = ref(false)
const editingStudent = ref<Student | null>(null)

const pagination = reactive({ page: 1, size: 50, total: 0 })

const schema = v.object({
  user_email: v.pipe(v.string(), v.minLength(1, 'Введите email'), v.email()),
  password: v.optional(v.string()),
  last_name: v.pipe(v.string(), v.minLength(1, 'Введите фамилию')),
  first_name: v.pipe(v.string(), v.minLength(1, 'Введите имя')),
  middle_name: v.optional(v.string()),
  birth_date: v.pipe(v.string(), v.minLength(1, 'Выберите дату')),
  enrollment_year: v.pipe(v.string(), v.minLength(1, 'Введите год')),
})

const formState = reactive({
  user_email: '', password: '', last_name: '', first_name: '', middle_name: '', birth_date: '', enrollment_year: '',
})

const loadStudents = async () => {
  isLoading.value = true
  try {
    const res = await getStudents(pagination.page, pagination.size)
    students.value = res.items
    pagination.total = res.total
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' })
  } finally { isLoading.value = false }
}

const viewStudent = (student: Student) => {
  navigateTo(RoutePaths.Students.View(student.id))
}

const editStudent = (student: Student) => {
  editingStudent.value = student
  formState.user_email = '' // email получаем из user
  formState.last_name = student.last_name
  formState.first_name = student.first_name
  formState.middle_name = student.middle_name || ''
  formState.birth_date = student.birth_date
  formState.enrollment_year = String(student.enrollment_year)
  showCreateModal.value = true
}

const deleteStudent = async (student: Student) => {
  if (!confirm(`Удалить студента "${student.last_name} ${student.first_name}"?`)) return
  try { await deleteApi(student.id); await loadStudents() }
  catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    const data: any = {
      last_name: formState.last_name,
      first_name: formState.first_name,
      middle_name: formState.middle_name,
      birth_date: formState.birth_date,
      enrollment_year: Number(formState.enrollment_year),
    }
    if (editingStudent.value) {
      await updateStudent(editingStudent.value.id, data)
    } else {
      // Для создания нужен user_id - это требует отдельного API
      toast.add({ title: 'Инфо', description: 'Создание студента требует создания пользователя. Используйте API напрямую.', color: 'warning' })
    }
    showCreateModal.value = false
    editingStudent.value = null
    formState.user_email = ''; formState.password = ''; formState.last_name = ''; formState.first_name = ''; formState.middle_name = ''; formState.birth_date = ''; formState.enrollment_year = ''
    await loadStudents()
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' })
  } finally { isSubmitting.value = false }
}

onMounted(loadStudents)
</script>
