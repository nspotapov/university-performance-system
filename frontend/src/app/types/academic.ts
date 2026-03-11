// Student
export interface Student {
  id: number
  user_id: number
  first_name: string
  last_name: string
  middle_name?: string
  birth_date: string
  enrollment_year: number
  is_expelled: boolean
  expulsion_reason?: string
  description?: string
}

export interface StudentCreate {
  user_id: number
  first_name: string
  last_name: string
  middle_name?: string
  birth_date: string
  enrollment_year: number
  is_expelled?: boolean
  expulsion_reason?: string
  description?: string
}

export interface StudentUpdate extends Partial<StudentCreate> {}

// Teacher
export interface Teacher {
  id: number
  user_id: number
  department_id: number
  first_name: string
  last_name: string
  middle_name?: string
  position: string
  academic_degree?: string
  academic_title?: string
  hire_date: string
  is_fired: boolean
  description?: string
}

export interface TeacherCreate {
  user_id: number
  department_id: number
  first_name: string
  last_name: string
  middle_name?: string
  position: string
  academic_degree?: string
  academic_title?: string
  hire_date: string
  is_fired?: boolean
  description?: string
}

export interface TeacherUpdate extends Partial<TeacherCreate> {}

// StudentGroup (link between student and study group)
export interface StudentGroupLink {
  id: number
  student_id: number
  study_group_id: number
  start_date: string
  end_date?: string
  is_current: boolean
}

export interface StudentGroupLinkCreate {
  student_id: number
  study_group_id: number
  start_date: string
  end_date?: string
  is_current?: boolean
}

export interface StudentGroupLinkUpdate extends Partial<StudentGroupLinkCreate> {}

// GradeBook
export interface GradeBook {
  id: number
  semester_id: number
  study_group_id: number
  discipline_id: number
  teacher_id: number
  grade_type: 'EXAM' | 'CREDIT' | 'COURSEWORK' | 'TEST'
  name: string
  created_at: string
  is_closed: boolean
}

export interface GradeBookCreate {
  semester_id: number
  study_group_id: number
  discipline_id: number
  teacher_id: number
  grade_type: 'EXAM' | 'CREDIT' | 'COURSEWORK' | 'TEST'
  name: string
  created_at: string
  is_closed?: boolean
}

export interface GradeBookUpdate extends Partial<GradeBookCreate> {}

// Grade
export interface Grade {
  id: number
  gradebook_id: number
  student_id: number
  grade_value: '5' | '4' | '3' | '2' | 'PASS' | 'FAIL'
  grade_date: string
  comment?: string
}

export interface GradeCreate {
  gradebook_id: number
  student_id: number
  grade_value: '5' | '4' | '3' | '2' | 'PASS' | 'FAIL'
  grade_date: string
  comment?: string
}

export interface GradeUpdate extends Partial<GradeCreate> {}

// Credit
export interface Credit {
  id: number
  student_id: number
  discipline_id: number
  semester_id: number
  teacher_id: number
  is_passed: boolean
  credit_date: string
  attempt_number: number
  comment?: string
}

export interface CreditCreate {
  student_id: number
  discipline_id: number
  semester_id: number
  teacher_id: number
  is_passed: boolean
  credit_date: string
  attempt_number?: number
  comment?: string
}

export interface CreditUpdate extends Partial<CreditCreate> {}

// Exam
export interface Exam {
  id: number
  student_id: number
  discipline_id: number
  semester_id: number
  teacher_id: number
  grade_value: '5' | '4' | '3' | '2'
  exam_date: string
  attempt_number: number
  comment?: string
}

export interface ExamCreate {
  student_id: number
  discipline_id: number
  semester_id: number
  teacher_id: number
  grade_value: '5' | '4' | '3' | '2'
  exam_date: string
  attempt_number?: number
  comment?: string
}

export interface ExamUpdate extends Partial<ExamCreate> {}

// Analytics
export interface PerformanceStats {
  total_students: number
  excellent: number
  good: number
  satisfactory: number
  unsatisfactory: number
  quality_percentage: number
  success_rate_percentage: number
}

export interface StudentCard {
  student: {
    id: number
    first_name: string
    last_name: string
    middle_name?: string
    birth_date: string
    enrollment_year: number
    is_expelled: boolean
  }
  study_group?: string
  grades_by_semester: Record<string, Array<{
    discipline: string
    grade: string
    type: string
    date: string
  }>>
  credits_by_semester: Record<string, Array<{
    discipline: string
    passed: boolean
    date: string
  }>>
  exams_by_semester: Record<string, Array<{
    discipline: string
    grade: string
    date: string
  }>>
}
