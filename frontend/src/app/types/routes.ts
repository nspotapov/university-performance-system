export const RoutePaths = {
  Main: '/',
  
  Auth: {
    Login: '/auth/login',
    MfaRequired: '/auth/mfa-required',
  },
  
  Profile: {
    Settings: '/profile/settings',
    Security: '/profile/security',
  },
  
  // University structure
  Faculties: {
    List: '/faculties',
    Create: '/faculties/create',
    Edit: (id: number) => `/faculties/${id}`,
    View: (id: number) => `/faculties/${id}/view`,
  },
  
  Departments: {
    List: '/departments',
    Create: '/departments/create',
    Edit: (id: number) => `/departments/${id}`,
    View: (id: number) => `/departments/${id}/view`,
  },
  
  Directions: {
    List: '/directions',
    Create: '/directions/create',
    Edit: (id: number) => `/directions/${id}`,
    View: (id: number) => `/directions/${id}/view`,
  },
  
  Disciplines: {
    List: '/disciplines',
    Create: '/disciplines/create',
    Edit: (id: number) => `/disciplines/${id}`,
  },
  
  Curricula: {
    List: '/curricula',
    Create: '/curricula/create',
    Edit: (id: number) => `/curricula/${id}`,
  },
  
  Courses: {
    List: '/courses',
    Create: '/courses/create',
    Edit: (id: number) => `/courses/${id}`,
  },
  
  Semesters: {
    List: '/semesters',
    Create: '/semesters/create',
    Edit: (id: number) => `/semesters/${id}`,
  },
  
  Groups: {
    List: '/groups',
    Create: '/groups/create',
    Edit: (id: number) => `/groups/${id}`,
    View: (id: number) => `/groups/${id}`,
  },
  
  // Students & Teachers
  Students: {
    List: '/students',
    Create: '/students/create',
    Edit: (id: number) => `/students/${id}`,
    View: (id: number) => `/students/${id}`,
    Card: (id: number) => `/students/${id}/card`,
  },
  
  Teachers: {
    List: '/teachers',
    Create: '/teachers/create',
    Edit: (id: number) => `/teachers/${id}`,
    View: (id: number) => `/teachers/${id}`,
  },
  
  // Grade management
  Gradebooks: {
    List: '/gradebooks',
    Create: '/gradebooks/create',
    Edit: (id: number) => `/gradebooks/${id}`,
    View: (id: number) => `/gradebooks/${id}/grades`,
  },
  
  Grades: {
    List: '/grades',
    Create: '/grades/create',
    Edit: (id: number) => `/grades/${id}`,
  },
  
  Credits: {
    List: '/credits',
    Create: '/credits/create',
  },
  
  Exams: {
    List: '/exams',
    Create: '/exams/create',
  },
  
  // Analytics
  Analytics: {
    Dashboard: '/analytics',
    Faculty: (id: number) => `/analytics/faculty/${id}`,
    Direction: (id: number) => `/analytics/direction/${id}`,
    Course: (id: number) => `/analytics/course/${id}`,
    Group: (id: number) => `/analytics/group/${id}`,
  },
} as const

export type RoutePath = typeof RoutePaths
