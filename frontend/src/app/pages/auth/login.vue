<template>
  <div class="flex-1 flex items-center justify-center py-10">
    <UCard class="w-full max-w-md">
      <template #header>
        <h1 class="text-2xl font-bold text-center">Вход в систему</h1>
        <p class="text-sm text-gray-500 text-center mt-2">
          Введите свои учетные данные для входа
        </p>
      </template>

      <!-- Форма входа -->
      <UForm
        v-if="!mfaRequired"
        :schema="loginSchema"
        :state="loginState"
        class="space-y-4"
        @submit="handleLogin"
      >
        <UFormField label="Email" name="email">
          <UInput
            v-model="loginState.email"
            type="email"
            placeholder="email@university.ru"
            autocomplete="email"
          />
        </UFormField>

        <UFormField label="Пароль" name="password">
          <UInput
            v-model="loginState.password"
            type="password"
            placeholder="••••••••"
            autocomplete="current-password"
          />
        </UFormField>

        <UButton
          type="submit"
          color="primary"
          size="lg"
          class="w-full"
          :loading="isLoading"
        >
          Войти
        </UButton>
      </UForm>

      <!-- MFA выбор метода -->
      <div v-else class="space-y-4">
        <div class="text-center">
          <UIcon name="i-heroicons-shield-check" class="w-12 h-12 mx-auto text-primary" />
          <h2 class="text-lg font-semibold mt-2">Двухфакторная аутентификация</h2>
          <p class="text-sm text-gray-500">
            {{ mfaMethod === 'TOTP' 
              ? 'Введите код из Google Authenticator' 
              : 'Введите код из email или запросите новый' 
            }}
          </p>
        </div>

        <!-- TOTP ввод -->
        <div v-if="mfaMethod === 'TOTP'" class="space-y-4">
          <UFormField label="Код из приложения">
            <UPinInput
              v-model="mfaCode"
              :length="6"
              type="number"
              otp
              class="justify-center"
              @update:model-value="onCodeComplete"
            />
          </UFormField>
        </div>

        <!-- OTP ввод -->
        <div v-else-if="mfaMethod === 'OTP'" class="space-y-4">
          <UFormField label="Код из email">
            <UPinInput
              v-model="mfaCode"
              :length="6"
              type="number"
              otp
              class="justify-center"
              @update:model-value="onCodeComplete"
            />
          </UFormField>
          
          <div class="text-center">
            <UButton
              variant="link"
              :disabled="isOtpLoading"
              @click="sendOtpCode"
            >
              {{ isOtpLoading ? 'Отправка...' : 'Отправить код повторно' }}
            </UButton>
          </div>
        </div>

        <div v-if="mfaError" class="text-center text-red-500 text-sm">
          {{ mfaError }}
        </div>
      </div>

      <template #footer>
        <p class="text-xs text-center text-gray-500">
          Система учёта успеваемости студентов
        </p>
      </template>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import { MFAMethod } from '~/types/auth'
import { RoutePaths } from '~/types/routes'

definePageMeta({
  layout: 'no-authenticated',
})

const { $api } = useNuxtApp()
const toast = useToast()
const { login, verifyTotp, verifyOtp, sendOtp } = useAuth()

// Схема валидации
const loginSchema = v.object({
  email: v.pipe(
    v.string(),
    v.minLength(1, 'Введите email'),
    v.email('Неверный формат email')
  ),
  password: v.pipe(
    v.string(),
    v.minLength(1, 'Введите пароль')
  ),
})

// Состояние формы входа
const loginState = reactive({
  email: '',
  password: '',
})

// Состояние MFA
const mfaRequired = ref(false)
const mfaMethod = ref<MFAMethod | null>(null)
const mfaCode = ref<string[]>([])
const mfaError = ref('')
const isLoading = ref(false)
const isOtpLoading = ref(false)

// Обработка ввода кода
const onCodeComplete = async () => {
  if (mfaCode.value.length !== 6 || isOtpLoading.value) return
  
  const code = mfaCode.value.join('')
  mfaError.value = ''
  isOtpLoading.value = true
  
  try {
    if (mfaMethod.value === MFAMethod.TOTP) {
      await verifyTotp(code)
    } else if (mfaMethod.value === MFAMethod.OTP) {
      await verifyOtp(code)
    }
    
    toast.add({
      title: 'Успешно',
      description: 'Вход выполнен',
      color: 'success',
    })
    
    navigateTo(RoutePaths.Main)
  } catch (error: any) {
    mfaError.value = error.data?.detail || 'Неверный код'
    mfaCode.value = []
  } finally {
    isOtpLoading.value = false
  }
}

// Отправка OTP кода
const sendOtpCode = async () => {
  isOtpLoading.value = true
  try {
    await sendOtp()
    toast.add({
      title: 'Код отправлен',
      description: 'Проверьте вашу почту',
      color: 'success',
    })
  } catch (error: any) {
    toast.add({
      title: 'Ошибка',
      description: error.data?.detail || 'Не удалось отправить код',
      color: 'error',
    })
  } finally {
    isOtpLoading.value = false
  }
}

// Обработка входа
const handleLogin = async () => {
  isLoading.value = true
  mfaError.value = ''
  
  try {
    const response = await login({
      email: loginState.email,
      password: loginState.password,
    })
    
    if (response.mfa_required) {
      mfaRequired.value = true
      mfaMethod.value = response.mfa_method || MFAMethod.OTP
      
      // Если OTP, сразу отправляем код
      if (mfaMethod.value === MFAMethod.OTP) {
        await sendOtpCode()
      }
    } else {
      toast.add({
        title: 'Успешно',
        description: 'Вход выполнен',
        color: 'success',
      })
      navigateTo(RoutePaths.Main)
    }
  } catch (error: any) {
    toast.add({
      title: 'Ошибка входа',
      description: error.data?.detail || 'Неверный email или пароль',
      color: 'error',
    })
  } finally {
    isLoading.value = false
  }
}
</script>
