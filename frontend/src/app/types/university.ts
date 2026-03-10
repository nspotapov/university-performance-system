// Faculty
export interface Faculty {
  id: number
  name: string
  short_name: string
  description?: string
}

export interface FacultyCreate {
  name: string
  short_name: string
  description?: string
}

export interface FacultyUpdate extends Partial<FacultyCreate> {}

// Department
export interface Department {
  id: number
  faculty_id: number
  name: string
  short_name: string
  description?: string
}

export interface DepartmentCreate {
  faculty_id: number
  name: string
  short_name: string
  description?: string
}

export interface DepartmentUpdate extends Partial<DepartmentCreate> {}

// StudyDirection
export interface StudyDirection {
  id: number
  faculty_id: number
  name: string
  code: string
  level: string
  description?: string
}

export interface StudyDirectionCreate {
  faculty_id: number
  name: string
  code: string
  level: string
  description?: string
}

export interface StudyDirectionUpdate extends Partial<StudyDirectionCreate> {}

// Discipline
export interface Discipline {
  id: number
  study_direction_id: number
  department_id: number
  name: string
  code: string
  hours: number
  description?: string
}

export interface DisciplineCreate {
  study_direction_id: number
  department_id: number
  name: string
  code: string
  hours: number
  description?: string
}

export interface DisciplineUpdate extends Partial<DisciplineCreate> {}

// Curriculum
export interface Curriculum {
  id: number
  study_direction_id: number
  name: string
  year: number
  description?: string
}

export interface CurriculumCreate {
  study_direction_id: number
  name: string
  year: number
  description?: string
}

export interface CurriculumUpdate extends Partial<CurriculumCreate> {}

// Course
export interface Course {
  id: number
  number: number
  description?: string
}

export interface CourseCreate {
  number: number
  description?: string
}

export interface CourseUpdate extends Partial<CourseCreate> {}

// Semester
export interface Semester {
  id: number
  course_id: number
  number: number
  name: string
  start_date: string
  end_date: string
  is_active: boolean
}

export interface SemesterCreate {
  course_id: number
  number: number
  name: string
  start_date: string
  end_date: string
  is_active?: boolean
}

export interface SemesterUpdate extends Partial<SemesterCreate> {}

// StudyGroup
export interface StudyGroup {
  id: number
  study_direction_id: number
  course_id: number
  name: string
  year: number
  description?: string
}

export interface StudyGroupCreate {
  study_direction_id: number
  course_id: number
  name: string
  year: number
  description?: string
}

export interface StudyGroupUpdate extends Partial<StudyGroupCreate> {}

// Pagination
export interface Page<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}
