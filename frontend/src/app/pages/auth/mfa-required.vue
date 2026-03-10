<template>
  <div class="flex-1 flex items-center justify-center py-10">
    <UCard class="w-full max-w-lg">
      <template #header>
        <div class="text-center">
          <UIcon name="i-heroicons-shield-exclamation" class="w-16 h-16 mx-auto text-warning" />
          <h1 class="text-2xl font-bold mt-4">Требуется настройка 2FA</h1>
          <p class="text-sm text-gray-500 mt-2">
            Для вашей роли обязательна двухфакторная аутентификация
          </p>
        </div>
      </template>

      <div class="space-y-6">
        <!-- Выбор метода -->
        <div>
          <h3 class="font-semibold mb-3">Выберите метод аутентификации:</h3>
          <div class="grid grid-cols-2 gap-4">
            <UButton
              :variant="selectedMethod === 'TOTP' ? 'solid' : 'outline'"
              :color="selectedMethod === 'TOTP' ? 'primary' : 'neutral'"
              class="h-auto py-4 flex flex-col items-center"
              @click="selectMethod('TOTP')"
            >
              <UIcon name="i-heroicons-device-phone-mobile" class="w-8 h-8 mb-2" />
              <span class="text-sm font-medium">Google Authenticator</span>
              <span class="text-xs text-gray-500 mt-1">Приложение на телефоне</span>
            </UButton>
            
            <UButton
              :variant="selectedMethod === 'OTP' ? 'solid' : 'outline'"
              :color="selectedMethod === 'OTP' ? 'primary' : 'neutral'"
              class="h-auto py-4 flex flex-col items-center"
              @click="selectMethod('OTP')"
            >
              <UIcon name="i-heroicons-envelope" class="w-8 h-8 mb-2" />
              <span class="text-sm font-medium">Email код</span>
              <span class="text-xs text-gray-500 mt-1">Код приходит на почту</span>
            </UButton>
          </div>
        </div>

        <!-- TOTP настройка -->
        <div v-if="selectedMethod === 'TOTP'" class="space-y-4">
          <UAlert
            title="Настройка Google Authenticator"
            description="1. Установите приложение Google Authenticator&#10;2. Отсканируйте QR код&#10;3. Введите код из приложения"
            class="mb-4"
          />
          
          <div v-if="totpData" class="flex flex-col items-center space-y-4">
            <!-- QR Code -->
            <div class="bg-white p-4 rounded-lg">
              <img :src="qrCodeUrl" alt="TOTP QR Code" class="w-48 h-48" />
            </div>
            
            <p class="text-sm text-gray-500">
              Secret: <code class="bg-gray-100 px-2 py-1 rounded">{{ totpData.secret }}</code>
            </p>
          </div>
          
          <UFormField label="Код из приложения">
            <UPinInput
              v-model="totpCode"
              :length="6"
              type="number"
              otp
              class="justify-center"
            />
          </UFormField>
          
          <UButton
            color="primary"
            size="lg"
            class="w-full"
            :loading="isEnabling"
            :disabled="totpCode.length !== 6"
            @click="enableTotp"
          >
            Подтвердить и включить
          </UButton>
        </div>

        <!-- OTP настройка -->
        <div v-if="selectedMethod === 'OTP'" class="space-y-4">
          <UAlert
            title="Email аутентификация"
            description="Код для входа будет приходить на вашу почту&#10;Это менее безопасно, но удобнее"
            class="mb-4"
          />
          
          <UButton
            color="primary"
            size="lg"
            class="w-full"
            :loading="isEnabling"
            @click="enableOtp"
          >
            Включить email аутентификацию
          </UButton>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-between">
          <UButton variant="ghost" @click="logout">
            Выйти
          </UButton>
          <p class="text-xs text-gray-500">
            После настройки 2FA вы будете перенаправлены в систему
          </p>
        </div>
      </template>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { MFAMethod } from '~/types/auth'
import { RoutePaths } from '~/types/routes'

definePageMeta({
  layout: 'no-authenticated',
  middleware: ['auth'],
})

const toast = useToast()
const { $api } = useNuxtApp()
const { setupTotp, enableTotp: enableTotpApi, enableOtp: enableOtpApi, logout, fetchUser } = useAuth()

const selectedMethod = ref<'TOTP' | 'OTP'>('TOTP')
const totpData = ref<{ secret: string; qr_code_uri: string } | null>(null)
const totpCode = ref<string[]>([])
const isEnabling = ref(false)

// Генерация QR code URL из URI
const qrCodeUrl = computed(() => {
  if (!totpData.value) return ''
  // Используем API для генерации QR кода
  return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(totpData.value.qr_code_uri)}`
})

// Выбор метода
const selectMethod = async (method: 'TOTP' | 'OTP') => {
  selectedMethod.value = method
  
  if (method === 'TOTP' && !totpData.value) {
    await loadTotpSetup()
  }
}

// Загрузка TOTP настройки
const loadTotpSetup = async () => {
  try {
    totpData.value = await setupTotp()
  } catch (error: any) {
    toast.add({
      title: 'Ошибка',
      description: error.data?.detail || 'Не удалось загрузить настройки',
      color: 'error',
    })
  }
}

// Включение TOTP
const enableTotp = async () => {
  if (totpCode.value.length !== 6) return
  
  isEnabling.value = true
  try {
    await enableTotpApi(totpCode.value.join(''))
    await fetchUser()
    
    toast.add({
      title: 'Успешно',
      description: '2FA настроена',
      color: 'success',
    })
    
    navigateTo(RoutePaths.Main)
  } catch (error: any) {
    toast.add({
      title: 'Ошибка',
      description: error.data?.detail || 'Неверный код',
      color: 'error',
    })
    totpCode.value = []
  } finally {
    isEnabling.value = false
  }
}

// Включение OTP
const enableOtp = async () => {
  isEnabling.value = true
  try {
    await enableOtpApi()
    await fetchUser()
    
    toast.add({
      title: 'Успешно',
      description: 'Email аутентификация включена',
      color: 'success',
    })
    
    navigateTo(RoutePaths.Main)
  } catch (error: any) {
    toast.add({
      title: 'Ошибка',
      description: error.data?.detail || 'Не удалось включить',
      color: 'error',
    })
  } finally {
    isEnabling.value = false
  }
}

// Инициализация
onMounted(() => {
  loadTotpSetup()
})
</script>
