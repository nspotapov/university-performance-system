<template>
  <div class="py-8">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Профиль</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Информация о пользователе -->
      <UCard class="lg:col-span-2">
        <template #header>
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Информация о пользователе</h2>
        </template>

        <div v-if="user" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-sm text-gray-500 dark:text-gray-400">Email</label>
              <p class="text-gray-900 dark:text-white">{{ user.email }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-500 dark:text-gray-400">Роль</label>
              <UBadge :label="user.role" color="primary" />
            </div>
            <div>
              <label class="text-sm text-gray-500 dark:text-gray-400">Статус</label>
              <UBadge :label="user.is_active ? 'Активен' : 'Заблокирован'" :color="user.is_active ? 'success' : 'error'" />
            </div>
            <div>
              <label class="text-sm text-gray-500 dark:text-gray-400">2FA</label>
              <UBadge :label="user.is_mfa_enabled ? (user.mfa_method === 'TOTP' ? 'TOTP' : 'OTP') : 'Отключена'" :color="user.is_mfa_enabled ? 'success' : 'neutral'" />
            </div>
          </div>
        </div>
      </UCard>

      <!-- Быстрые действия -->
      <UCard>
        <template #header>
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Действия</h2>
        </template>

        <div class="space-y-2">
          <UButton to="/profile/security" color="neutral" variant="ghost" class="w-full justify-start" icon="i-heroicons-shield-check">
            Безопасность
          </UButton>
          <UButton to="/profile/settings" color="neutral" variant="ghost" class="w-full justify-start" icon="i-heroicons-cog-6-tooth">
            Настройки
          </UButton>
        </div>
      </UCard>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const { user } = useAuth()
</script>
