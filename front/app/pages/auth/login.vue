<template>
  <div class="flex-1 flex items-center justify-center">
    <UForm
      :schema="schema"
      :state="state"
      class="space-y-4 min-w-1/4"
      @submit="loginFormOnSubmit"
    >
      <UFormField
        label="Email"
        name="email"
      >
        <UInput
          v-model="state.email"
          class="w-full"
        />
      </UFormField>

      <UFormField
        label="Пароль"
        name="password"
      >
        <UInput
          v-model="state.password"
          class="w-full"
          type="password"
        />
      </UFormField>

      <UButton type="submit">
        Войти
      </UButton>
    </UForm>

    <UModal
      v-model:open="otpCodeModalOpen"
      :dismissible="false"
      :close="{
        color: 'primary',
        variant: 'outline',
        class: 'rounded-full'
      }"
      title="Введите код подтверждения"
      :description="`Код подтверждения выслан на почту ${state.email}`"
    >
      <template #body>
        <div class="w-full gap-5 flex flex-col justify-center items-center">
          <UPinInput
            id="pin-input"
            v-model="otpCode"
            otp
            mask
            :length="4"
            type="number"
            :autofocus="true"
          />
          <span
            :v-if="otpCodeErrorText !== ''"
          >
            {{ otpCodeErrorText }}
          </span>
        </div>
      </template>
    </UModal>
  </div>
</template>

<script lang="ts" setup>
import * as v from 'valibot'

definePageMeta({
  layout: 'no-authenticated',
})

const schema = v.object({
  email: v.pipe(v.string(), v.email('Неверный формат email')),
  password: v.pipe(v.string()),
})

const state = reactive({
  email: '',
  password: '',
})

const toast = useToast()

const otpCode = ref([])
const lastOtpCode = ref([])
const otpCodeErrorText = ref('')
const otpCodeModalOpen = ref(false)
const isOtpLoading = ref(false)
const isOtpVerified = ref(false)

// Watcher для отслеживания изменения пин-кода
watch(otpCode, async (newValue) => {
  // Проверяем, что введены все 4 цифры
  if (newValue.join('').length === 4 && !isOtpVerified.value && newValue.join('') !== lastOtpCode.value.join('')) {
    lastOtpCode.value = otpCode.value
    await verifyOtpCode()
  }
})

async function loginFormOnSubmit() {
  const { $api } = useNuxtApp()

  try {
    await $api(
      'auth/login', {
        method: 'POST',
        body: state,
      })

    otpCodeModalOpen.value = true
  }
  catch {
    toast.add({ title: 'Ошибка', description: 'Неверный email или пароль', color: 'warning' })
  }
}

async function verifyOtpCode() {
  if (isOtpLoading.value) return

  isOtpLoading.value = true

  const { $api } = useNuxtApp()

  try {
    const otpLoginResponse = await $api(
      'auth/otp', {
        method: 'POST',
        body: {
          ...state,
          otp_code: otpCode.value.join(''),
        },
      },
    )

    isOtpVerified.value = true

    otpCodeErrorText.value = ''

    toast.add({ title: 'Успешно', description: 'Вход выполнен', color: 'success' })

    useCookie(AuthConfig.AccessTokenCookieName).value = otpLoginResponse.token

    setTimeout(async () => {
      otpCodeModalOpen.value = false
      navigateTo(RoutePaths.Main)
    }, 500)
  }
  catch {
    otpCodeErrorText.value = 'Неверный код подтверждения'
    isOtpLoading.value = false
  }
}
</script>

<style lang="scss">

</style>
