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
        :data="faculties"
        :loading="isLoading"
      >
        <template #actions-cell="{ row }">
          <div class="flex gap-2">
            <UButton
              color="neutral"
              variant="ghost"
              size="sm"
              icon="i-heroicons-pencil"
              @click="editFaculty(row.original)"
            />
            <UButton
              color="error"
              variant="ghost"
              size="sm"
              icon="i-heroicons-trash"
              @click="deleteFaculty(row.original)"
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
      <template #default="{ close }">
        <UCard>
          <template #header>
            <h2 class="text-xl font-bold">
              {{ editingFaculty ? 'Редактировать факультет' : 'Создать факультет' }}
            </h2>
          </template>

          <form @submit.prevent="onSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-1">Название</label>
              <UInput v-model="formState.name" class="w-full" />
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Краткое название</label>
              <UInput v-model="formState.short_name" class="w-full" />
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Описание</label>
              <UTextarea v-model="formState.description" class="w-full" />
            </div>

            <div class="flex gap-2 justify-end">
              <UButton color="neutral" variant="ghost" @click="close()">
                Отмена
              </UButton>
              <UButton type="submit" color="primary" :loading="isSubmitting">
                {{ editingFaculty ? 'Сохранить' : 'Создать' }}
              </UButton>
            </div>
          </form>
        </UCard>
      </template>
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
  { key: 'name', label: 'Название', id: 'name' },
  { key: 'short_name', label: 'Краткое название', id: 'short_name' },
  { key: 'description', label: 'Описание', id: 'description' },
  { key: 'actions', label: 'Действия', id: 'actions' },
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

const onRowSelect = () => {
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
