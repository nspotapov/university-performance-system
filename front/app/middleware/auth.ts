export default defineNuxtRouteMiddleware(async () => {
  console.log('Auth middleware')

  const accessToken = useCookie(AuthConfig.AccessTokenCookieName)

  const isAuthenticated = ref(accessToken.value != null)

  if (!isAuthenticated.value) {
    return navigateTo(RoutePaths.Auth.Login)
  }
})
