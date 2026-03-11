<template>
  <div class="py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Ведомости</h1>
      <UButton color="primary" @click="showCreateModal = true">
        <UIcon name="i-heroicons-plus" class="w-5 h-5 mr-2" />
        Создать ведомость
      </UButton>
    </div>

    <UCard>
      <UTable :columns="columns" :data="items" :loading="isLoading">
        <template #grade_type-data="{ row }">
          <UBadge :color="row.grade_type === 'EXAM' ? 'primary' : 'neutral'" :label="row.grade_type === 'EXAM' ? 'Экзамен' : 'Зачет'" />
        </template>
        <template #is_closed-data="{ row }">
          <UBadge :color="row.is_closed ? 'success' : 'warning'" :label="row.is_closed ? 'Закрыта' : 'Открыта'" />
        </template>
        <template #actions-cell="{ row }">
          <div class="flex gap-2">
            <UButton color="primary" variant="ghost" size="sm" icon="i-heroicons-list-bullet" @click="viewGrades(row.original)" />
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
import type { GradeBook } from '~/types/academic'
import { RoutePaths } from '~/types/routes'

definePageMeta({ middleware: ['auth'] })

const { getGradeBooks, createGradeBook, updateGradeBook, deleteGradeBook, getSemesters, getStudyGroups, getDisciplines, getTeachersList } = useAcademic()
const toast = useToast()

const columns = [{ key: 'name', label: 'Название', id: 'name' }, { key: 'grade_type', label: 'Тип', id: 'grade_type' }, { key: 'is_closed', label: 'Статус', id: 'is_closed' }, { key: 'actions', label: 'Действия', id: 'actions' }]
const items = ref<GradeBook[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const showCreateModal = ref(false)
const editingItem = ref<GradeBook | null>(null)
const semesterOptions = ref<any[]>([])
const groupOptions = ref<any[]>([])
const disciplineOptions = ref<any[]>([])
const teacherOptions = ref<any[]>([])

const schema = v.object({
  semester_id: v.pipe(v.string(), v.minLength(1, 'Выберите семестр')),
  study_group_id: v.pipe(v.string(), v.minLength(1, 'Выберите группу')),
  discipline_id: v.pipe(v.string(), v.minLength(1, 'Выберите дисциплину')),
  teacher_id: v.pipe(v.string(), v.minLength(1, 'Выберите преподавателя')),
  grade_type: v.pipe(v.string(), v.minLength(1, 'Выберите тип')),
  name: v.pipe(v.string(), v.minLength(1, 'Введите название')),
  created_at: v.pipe(v.string(), v.minLength(1, 'Выберите дату')),
})

const formState = reactive({ semester_id: '', study_group_id: '', discipline_id: '', teacher_id: '', grade_type: 'EXAM', name: '', created_at: '' })

const loadItems = async () => {
  isLoading.value = true
  try {
    const [gradebooks, semesters, groups, disciplines, teachers] = await Promise.all([
      getGradeBooks(), getSemesters(), getStudyGroups(), getDisciplines(), getTeachersList()
    ])
    items.value = gradebooks.items
    semesterOptions.value = semesters.items.map((s: any) => ({ value: s.id, label: s.name }))
    groupOptions.value = groups.items.map((g: any) => ({ value: g.id, label: g.name }))
    disciplineOptions.value = disciplines.items.map((d: any) => ({ value: d.id, label: d.name }))
    teacherOptions.value = teachers.items.map((t: any) => ({ value: t.id, label: `${t.last_name} ${t.first_name}` }))
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isLoading.value = false }
}

const viewGrades = (item: GradeBook) => {
  navigateTo(RoutePaths.Gradebooks.View(item.id))
}

const editItem = (item: GradeBook) => {
  editingItem.value = item
  formState.semester_id = String(item.semester_id)
  formState.study_group_id = String(item.study_group_id)
  formState.discipline_id = String(item.discipline_id)
  formState.teacher_id = String(item.teacher_id)
  formState.grade_type = item.grade_type
  formState.name = item.name
  formState.created_at = item.created_at
  showCreateModal.value = true
}

const deleteItem = async (item: GradeBook) => {
  if (!confirm(`Удалить ведомость "${item.name}"?`)) return
  try { await deleteGradeBook(item.id); await loadItems() }
  catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
}

const onSubmit = async () => {
  isSubmitting.value = true
  try {
    const data = { ...formState, semester_id: Number(formState.semester_id), study_group_id: Number(formState.study_group_id), discipline_id: Number(formState.discipline_id), teacher_id: Number(formState.teacher_id) }
    if (editingItem.value) await updateGradeBook(editingItem.value.id, data)
    else await createGradeBook(data)
    showCreateModal.value = false
    editingItem.value = null
    Object.keys(formState).forEach(k => formState[k] = k === 'grade_type' ? 'EXAM' : '')
    await loadItems()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isSubmitting.value = false }
}

onMounted(loadItems)
</script>
