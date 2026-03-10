import { AuthConfig } from '~/types/auth'
import { RoutePaths } from '~/types/routes'

export default defineNuxtRouteMiddleware(async (to) => {
  const accessToken = useCookie(AuthConfig.AccessTokenCookieName)
  
  // Если токена нет и страница не публичная - редирект на логин
  if (!accessToken.value) {
    const publicPaths = [RoutePaths.Auth.Login, RoutePaths.Auth.MfaRequired]
    if (!publicPaths.includes(to.path as any)) {
      return navigateTo(RoutePaths.Auth.Login)
    }
    return
  }
  
  // Если уже аутентифицирован и пытается зайти на страницу авторизации - редирект на главную
  if (to.path.startsWith('/auth')) {
    return navigateTo(RoutePaths.Main)
  }
})
