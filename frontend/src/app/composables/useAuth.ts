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
  
  /**
   * Проверка прав доступа
   */
  const hasPermission = (permission: string): boolean => {
    if (!user.value) return false
    if (user.value.role === UserRole.ADMIN) return true
    
    const permissions = RolePermissions[user.value.role] || []
    return permissions.includes('all') || permissions.includes(permission as any)
  }
  
  /**
   * Проверка роли
   */
  const hasRole = (roles: UserRole[]): boolean => {
    if (!user.value) return false
    return roles.includes(user.value.role)
  }
  
  /**
   * Вход в систему
   */
  const login = async (data: LoginRequest): Promise<LoginResponse> => {
    try {
      const response = await $api<LoginResponse>('auth/login', {
        method: 'POST',
        body: data,
      })
      
      if (response.mfa_required) {
        // Сохраняем MFA токен для второго этапа
        mfaToken.value = response.access_token
        mfaTokenCookie.value = response.access_token
      } else {
        // Сохраняем access токен
        accessTokenCookie.value = response.access_token
        isAuthenticated.value = true
        await fetchUser()
      }
      
      return response
    } catch (error: any) {
      if (error.statusCode === 403 && error.data?.detail === 'Двухфакторная аутентификация обязательна для вашей роли') {
        // Требуется настройка 2FA
        navigateTo(RoutePaths.Auth.MfaRequired)
      }
      throw error
    }
  }
  
  /**
   * Проверка TOTP кода
   */
  const verifyTotp = async (code: string): Promise<VerifyCodeResponse> => {
    const response = await $api<VerifyCodeResponse>('auth/mfa/totp/verify', {
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
  
  /**
   * Отправка OTP кода на email
   */
  const sendOtp = async (): Promise<OtpSendResponse> => {
    return await $api<OtpSendResponse>('auth/mfa/otp/send', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${mfaToken.value}`,
      },
    })
  }
  
  /**
   * Проверка OTP кода
   */
  const verifyOtp = async (code: string): Promise<VerifyCodeResponse> => {
    const response = await $api<VerifyCodeResponse>('auth/mfa/otp/verify', {
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
  
  /**
   * Выход из системы
   */
  const logout = async () => {
    try {
      await $api('auth/logout', { method: 'POST' })
    } catch (e) {
      // Игнорируем ошибки при выходе
    }
    
    accessTokenCookie.value = null
    mfaTokenCookie.value = null
    mfaToken.value = null
    user.value = null
    isAuthenticated.value = false
    navigateTo(RoutePaths.Auth.Login)
  }
  
  /**
   * Обновление access токена
   */
  const refresh = async () => {
    try {
      const response = await $api<RefreshTokenResponse>('auth/refresh', {
        method: 'POST',
      })
      accessTokenCookie.value = response.access_token
    } catch (error) {
      await logout()
    }
  }
  
  /**
   * Настройка TOTP
   */
  const setupTotp = async (): Promise<TotpSetupResponse> => {
    return await $api<TotpSetupResponse>('auth/mfa/totp/setup', {
      method: 'POST',
    })
  }
  
  /**
   * Включение TOTP
   */
  const enableTotp = async (code: string): Promise<void> => {
    await $api('auth/mfa/totp/enable', {
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
  
  /**
   * Включение OTP
   */
  const enableOtp = async (): Promise<void> => {
    await $api('auth/mfa/otp/enable', {
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
  
  /**
   * Отключение MFA
   */
  const disableMfa = async (password: string): Promise<void> => {
    await $api('auth/mfa/disable', {
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
  
  /**
   * Получение статуса MFA
   */
  const getMfaStatus = async (): Promise<MfaStatus> => {
    return await $api<MfaStatus>('auth/mfa/status')
  }
  
  /**
   * Получение текущего пользователя
   */
  const getCurrentUser = async (): Promise<User> => {
    return await $api<User>('auth/me')
  }
  
  /**
   * Загрузка данных пользователя
   */
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
  
  // Инициализация при загрузке
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
