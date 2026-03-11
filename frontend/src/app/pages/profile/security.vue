<template>
  <div class="py-8">
    <UButton color="neutral" variant="ghost" @click="navigateTo('/profile')" class="mb-4">
      <UIcon name="i-heroicons-arrow-left" class="w-5 h-5 mr-2" />
      Назад к профилю
    </UButton>

    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Безопасность</h1>

    <div class="space-y-6">
      <!-- Смена пароля -->
      <UCard>
        <template #header>
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Смена пароля</h2>
        </template>

        <UForm :schema="passwordSchema" :state="passwordForm" @submit="onChangePassword" class="space-y-4 max-w-md">
          <UFormField label="Текущий пароль" name="current_password">
            <UInput v-model="passwordForm.current_password" type="password" class="w-full" />
          </UFormField>
          <UFormField label="Новый пароль" name="new_password">
            <UInput v-model="passwordForm.new_password" type="password" class="w-full" />
          </UFormField>
          <UFormField label="Подтверждение" name="confirm_password">
            <UInput v-model="passwordForm.confirm_password" type="password" class="w-full" />
          </UFormField>
          <UButton type="submit" color="primary" :loading="isPasswordLoading">Сменить пароль</UButton>
        </UForm>
      </UCard>

      <!-- Двухфакторная аутентификация -->
      <UCard>
        <template #header>
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Двухфакторная аутентификация</h2>
        </template>

        <div v-if="mfaStatus" class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-900 dark:text-white">Статус 2FA</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ mfaStatus.is_required ? 'Обязательна для вашей роли' : 'Опционально' }}
              </p>
            </div>
            <UBadge :label="mfaStatus.is_enabled ? (mfaStatus.method === 'TOTP' ? 'TOTP' : 'OTP') : 'Отключена'" :color="mfaStatus.is_enabled ? 'success' : 'neutral'" />
          </div>

          <div v-if="!mfaStatus.is_enabled && !mfaStatus.is_required" class="space-y-4 pt-4 border-t">
            <h3 class="font-medium text-gray-900 dark:text-white">Включить 2FA</h3>
            <div class="flex gap-2">
              <UButton color="primary" variant="outline" @click="setupTOTP" :loading="isSettingUp">
                <UIcon name="i-heroicons-device-phone-mobile" class="w-5 h-5 mr-2" />
                Google Authenticator
              </UButton>
              <UButton color="primary" variant="outline" @click="enableOTP" :loading="isSettingUp">
                <UIcon name="i-heroicons-envelope" class="w-5 h-5 mr-2" />
                Email код
              </UButton>
            </div>
          </div>

          <div v-if="mfaStatus.is_enabled && !mfaStatus.is_required" class="pt-4 border-t">
            <UButton color="error" variant="outline" @click="showDisableModal = true" :disabled="isDisabling">
              Отключить 2FA
            </UButton>
          </div>
        </div>
      </UCard>
    </div>

    <!-- Модалка отключения 2FA -->
    <UModal v-model:open="showDisableModal">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">Отключить 2FA</h2>
        </template>
        <UForm :schema="disableSchema" :state="disableForm" @submit="onDisableMFA">
          <UFormField label="Пароль" name="password">
            <UInput v-model="disableForm.password" type="password" class="w-full" />
          </UFormField>
          <div class="flex gap-2 justify-end mt-4">
            <UButton color="neutral" variant="ghost" @click="showDisableModal = false">Отмена</UButton>
            <UButton type="submit" color="error" :loading="isDisabling">Отключить</UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>

    <!-- Модалка настройки TOTP -->
    <UModal v-model:open="showTOTPModal" :dismissible="false">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">Настройка TOTP</h2>
        </template>
        <div v-if="totpData" class="space-y-4">
          <div class="text-center">
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">Отсканируйте QR код в Google Authenticator</p>
            <img :src="qrCodeUrl" alt="QR Code" class="mx-auto w-48 h-48" />
            <p class="text-xs text-gray-400 mt-2">Secret: {{ totpData.secret }}</p>
          </div>
          <UForm :schema="totpSchema" :state="totpForm" @submit="onEnableTOTP">
            <UFormField label="Код из приложения" name="code">
              <UPinInput v-model="totpForm.code" :length="6" type="number" otp class="justify-center" />
            </UFormField>
            <div class="flex gap-2 justify-end mt-4">
              <UButton color="neutral" variant="ghost" @click="showTOTPModal = false">Отмена</UButton>
              <UButton type="submit" color="primary" :loading="isSettingUp">Подтвердить</UButton>
            </div>
          </UForm>
        </div>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { MfaStatus } from '~/types/auth'

definePageMeta({ middleware: ['auth'] })

const { getMfaStatus, setupTotp, enableTotp, enableOtp, disableMfa } = useAuth()
const toast = useToast()

const mfaStatus = ref<MfaStatus | null>(null)
const isPasswordLoading = ref(false)
const isSettingUp = ref(false)
const isDisabling = ref(false)
const showDisableModal = ref(false)
const showTOTPModal = ref(false)
const totpData = ref<{ secret: string; qr_code_uri: string } | null>(null)

const passwordSchema = v.object({
  current_password: v.pipe(v.string(), v.minLength(1, 'Введите пароль')),
  new_password: v.pipe(v.string(), v.minLength(6, 'Минимум 6 символов')),
  confirm_password: v.string(),
})

const passwordForm = reactive({ current_password: '', new_password: '', confirm_password: '' })

const disableSchema = v.object({
  password: v.pipe(v.string(), v.minLength(1, 'Введите пароль')),
})

const disableForm = reactive({ password: '' })

const totpSchema = v.object({
  code: v.pipe(v.string(), v.minLength(6, '6 цифр')),
})

const totpForm = reactive({ code: ['','','','','',''] as string[] })

const qrCodeUrl = computed(() => totpData.value ? `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(totpData.value.qr_code_uri)}` : '')

const loadMfaStatus = async () => {
  try { mfaStatus.value = await getMfaStatus() }
  catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
}

const onChangePassword = async () => {
  isPasswordLoading.value = true
  try {
    // TODO: API для смены пароля
    toast.add({ title: 'Инфо', description: 'Функция смены пароля в разработке', color: 'warning' })
    passwordForm.current_password = ''; passwordForm.new_password = ''; passwordForm.confirm_password = ''
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isPasswordLoading.value = false }
}

const setupTOTP = async () => {
  isSettingUp.value = true
  try {
    totpData.value = await setupTotp()
    showTOTPModal.value = true
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isSettingUp.value = false }
}

const enableOTP = async () => {
  isSettingUp.value = true
  try {
    await enableOtp()
    await loadMfaStatus()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isSettingUp.value = false }
}

const onEnableTOTP = async () => {
  isSettingUp.value = true
  try {
    await enableTotp(totpForm.code.join(''))
    showTOTPModal.value = false
    totpForm.code = ['','','','','','']
    await loadMfaStatus()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail || 'Неверный код', color: 'error' }) }
  finally { isSettingUp.value = false }
}

const onDisableMFA = async () => {
  isDisabling.value = true
  try {
    await disableMfa(disableForm.password)
    showDisableModal.value = false
    disableForm.password = ''
    await loadMfaStatus()
  } catch (e: any) { toast.add({ title: 'Ошибка', description: e.data?.detail, color: 'error' }) }
  finally { isDisabling.value = false }
}

onMounted(loadMfaStatus)
</script>
