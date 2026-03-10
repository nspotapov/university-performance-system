// Принудительно устанавливаем светлую тему
export default defineNuxtPlugin(() => {
  if (import.meta.client) {
    document.documentElement.classList.remove('dark')
    document.documentElement.classList.add('light')
    
    // Блокируем изменение темы
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.attributeName === 'class') {
          document.documentElement.classList.remove('dark')
          document.documentElement.classList.add('light')
        }
      })
    })
    
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    })
  }
})
