<template>
  <div class="py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Факультеты</h1>
      <UButton color="primary" @click="showCreateModal = true">
        <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
        Создать факультет
      </UButton>
    </div>

    <!-- Таблица факультетов -->
    <UCard>
      <UTable
        :columns="columns"
        :rows="faculties"
        :loading="isLoading"
        @select="onRowSelect"
      >
        <template #actions-data="{ row }">
          <div class="flex gap-2">
            <UButton
              color="neutral"
              variant="ghost"
              size="sm"
              icon="i-heroicons-pencil"
              @click="editFaculty(row)"
            />
            <UButton
              color="error"
              variant="ghost"
              size="sm"
              icon="i-heroicons-trash"
              @click="deleteFaculty(row)"
            />
          </div>
        </template>
      </UTable>

      <!-- Пагинация -->
      <div class="flex justify-between items-center mt-4">
        <span class="text-sm text-gray-500">
          Всего: {{ pagination.total }}
        </span>
        <UPagination
          v-model="pagination.page"
          :total="pagination.total"
          :page-size="pagination.size"
          @update:model-value="loadFaculties"
        />
      </div>
    </UCard>

    <!-- Модалка создания/редактирования -->
    <UModal v-model:open="showCreateModal">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">
            {{ editingFaculty ? 'Редактировать факультет' : 'Создать факультет' }}
          </h2>
        </template>

        <UForm :schema="schema" :state="formState" @submit="onSubmit">
          <UFormField label="Название" name="name">
            <UInput v-model="formState.name" class="w-full" />
          </UFormField>

          <UFormField label="Краткое название" name="short_name">
            <UInput v-model="formState.short_name" class="w-full" />
          </UFormField>

          <UFormField label="Описание" name="description">
            <UTextarea v-model="formState.description" class="w-full" />
          </UFormField>

          <div class="flex gap-2 justify-end mt-4">
            <UButton color="neutral" variant="ghost" @click="showCreateModal = false">
              Отмена
            </UButton>
            <UButton type="submit" color="primary" :loading="isSubmitting">
              {{ editingFaculty ? 'Сохранить' : 'Создать' }}
            </UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { Faculty, FacultyCreate } from '~/types/university'
import { RoutePaths } from '~/types/routes'

definePageMeta({
  middleware: ['auth'],
})

const { getFaculties, createFaculty, updateFaculty, deleteFaculty: deleteFacultyApi } = useUniversity()
const toast = useToast()

const columns = [
  { key: 'name', label: 'Название' },
  { key: 'short_name', label: 'Краткое название' },
  { key: 'description', label: 'Описание' },
  { key: 'actions', label: 'Действия' },
]

const faculties = ref<Faculty[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showCreateModal = ref(false)
const editingFaculty = ref<Faculty | null>(null)

const pagination = reactive({
  page: 1,
  size: 50,
  total: 0,
})

const schema = v.object({
  name: v.pipe(v.string(), v.minLength(1, 'Введите название')),
  short_name: v.pipe(v.string(), v.minLength(1, 'Введите краткое название')),
  description: v.optional(v.string()),
})

const formState = reactive({
  name: '',
  short_name: '',
  description: '',
})

const loadFaculties = async () => {
  isLoading.value = true
  try {
    const response = await getFaculties(pagination.page, pagination.size)
    faculties.value = response.items
    pagination.total = response.total
  } catch (error: any) {
    toast.add({
      title: 'Ошибка',
      description: error.data?.detail || 'Не удалось загрузить факультеты',
      color: 'error',
    })
  } finally {
    isLoading.value = false
  }
}

const onRowSelect = (row: Faculty) => {
  // Можно добавить просмотр деталей
}

const editFaculty = (faculty: Faculty) => {
  editingFaculty.value = faculty
  formState.name = faculty.name
  formState.short_name = faculty.short_name
  formState.description = faculty.description || ''
  showCreateModal.value = true
}

const deleteFaculty = async (faculty: Faculty) => {
  if (!confirm(`Удалить факультет "${faculty.name}"?`)) return
  
  try {
    await deleteFacultyApi(faculty.id)
    await loadFaculties()
  } catch (error: any) {
    toast.add({
      title: 'Ошибка',
      description: error.data?.detail || 'Не удалось удалить факультет',
      color: 'error',
    })
  }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    if (editingFaculty.value) {
      await updateFaculty(editingFaculty.value.id, formState)
    } else {
      await createFaculty(formState)
    }
    showCreateModal.value = false
    resetForm()
    await loadFaculties()
  } catch (error: any) {
    toast.add({
      title: 'Ошибка',
      description: error.data?.detail || 'Ошибка при сохранении',
      color: 'error',
    })
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  editingFaculty.value = null
  formState.name = ''
  formState.short_name = ''
  formState.description = ''
}

onMounted(() => {
  loadFaculties()
})
</script>
