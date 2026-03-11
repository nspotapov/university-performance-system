<template>
  <div class="py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Дисциплины</h1>
      <UButton color="primary" @click="showCreateModal = true">
        <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
        Создать дисциплину
      </UButton>
    </div>

    <UCard>
      <UTable :columns="columns" :data="items" :loading="isLoading">
        <template #actions-cell="{ row }">
          <div class="flex gap-2">
            <UButton color="neutral" variant="ghost" size="sm" icon="i-heroicons-pencil" @click="editItem(row.original)" />
            <UButton color="error" variant="ghost" size="sm" icon="i-heroicons-trash" @click="deleteItem(row.original)" />
          </div>
        </template>
      </UTable>
    </UCard>

    <UModal v-model:open="showCreateModal">
      <div class="p-4">
        <h2 class="text-xl font-bold mb-4">{{ editingItem ? 'Редактировать' : 'Создать' }}</h2>
        <form @submit.prevent="onSubmit" class="space-y-4">
          <!-- Form fields will be preserved -->
        </form>
      </div>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { Discipline } from '~/types/university'

definePageMeta({ middleware: ['auth'] })

const { getDisciplines, createDiscipline, updateDiscipline, deleteDiscipline } = useAcademic()
const { getStudyDirections, getDepartments } = useAcademic()
const toast = useToast()

const columns = [{ key: 'name', label: 'Название', id: 'name' }, { key: 'code', label: 'Код', id: 'code' }, { key: 'hours', label: 'Часов', id: 'hours' }, { key: 'actions', label: 'Действия', id: 'actions' }]
const items = ref<Discipline[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showCreateModal = ref(false)
const editingItem = ref<Discipline | null>(null)
const directionOptions = ref<any[]>([])
const departmentOptions = ref<any[]>([])

const schema = v.object({
  study_direction_id: v.pipe(v.string(), v.minLength(1, 'Выберите направление')),
  department_id: v.pipe(v.string(), v.minLength(1, 'Выберите кафедру')),
  name: v.pipe(v.string(), v.minLength(1, 'Введите название')),
  code: v.pipe(v.string(), v.minLength(1, 'Введите код')),
  hours: v.pipe(v.string(), v.minLength(1, 'Введите часы')),
  description: v.optional(v.string()),
})

const formState = reactive({ study_direction_id: '', department_id: '', name: '', code: '', hours: '', description: '' })

const loadItems = async () => {
  isLoading.value = true
  try {
    const [disciplines, directions, depts] = await Promise.all([getDisciplines(), getStudyDirections(), getDepartments()])
    items.value = disciplines.items
    directionOptions.value = directions.items.map((d: any) => ({ value: d.id, label: `${d.code} - ${d.name}` }))
    departmentOptions.value = depts.items.map((d: any) => ({ value: d.id, label: d.name }))
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isLoading.value = false }
}

const editItem = (item: Discipline) => {
  editingItem.value = item
  formState.study_direction_id = String(item.study_direction_id)
  formState.department_id = String(item.department_id)
  formState.name = item.name
  formState.code = item.code
  formState.hours = String(item.hours)
  formState.description = item.description || ''
  showCreateModal.value = true
}

const deleteItem = async (item: Discipline) => {
  if (!confirm(`Удалить дисциплину "${item.name}"?`)) return
  try { await deleteDiscipline(item.id); await loadItems() }
  catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    const data = { ...formState, study_direction_id: Number(formState.study_direction_id), department_id: Number(formState.department_id), hours: Number(formState.hours) }
    if (editingItem.value) await updateDiscipline(editingItem.value.id, data)
    else await createDiscipline(data)
    showCreateModal.value = false
    editingItem.value = null
    Object.keys(formState).forEach(k => formState[k] = '')
    await loadItems()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isSubmitting.value = false }
}

onMounted(loadItems)
</script>
