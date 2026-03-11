<template>
  <div class="py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Учебные группы</h1>
      <UButton color="primary" @click="showCreateModal = true">
        <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
        Создать группу
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
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ editingItem ? 'Редактировать' : 'Создать группу' }}</h2>
        </template>
        <form @submit.prevent="onSubmit">
          <div><label class="block text-sm font-medium mb-1">Направление</label>
            <USelect v-model="formState.study_direction_id" :options="directionOptions" option-attribute="label" value-attribute="value" class="w-full" />
          </div>
          <div><label class="block text-sm font-medium mb-1">Курс</label>
            <USelect v-model="formState.course_id" :options="courseOptions" option-attribute="label" value-attribute="value" class="w-full" />
          </div>
          <div><label class="block text-sm font-medium mb-1">Название</label>
            <UInput v-model="formState.name" class="w-full" placeholder="ИВТ-101" />
          </div>
          <div><label class="block text-sm font-medium mb-1">Год набора</label>
            <UInput v-model="formState.year" type="number" class="w-full" />
          </div>
          <div><label class="block text-sm font-medium mb-1">Описание</label>
            <UTextarea v-model="formState.description" class="w-full" />
          </div>
          <div class="flex gap-2 justify-end mt-4">
            <UButton color="neutral" variant="ghost" @click="showCreateModal = false">Отмена</UButton>
            <UButton type="submit" color="primary" :loading="isSubmitting">{{ editingItem ? 'Сохранить' : 'Создать' }}</UButton>
          </div>
        </form>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { StudyGroup } from '~/types/university'

definePageMeta({ middleware: ['auth'] })

const { getStudyGroups, createStudyGroup, updateStudyGroup, deleteStudyGroup } = useUniversity()
const { getStudyDirections, getCourses } = useUniversity()
const toast = useToast()

const columns = [{ key: 'name', label: 'Название', id: 'name' }, { key: 'year', label: 'Год набора', id: 'year' }, { key: 'actions', label: 'Действия', id: 'actions' }]
const items = ref<StudyGroup[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showCreateModal = ref(false)
const editingItem = ref<StudyGroup | null>(null)
const directionOptions = ref<any[]>([])
const courseOptions = ref<any[]>([])

const schema = v.object({
  study_direction_id: v.pipe(v.string(), v.minLength(1, 'Выберите направление')),
  course_id: v.pipe(v.string(), v.minLength(1, 'Выберите курс')),
  name: v.pipe(v.string(), v.minLength(1, 'Введите название')),
  year: v.pipe(v.string(), v.minLength(1, 'Введите год')),
  description: v.optional(v.string()),
})

const formState = reactive({ study_direction_id: '', course_id: '', name: '', year: '', description: '' })

const loadItems = async () => {
  isLoading.value = true
  try {
    const [groups, directions, courses] = await Promise.all([getStudyGroups(), getStudyDirections(), getCourses()])
    items.value = groups.items
    directionOptions.value = directions.items.map((d: any) => ({ value: d.id, label: `${d.code} - ${d.name}` }))
    courseOptions.value = courses.items.map((c: any) => ({ value: c.id, label: `${c.number} курс` }))
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isLoading.value = false }
}

const editItem = (item: StudyGroup) => {
  editingItem.value = item
  formState.study_direction_id = String(item.study_direction_id)
  formState.course_id = String(item.course_id)
  formState.name = item.name
  formState.year = String(item.year)
  formState.description = item.description || ''
  showCreateModal.value = true
}

const deleteItem = async (item: StudyGroup) => {
  if (!confirm(`Удалить группу "${item.name}"?`)) return
  try { await deleteStudyGroup(item.id); await loadItems() }
  catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    const data = { ...formState, study_direction_id: Number(formState.study_direction_id), course_id: Number(formState.course_id), year: Number(formState.year) }
    if (editingItem.value) await updateStudyGroup(editingItem.value.id, data)
    else await createStudyGroup(data)
    showCreateModal.value = false
    editingItem.value = null
    Object.keys(formState).forEach(k => formState[k] = '')
    await loadItems()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isSubmitting.value = false }
}

onMounted(loadItems)
</script>
