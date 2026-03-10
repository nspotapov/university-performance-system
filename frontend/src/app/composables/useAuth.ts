import type {
  User,
  LoginRequest,
  LoginResponse,
  MfaStatus,
  TotpSetupResponse,
  VerifyCodeRequest,
  VerifyCodeResponse,
  RefreshTokenResponse,
  OtpSendResponse,
  UserRole,
} from '~/types/auth'
import { AuthConfig, RolePermissions } from '~/types/auth'
import { RoutePaths } from '~/types/routes'

export interface UseAuthReturn {
  user: Ref<User | null>
  isAuthenticated: Ref<boolean>
  isLoading: Ref<boolean>
  mfaToken: Ref<string | null>
  login: (data: LoginRequest) => Promise<LoginResponse>
  verifyTotp: (code: string) => Promise<VerifyCodeResponse>
  sendOtp: () => Promise<OtpSendResponse>
  verifyOtp: (code: string) => Promise<VerifyCodeResponse>
  logout: () => Promise<void>
  refresh: () => Promise<void>
  setupTotp: () => Promise<TotpSetupResponse>
  enableTotp: (code: string) => Promise<void>
  enableOtp: () => Promise<void>
  disableMfa: (password: string) => Promise<void>
  getMfaStatus: () => Promise<MfaStatus>
  getCurrentUser: () => Promise<User>
  hasPermission: (permission: string) => boolean
  hasRole: (roles: UserRole[]) => boolean
  fetchUser: () => Promise<void>
}

export const useAuth = (): UseAuthReturn => {
  const { $api } = useNuxtApp()
  const toast = useToast()
  
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(true)
  const mfaToken = ref<string | null>(null)
  
  // Token cookies
  const accessTokenCookie = useCookie(AuthConfig.AccessTokenCookieName, {
    maxAge: 60 * 15, // 15 minutes
    path: '/',
  })
  
  const mfaTokenCookie = useCookie(AuthConfig.MfaTokenCookieName, {
    maxAge: 60 * 5, // 5 minutes
    path: '/',
  })
  
  const hasPermission = (permission: string): boolean => {
    if (!user.value) return false
    if (user.value.role === UserRole.ADMIN) return true
    
    const permissions = RolePermissions[user.value.role] || []
    return permissions.includes('all') || permissions.includes(permission as any)
  }
  
  const hasRole = (roles: UserRole[]): boolean => {
    if (!user.value) return false
    return roles.includes(user.value.role)
  }
  
  const login = async (data: LoginRequest): Promise<LoginResponse> => {
    try {
      const response = await $api<LoginResponse>('v1/auth/login', {
        method: 'POST',
        body: data,
      })
      
      if (response.mfa_required) {
        mfaToken.value = response.access_token
        mfaTokenCookie.value = response.access_token
      } else {
        accessTokenCookie.value = response.access_token
        isAuthenticated.value = true
        await fetchUser()
      }
      
      return response
    } catch (error: any) {
      if (error.statusCode === 403 && error.data?.detail === 'Двухфакторная аутентификация обязательна для вашей роли') {
        navigateTo(RoutePaths.Auth.MfaRequired)
      }
      throw error
    }
  }
  
  const verifyTotp = async (code: string): Promise<VerifyCodeResponse> => {
    const response = await $api<VerifyCodeResponse>('v1/auth/mfa/totp/verify', {
      method: 'POST',
      body: { code },
      headers: {
        Authorization: `Bearer ${mfaToken.value}`,
      },
    })
    
    accessTokenCookie.value = response.access_token
    mfaToken.value = null
    mfaTokenCookie.value = null
    isAuthenticated.value = true
    await fetchUser()
    
    return response
  }
  
  const sendOtp = async (): Promise<OtpSendResponse> => {
    return await $api<OtpSendResponse>('v1/auth/mfa/otp/send', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${mfaToken.value}`,
      },
    })
  }
  
  const verifyOtp = async (code: string): Promise<VerifyCodeResponse> => {
    const response = await $api<VerifyCodeResponse>('v1/auth/mfa/otp/verify', {
      method: 'POST',
      body: { code },
      headers: {
        Authorization: `Bearer ${mfaToken.value}`,
      },
    })
    
    accessTokenCookie.value = response.access_token
    mfaToken.value = null
    mfaTokenCookie.value = null
    isAuthenticated.value = true
    await fetchUser()
    
    return response
  }
  
  const logout = async () => {
    try {
      await $api('v1/auth/logout', { method: 'POST' })
    } catch (e) {
      // Ignore errors
    }
    
    accessTokenCookie.value = null
    mfaTokenCookie.value = null
    mfaToken.value = null
    user.value = null
    isAuthenticated.value = false
    navigateTo(RoutePaths.Auth.Login)
  }
  
  const refresh = async () => {
    try {
      const response = await $api<RefreshTokenResponse>('v1/auth/refresh', {
        method: 'POST',
      })
      accessTokenCookie.value = response.access_token
    } catch (error) {
      await logout()
    }
  }
  
  const setupTotp = async (): Promise<TotpSetupResponse> => {
    return await $api<TotpSetupResponse>('v1/auth/mfa/totp/setup', {
      method: 'POST',
    })
  }
  
  const enableTotp = async (code: string): Promise<void> => {
    await $api('v1/auth/mfa/totp/enable', {
      method: 'POST',
      body: { code },
    })
    
    if (user.value) {
      user.value.is_mfa_enabled = true
      user.value.mfa_method = 'TOTP'
    }
    
    toast.add({
      title: 'Успешно',
      description: 'TOTP аутентификация включена',
      color: 'success',
    })
  }
  
  const enableOtp = async (): Promise<void> => {
    await $api('v1/auth/mfa/otp/enable', {
      method: 'POST',
    })
    
    if (user.value) {
      user.value.is_mfa_enabled = true
      user.value.mfa_method = 'OTP'
    }
    
    toast.add({
      title: 'Успешно',
      description: 'OTP аутентификация включена',
      color: 'success',
    })
  }
  
  const disableMfa = async (password: string): Promise<void> => {
    await $api('v1/auth/mfa/disable', {
      method: 'POST',
      body: { password },
    })
    
    if (user.value) {
      user.value.is_mfa_enabled = false
    }
    
    toast.add({
      title: 'Успешно',
      description: 'MFA аутентификация отключена',
      color: 'success',
    })
  }
  
  const getMfaStatus = async (): Promise<MfaStatus> => {
    return await $api<MfaStatus>('v1/auth/mfa/status')
  }
  
  const getCurrentUser = async (): Promise<User> => {
    return await $api<User>('v1/auth/me')
  }
  
  const fetchUser = async () => {
    try {
      user.value = await getCurrentUser()
      isAuthenticated.value = true
    } catch (error) {
      user.value = null
      isAuthenticated.value = false
    } finally {
      isLoading.value = false
    }
  }
  
  onMounted(async () => {
    if (accessTokenCookie.value) {
      await fetchUser()
    } else {
      isLoading.value = false
    }
  })
  
  return {
    user,
    isAuthenticated,
    isLoading,
    mfaToken,
    login,
    verifyTotp,
    sendOtp,
    verifyOtp,
    logout,
    refresh,
    setupTotp,
    enableTotp,
    enableOtp,
    disableMfa,
    getMfaStatus,
    getCurrentUser,
    hasPermission,
    hasRole,
    fetchUser,
  }
}
