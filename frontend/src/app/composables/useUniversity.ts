import type {
  Faculty, FacultyCreate, FacultyUpdate,
  Department, DepartmentCreate, DepartmentUpdate,
  StudyDirection, StudyDirectionCreate, StudyDirectionUpdate,
  Page,
} from '~/types/university'

export const useUniversity = () => {
  const { $api } = useNuxtApp()
  const toast = useToast()

  // Faculties
  const getFaculties = async (page = 1, size = 50) => {
    return await $api<Page<Faculty>>('v1/faculties', {
      method: 'GET',
      query: { page, size },
    })
  }

  const getFaculty = async (id: number) => {
    return await $api<Faculty>(`v1/faculties/${id}`)
  }

  const createFaculty = async (data: FacultyCreate) => {
    const result = await $api<Faculty>('v1/faculties', {
      method: 'POST',
      body: data,
    })
    toast.add({ title: 'Успешно', description: 'Факультет создан', color: 'success' })
    return result
  }

  const updateFaculty = async (id: number, data: FacultyUpdate) => {
    const result = await $api<Faculty>(`v1/faculties/${id}`, {
      method: 'PATCH',
      body: data,
    })
    toast.add({ title: 'Успешно', description: 'Факультет обновлен', color: 'success' })
    return result
  }

  const deleteFaculty = async (id: number) => {
    await $api(`v1/faculties/${id}`, { method: 'DELETE' })
    toast.add({ title: 'Успешно', description: 'Факультет удален', color: 'success' })
  }

  // Departments
  const getDepartments = async (page = 1, size = 50, faculty_id?: number) => {
    return await $api<Page<Department>>('v1/departments', {
      method: 'GET',
      query: { page, size, faculty_id },
    })
  }

  const getDepartment = async (id: number) => {
    return await $api<Department>(`v1/departments/${id}`)
  }

  const createDepartment = async (data: DepartmentCreate) => {
    const result = await $api<Department>('v1/departments', {
      method: 'POST',
      body: data,
    })
    toast.add({ title: 'Успешно', description: 'Кафедра создана', color: 'success' })
    return result
  }

  const updateDepartment = async (id: number, data: DepartmentUpdate) => {
    const result = await $api<Department>(`v1/departments/${id}`, {
      method: 'PATCH',
      body: data,
    })
    toast.add({ title: 'Успешно', description: 'Кафедра обновлена', color: 'success' })
    return result
  }

  const deleteDepartment = async (id: number) => {
    await $api(`v1/departments/${id}`, { method: 'DELETE' })
    toast.add({ title: 'Успешно', description: 'Кафедра удалена', color: 'success' })
  }

  // Study Directions
  const getStudyDirections = async (page = 1, size = 50, faculty_id?: number) => {
    return await $api<Page<StudyDirection>>('v1/study-directions', {
      method: 'GET',
      query: { page, size, faculty_id },
    })
  }

  const getStudyDirection = async (id: number) => {
    return await $api<StudyDirection>(`v1/study-directions/${id}`)
  }

  const createStudyDirection = async (data: StudyDirectionCreate) => {
    const result = await $api<StudyDirection>('v1/study-directions', {
      method: 'POST',
      body: data,
    })
    toast.add({ title: 'Успешно', description: 'Направление создано', color: 'success' })
    return result
  }

  const updateStudyDirection = async (id: number, data: StudyDirectionUpdate) => {
    const result = await $api<StudyDirection>(`v1/study-directions/${id}`, {
      method: 'PATCH',
      body: data,
    })
    toast.add({ title: 'Успешно', description: 'Направление обновлено', color: 'success' })
    return result
  }

  const deleteStudyDirection = async (id: number) => {
    await $api(`v1/study-directions/${id}`, { method: 'DELETE' })
    toast.add({ title: 'Успешно', description: 'Направление удалено', color: 'success' })
  }

  return {
    // Faculties
    getFaculties,
    getFaculty,
    createFaculty,
    updateFaculty,
    deleteFaculty,
    // Departments
    getDepartments,
    getDepartment,
    createDepartment,
    updateDepartment,
    deleteDepartment,
    // Study Directions
    getStudyDirections,
    getStudyDirection,
    createStudyDirection,
    updateStudyDirection,
    deleteStudyDirection,
  }
}
