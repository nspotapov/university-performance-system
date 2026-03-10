// Roles
export enum UserRole {
  ADMIN = 'ADMIN',
  RECTOR = 'RECTOR',
  DEAN = 'DEAN',
  HEAD_TEACHER = 'HEAD_TEACHER',
  TEACHER = 'TEACHER',
  STUDENT = 'STUDENT',
}

// MFA Methods
export enum MFAMethod {
  OTP = 'OTP',
  TOTP = 'TOTP',
}

// User
export interface User {
  id: number
  email: string
  role: UserRole
  is_active: boolean
  is_mfa_enabled: boolean
  mfa_method: MFAMethod
}

// Login
export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  mfa_required: boolean
  mfa_method?: MFAMethod
  message?: string
}

// MFA Status
export interface MfaStatus {
  is_enabled: boolean
  method?: MFAMethod
  is_required: boolean
}

// TOTP Setup
export interface TotpSetupResponse {
  secret: string
  qr_code_uri: string
  message: string
}

// Verify Code
export interface VerifyCodeRequest {
  code: string
}

export interface VerifyCodeResponse {
  access_token: string
  token_type: string
  expires_in: number
}

// OTP Send
export interface OtpSendResponse {
  message: string
  expires_in: number
}

// Refresh Token
export interface RefreshTokenResponse {
  access_token: string
  token_type: string
  expires_in: number
}

// Auth Config
export const AuthConfig = {
  AccessTokenCookieName: 'access_token',
  RefreshTokenCookieName: 'refresh_token',
  MfaTokenCookieName: 'mfa_token',
} as const

// Role permissions
export const RolePermissions = {
  [UserRole.ADMIN]: ['all'],
  [UserRole.RECTOR]: ['analytics', 'faculties', 'departments', 'users'],
  [UserRole.DEAN]: ['analytics', 'faculties', 'departments', 'directions', 'students', 'teachers'],
  [UserRole.HEAD_TEACHER]: ['analytics', 'department', 'teachers', 'disciplines', 'gradebooks'],
  [UserRole.TEACHER]: ['analytics', 'gradebooks', 'grades', 'students'],
  [UserRole.STUDENT]: ['analytics', 'grades', 'card'],
} as const

export type Permission = typeof RolePermissions[UserRole][number]
