<template>
  <div class="py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Преподаватели</h1>
      <UButton color="primary" @click="showCreateModal = true">
        <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
        Добавить преподавателя
      </UButton>
    </div>

    <UCard>
      <UTable :columns="columns" :data="teachers" :loading="isLoading">
        <template #full_name-data="{ row }">
          {{ row.last_name }} {{ row.first_name }} {{ row.middle_name || '' }}
        </template>
        <template #actions-cell="{ row }">
          <div class="flex gap-2">
            <UButton color="neutral" variant="ghost" size="sm" icon="i-heroicons-pencil" @click="editTeacher(row.original)" />
            <UButton color="error" variant="ghost" size="sm" icon="i-heroicons-trash" @click="deleteTeacher(row.original)" />
          </div>
        </template>
      </UTable>
    </UCard>

    <UModal v-model:open="showCreateModal">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ editingTeacher ? 'Редактировать' : 'Добавить преподавателя' }}</h2>
        </template>
        <UForm :schema="schema" :state="formState" @submit="onSubmit">
          <UFormField label="Email" name="user_email">
            <UInput v-model="formState.user_email" type="email" class="w-full" />
          </UFormField>
          <UFormField label="Пароль" name="password" v-if="!editingTeacher">
            <UInput v-model="formState.password" type="password" class="w-full" />
          </UFormField>
          <UFormField label="Кафедра" name="department_id">
            <USelect v-model="formState.department_id" :options="departmentOptions" option-attribute="label" value-attribute="value" class="w-full" />
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
          <UFormField label="Должность" name="position">
            <UInput v-model="formState.position" class="w-full" placeholder="Доцент" />
          </UFormField>
          <UFormField label="Ученая степень" name="academic_degree">
            <UInput v-model="formState.academic_degree" class="w-full" placeholder="Кандидат наук" />
          </UFormField>
          <UFormField label="Ученое звание" name="academic_title">
            <UInput v-model="formState.academic_title" class="w-full" placeholder="Доцент" />
          </UFormField>
          <UFormField label="Дата приема" name="hire_date">
            <UInput v-model="formState.hire_date" type="date" class="w-full" />
          </UFormField>
          <div class="flex gap-2 justify-end mt-4">
            <UButton color="neutral" variant="ghost" @click="showCreateModal = false">Отмена</UButton>
            <UButton type="submit" color="primary" :loading="isSubmitting">{{ editingTeacher ? 'Сохранить' : 'Добавить' }}</UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { Teacher } from '~/types/academic'

definePageMeta({ middleware: ['auth'] })

const { getTeachers, createTeacher, updateTeacher, deleteTeacher: deleteApi } = useAcademic()
const { getDepartments } = useUniversity()
const toast = useToast()

const columns = [
  { key: 'full_name', label: 'ФИО' },
  { key: 'position', label: 'Должность' },
  { key: 'academic_degree', label: 'Степень' },
  { key: 'actions', label: 'Действия' },
]

const teachers = ref<Teacher[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showCreateModal = ref(false)
const editingTeacher = ref<Teacher | null>(null)
const departmentOptions = ref<any[]>([])

const schema = v.object({
  user_email: v.pipe(v.string(), v.minLength(1, 'Введите email'), v.email()),
  password: v.optional(v.string()),
  department_id: v.pipe(v.string(), v.minLength(1, 'Выберите кафедру')),
  last_name: v.pipe(v.string(), v.minLength(1, 'Введите фамилию')),
  first_name: v.pipe(v.string(), v.minLength(1, 'Введите имя')),
  middle_name: v.optional(v.string()),
  position: v.pipe(v.string(), v.minLength(1, 'Введите должность')),
  academic_degree: v.optional(v.string()),
  academic_title: v.optional(v.string()),
  hire_date: v.pipe(v.string(), v.minLength(1, 'Выберите дату')),
})

const formState = reactive({
  user_email: '', password: '', department_id: '', last_name: '', first_name: '', middle_name: '', position: '', academic_degree: '', academic_title: '', hire_date: '',
})

const loadTeachers = async () => {
  isLoading.value = true
  try {
    const [teachersRes, deptsRes] = await Promise.all([getTeachers(), getDepartments()])
    teachers.value = teachersRes.items
    departmentOptions.value = deptsRes.items.map((d: any) => ({ value: d.id, label: d.name }))
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' })
  } finally { isLoading.value = false }
}

const editTeacher = (teacher: Teacher) => {
  editingTeacher.value = teacher
  formState.user_email = ''
  formState.department_id = String(teacher.department_id)
  formState.last_name = teacher.last_name
  formState.first_name = teacher.first_name
  formState.middle_name = teacher.middle_name || ''
  formState.position = teacher.position
  formState.academic_degree = teacher.academic_degree || ''
  formState.academic_title = teacher.academic_title || ''
  formState.hire_date = teacher.hire_date
  showCreateModal.value = true
}

const deleteTeacher = async (teacher: Teacher) => {
  if (!confirm(`Удалить "${teacher.last_name} ${teacher.first_name}"?`)) return
  try { await deleteApi(teacher.id); await loadTeachers() }
  catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    const data: any = {
      department_id: Number(formState.department_id),
      last_name: formState.last_name,
      first_name: formState.first_name,
      middle_name: formState.middle_name,
      position: formState.position,
      academic_degree: formState.academic_degree,
      academic_title: formState.academic_title,
      hire_date: formState.hire_date,
    }
    if (editingTeacher.value) {
      await updateTeacher(editingTeacher.value.id, data)
    } else {
      toast.add({ title: 'Инфо', description: 'Создание требует создания пользователя', color: 'warning' })
    }
    showCreateModal.value = false
    editingTeacher.value = null
    Object.keys(formState).forEach(k => formState[k] = '')
    await loadTeachers()
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' })
  } finally { isSubmitting.value = false }
}

onMounted(loadTeachers)
</script>
