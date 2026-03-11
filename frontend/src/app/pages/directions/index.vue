<template>
  <div class="py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Направления обучения</h1>
      <UButton color="primary" @click="showCreateModal = true">
        <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
        Создать направление
      </UButton>
    </div>

    <UCard>
      <UTable :columns="columns" :rows="items" :loading="isLoading">
        <template #actions-data="{ row }">
          <div class="flex gap-2">
            <UButton color="neutral" variant="ghost" size="sm" icon="i-heroicons-pencil" @click="editItem(row)" />
            <UButton color="error" variant="ghost" size="sm" icon="i-heroicons-trash" @click="deleteItem(row)" />
          </div>
        </template>
      </UTable>
    </UCard>

    <UModal v-model:open="showCreateModal">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ editingItem ? 'Редактировать' : 'Создать' }}</h2>
        </template>
        <UForm :schema="schema" :state="formState" @submit="onSubmit">
          <UFormField label="Факультет" name="faculty_id">
            <USelect v-model="formState.faculty_id" :options="facultyOptions" option-attribute="label" value-attribute="value" class="w-full" />
          </UFormField>
          <UFormField label="Название" name="name">
            <UInput v-model="formState.name" class="w-full" />
          </UFormField>
          <UFormField label="Код" name="code">
            <UInput v-model="formState.code" class="w-full" placeholder="09.03.01" />
          </UFormField>
          <UFormField label="Уровень" name="level">
            <USelect v-model="formState.level" :options="['Бакалавриат', 'Магистратура', 'Специалитет']" class="w-full" />
          </UFormField>
          <UFormField label="Описание" name="description">
            <UTextarea v-model="formState.description" class="w-full" />
          </UFormField>
          <div class="flex gap-2 justify-end mt-4">
            <UButton color="neutral" variant="ghost" @click="showCreateModal = false">Отмена</UButton>
            <UButton type="submit" color="primary" :loading="isSubmitting">{{ editingItem ? 'Сохранить' : 'Создать' }}</UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { StudyDirection } from '~/types/university'

definePageMeta({ middleware: ['auth'] })

const { getStudyDirections, createStudyDirection, updateStudyDirection, deleteStudyDirection } = useUniversity()
const { getFaculties } = useUniversity()
const toast = useToast()

const columns = [{ key: 'name', label: 'Название' }, { key: 'code', label: 'Код' }, { key: 'level', label: 'Уровень' }, { key: 'actions', label: 'Действия' }]
const items = ref<StudyDirection[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showCreateModal = ref(false)
const editingItem = ref<StudyDirection | null>(null)
const facultyOptions = ref<any[]>([])

const schema = v.object({
  faculty_id: v.pipe(v.string(), v.minLength(1, 'Выберите факультет')),
  name: v.pipe(v.string(), v.minLength(1, 'Введите название')),
  code: v.pipe(v.string(), v.minLength(1, 'Введите код')),
  level: v.pipe(v.string(), v.minLength(1, 'Выберите уровень')),
  description: v.optional(v.string()),
})

const formState = reactive({ faculty_id: '', name: '', code: '', level: 'Бакалавриат', description: '' })

const loadItems = async () => {
  isLoading.value = true
  try {
    const res = await getStudyDirections()
    items.value = res.items
    const faculties = await getFaculties()
    facultyOptions.value = faculties.items.map((f: any) => ({ value: f.id, label: f.name }))
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isLoading.value = false }
}

const editItem = (item: StudyDirection) => {
  editingItem.value = item
  formState.faculty_id = String(item.faculty_id)
  formState.name = item.name
  formState.code = item.code
  formState.level = item.level
  formState.description = item.description || ''
  showCreateModal.value = true
}

const deleteItem = async (item: StudyDirection) => {
  if (!confirm(`Удалить "${item.name}"?`)) return
  try { await deleteStudyDirection(item.id); await loadItems() }
  catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    const data = { ...formState, faculty_id: Number(formState.faculty_id) }
    if (editingItem.value) await updateStudyDirection(editingItem.value.id, data)
    else await createStudyDirection(data)
    showCreateModal.value = false
    editingItem.value = null
    formState.faculty_id = ''; formState.name = ''; formState.code = ''; formState.level = 'Бакалавриат'; formState.description = ''
    await loadItems()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isSubmitting.value = false }
}

onMounted(loadItems)
</script>
