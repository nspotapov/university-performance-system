<template>
  <footer class="border-t border-gray-200 bg-white py-6">
    <div class="container mx-auto px-5">
      <div class="flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="text-sm text-gray-500">
          © {{ currentYear }} Система учёта успеваемости студентов
        </div>
        
        <div class="flex items-center gap-6 text-sm text-gray-500">
          <span>Версия: 1.0.0</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>
