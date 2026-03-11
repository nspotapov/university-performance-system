import type {
  Student, StudentCreate, StudentUpdate,
  Teacher, TeacherCreate, TeacherUpdate,
  GradeBook, GradeBookCreate,
  Grade, GradeCreate,
  PerformanceStats, StudentCard,
} from '~/types/academic'
import type { Page } from '~/types/university'

export const useAcademic = () => {
  const { $api } = useNuxtApp()
  const toast = useToast()

  // Faculties (from university)
  const getFaculties = async (page = 1, size = 50) => {
    return await $api<Page<any>>('v1/faculties', { method: 'GET', query: { page, size } })
  }

  const getStudyDirections = async (page = 1, size = 50) => {
    return await $api<Page<any>>('v1/study-directions', { method: 'GET', query: { page, size } })
  }

  const getCourses = async (page = 1, size = 50) => {
    return await $api<Page<any>>('v1/courses', { method: 'GET', query: { page, size } })
  }

  // Students
  const getStudents = async (page = 1, size = 50) => {
    return await $api<Page<Student>>('v1/students', { method: 'GET', query: { page, size } })
  }

  const getStudent = async (id: number) => {
    return await $api<Student>(`v1/students/${id}`)
  }

  const createStudent = async (data: StudentCreate) => {
    const result = await $api<Student>('v1/students', { method: 'POST', body: data })
    toast.add({ title: 'Успешно', description: 'Студент создан', color: 'success' })
    return result
  }

  const updateStudent = async (id: number, data: StudentUpdate) => {
    const result = await $api<Student>(`v1/students/${id}`, { method: 'PATCH', body: data })
    toast.add({ title: 'Успешно', description: 'Студент обновлен', color: 'success' })
    return result
  }

  const deleteStudent = async (id: number) => {
    await $api(`v1/students/${id}`, { method: 'DELETE' })
    toast.add({ title: 'Успешно', description: 'Студент удален', color: 'success' })
  }

  const getStudentCard = async (id: number) => {
    return await $api<StudentCard>(`v1/analytics/student/${id}/card`)
  }

  // Teachers
  const getTeachers = async (page = 1, size = 50, department_id?: number) => {
    return await $api<Page<Teacher>>('v1/teachers', { 
      method: 'GET', 
      query: { page, size, department_id } 
    })
  }

  const getTeacher = async (id: number) => {
    return await $api<Teacher>(`v1/teachers/${id}`)
  }

  const createTeacher = async (data: TeacherCreate) => {
    const result = await $api<Teacher>('v1/teachers', { method: 'POST', body: data })
    toast.add({ title: 'Успешно', description: 'Преподаватель создан', color: 'success' })
    return result
  }

  const updateTeacher = async (id: number, data: TeacherUpdate) => {
    const result = await $api<Teacher>(`v1/teachers/${id}`, { method: 'PATCH', body: data })
    toast.add({ title: 'Успешно', description: 'Преподаватель обновлен', color: 'success' })
    return result
  }

  const deleteTeacher = async (id: number) => {
    await $api(`v1/teachers/${id}`, { method: 'DELETE' })
    toast.add({ title: 'Успешно', description: 'Преподаватель удален', color: 'success' })
  }

  // GradeBooks
  const getGradeBooks = async (page = 1, size = 50, filters?: any) => {
    return await $api<Page<GradeBook>>('v1/gradebooks', { method: 'GET', query: { page, size, ...filters } })
  }

  const createGradeBook = async (data: GradeBookCreate) => {
    const result = await $api<GradeBook>('v1/gradebooks', { method: 'POST', body: data })
    toast.add({ title: 'Успешно', description: 'Ведомость создана', color: 'success' })
    return result
  }

  const updateGradeBook = async (id: number, data: any) => {
    const result = await $api<GradeBook>(`v1/gradebooks/${id}`, { method: 'PATCH', body: data })
    toast.add({ title: 'Успешно', description: 'Ведомость обновлена', color: 'success' })
    return result
  }

  const deleteGradeBook = async (id: number) => {
    await $api(`v1/gradebooks/${id}`, { method: 'DELETE' })
    toast.add({ title: 'Успешно', description: 'Ведомость удалена', color: 'success' })
  }

  // Grades
  const getGrades = async (gradebook_id: number) => {
    return await $api<Page<Grade>>('v1/grades', { method: 'GET', query: { gradebook_id } })
  }

  const createGrade = async (data: GradeCreate) => {
    const result = await $api<Grade>('v1/grades', { method: 'POST', body: data })
    toast.add({ title: 'Успешно', description: 'Оценка выставлена', color: 'success' })
    return result
  }

  const updateGrade = async (id: number, data: any) => {
    const result = await $api<Grade>(`v1/grades/${id}`, { method: 'PATCH', body: data })
    toast.add({ title: 'Успешно', description: 'Оценка обновлена', color: 'success' })
    return result
  }

  const deleteGrade = async (id: number) => {
    await $api(`v1/grades/${id}`, { method: 'DELETE' })
  }

  // Analytics
  const getFacultyPerformance = async (faculty_id: number, semester_id: number) => {
    return await $api<PerformanceStats>(`v1/analytics/performance/faculty/${faculty_id}`, {
      method: 'GET',
      query: { semester_id }
    })
  }

  const getGroupPerformance = async (group_id: number, semester_id: number) => {
    return await $api<PerformanceStats>(`v1/analytics/performance/group/${group_id}`, {
      method: 'GET',
      query: { semester_id }
    })
  }

  return {
    // Reference data
    getFaculties,
    getStudyDirections,
    getCourses,
    // Students
    getStudents,
    getStudent,
    createStudent,
    updateStudent,
    deleteStudent,
    getStudentCard,
    // Teachers
    getTeachers,
    getTeacher,
    createTeacher,
    updateTeacher,
    deleteTeacher,
    // GradeBooks
    getGradeBooks,
    createGradeBook,
    updateGradeBook,
    deleteGradeBook,
    // Grades
    getGrades,
    createGrade,
    updateGrade,
    deleteGrade,
    // Analytics
    getFacultyPerformance,
    getGroupPerformance,
  }
}
