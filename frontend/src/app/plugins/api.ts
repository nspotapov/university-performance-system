import type { H3Error } from 'h3'
import { AuthConfig } from '~/types/auth'
import { RoutePaths } from '~/types/routes'

type IResponse = Response & {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  _data: any
} | null

interface ApiErrorOptions {
  response: IResponse
  error: H3Error | Error
}

/**
 * Обработчик ошибок API
 */
function handleApiError({ response, error }: ApiErrorOptions) {
  if (!response) {
    console.error('Network error:', error.message)
    return
  }

  const errorMessage = response._data?.message || error?.message || 'Unknown error'

  const toast = useToast()

  switch (response.status) {
    case 401:
      return navigateTo(RoutePaths.Auth.Login)

    case 403:
    case 404:
    case 400:
      break

    case 500:
      toast.add({ title: 'Ошибка', description: 'Произошла ошибка на сервере, попробуйте позже', color: 'error' })
      break

    default:
      console.error(`Error ${response.status}:`, errorMessage)
  }

  throw createError({
    statusCode: response.status,
    statusMessage: errorMessage,
    fatal: false,
  })
}

export default defineNuxtPlugin({
  name: 'api-plugin',
  setup() {
    const config = useRuntimeConfig()
    const accessTokenCookie = useCookie(AuthConfig.AccessTokenCookieName)

    const api = $fetch.create({
      baseURL: config.public.baseApiUrl,

      onRequest({ request, options }) {
        // Добавляем заголовок авторизации, если есть токен
        if (accessTokenCookie.value) {
          options.headers = {
            ...options.headers,
            Authorization: `Bearer ${accessTokenCookie.value}`,
          } as any
        }

        if (import.meta.dev) {
          console.log('[API Request]', request, options)
        }
      },

      async onResponse({ response }) {
        if (import.meta.dev) {
          console.log('[API Response]', response.status, response._data)
        }
      },

      async onResponseError({ response, error }): Promise<void> {
        handleApiError({
          response: response as IResponse,
          error: error as H3Error,
        })
      },
    })

    return {
      provide: {
        api,
      },
    }
  },
})
