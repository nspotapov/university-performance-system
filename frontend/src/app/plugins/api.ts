import type { H3Error } from 'h3'

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
      // console.error('Unauthorized access. Redirecting to login.')
      return navigateTo(RoutePaths.Auth.Login)

    case 403:
      // console.error('Forbidden:', errorMessage)
      break

    case 404:
      // console.error('Not found:', errorMessage)
      break

    case 400:
      // console.error('Bad request', errorMessage)
      break

    case 500:
      // console.error('Server error:', errorMessage)
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
  setup(nuxtApp) {
    const config = nuxtApp.$config

    let baseURL = '/'

    baseURL = config.public.baseApiUrl

    const api = $fetch.create({
      baseURL,

      onRequest({ request, options }) {
        // Добавляем заголовок авторизации, если есть токен
        const tokenAuthenticated = useCookie(AuthConfig.AccessTokenCookieName)

        if (tokenAuthenticated.value) {
          options.headers = {
            ...options.headers,
            Authorization: `Bearer ${tokenAuthenticated.value}`,
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
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
