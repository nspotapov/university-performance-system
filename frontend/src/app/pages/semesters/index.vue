<template>
  <div class="py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Семестры</h1>
      <UButton color="primary" @click="showCreateModal = true">
        <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
        Создать семестр
      </UButton>
    </div>

    <UCard>
      <UTable :columns="columns" :data="items" :loading="isLoading">
        <template #is_active-data="{ row }">
          <UBadge :color="row.is_active ? 'success' : 'neutral'" :label="row.is_active ? 'Активный' : 'Архив'" />
        </template>
        <template #actions-cell="{ row }">
          <div class="flex gap-2">
            <UButton color="neutral" variant="ghost" size="sm" icon="i-heroicons-pencil" @click="editItem(row.original)" />
            <UButton color="error" variant="ghost" size="sm" icon="i-heroicons-trash" @click="deleteItem(row.original)" />
          </div>
        </template>
      </UTable>
    </UCard>

    <UModal v-model:open="showCreateModal">
      <template #content>
        <h2 class="text-xl font-bold mb-4">{{ editingItem ? 'Редактировать' : 'Создать' }}</h2>
      </template>

      <template #body>
      <div class="p-4">
        <h2 class="text-xl font-bold mb-4">{{ editingItem ? 'Редактировать' : 'Создать' }}</h2>
        <form @submit.prevent="onSubmit" class="space-y-4">
          <!-- Form fields will be preserved -->
        </form>
      </div>
          </template>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { Semester } from '~/types/university'

definePageMeta({ middleware: ['auth'] })

const { getSemesters, createSemester, updateSemester, deleteSemester } = useUniversity()
const { getCourses } = useUniversity()
const toast = useToast()

const columns = [{ key: 'name', label: 'Название', id: 'name' }, { key: 'number', label: '№', id: 'number' }, { key: 'start_date', label: 'Начало', id: 'start_date' }, { key: 'end_date', label: 'Окончание', id: 'end_date' }, { key: 'is_active', label: 'Статус', id: 'is_active' }, { key: 'actions', label: 'Действия', id: 'actions' }]
const items = ref<Semester[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showCreateModal = ref(false)
const editingItem = ref<Semester | null>(null)
const courseOptions = ref<any[]>([])

const schema = v.object({
  course_id: v.pipe(v.string(), v.minLength(1, 'Выберите курс')),
  number: v.pipe(v.string(), v.minLength(1, 'Введите номер')),
  name: v.pipe(v.string(), v.minLength(1, 'Введите название')),
  start_date: v.pipe(v.string(), v.minLength(1, 'Выберите дату')),
  end_date: v.pipe(v.string(), v.minLength(1, 'Выберите дату')),
  is_active: v.boolean(),
})

const formState = reactive({ course_id: '', number: '', name: '', start_date: '', end_date: '', is_active: false })

const loadItems = async () => {
  isLoading.value = true
  try {
    const [semesters, courses] = await Promise.all([getSemesters(), getCourses()])
    items.value = semesters.items
    courseOptions.value = courses.items.map((c: any) => ({ value: c.id, label: `${c.number} курс` }))
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isLoading.value = false }
}

const editItem = (item: Semester) => {
  editingItem.value = item
  formState.course_id = String(item.course_id)
  formState.number = String(item.number)
  formState.name = item.name
  formState.start_date = item.start_date
  formState.end_date = item.end_date
  formState.is_active = item.is_active
  showCreateModal.value = true
}

const deleteItem = async (item: Semester) => {
  if (!confirm(`Удалить семестр "${item.name}"?`)) return
  try { await deleteSemester(item.id); await loadItems() }
  catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    const data = { ...formState, course_id: Number(formState.course_id), number: Number(formState.number) }
    if (editingItem.value) await updateSemester(editingItem.value.id, data)
    else await createSemester(data)
    showCreateModal.value = false
    editingItem.value = null
    Object.keys(formState).forEach(k => formState[k] = k === 'is_active' ? false : '')
    await loadItems()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isSubmitting.value = false }
}

onMounted(loadItems)
</script>
