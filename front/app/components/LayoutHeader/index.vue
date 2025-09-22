<template>
  <header class="container mx-auto p-5 flex flex-row justify-end">
    <ul class="flex gap-5">
      <li>
        <NuxtLink
          to="/"
          @click.prevent="logout()"
        >
          Выход
        </NuxtLink>
      </li>
    </ul>
  </header>
</template>

<script lang="ts" setup>

const logout = () => {
  useCookie(AuthConfig.AccessTokenCookieName).value = null
  navigateTo(RoutePaths.Auth.Login)
  const toast = useToast()
  toast.add({ title: 'Выход', description: 'Вы вышли из системы', color: 'info' })
}

</script>

<style scoped lang="scss">
@use './style.scss';
</style>
