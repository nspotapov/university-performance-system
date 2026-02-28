<template>
  <footer class="container mx-auto p-5">
    &copy; 2025-{{currentYear}} Потапов Н. С.
  </footer>
</template>

<script lang="ts" setup>
  const currentYear = new Date().getFullYear();
</script>

<style scoped lang="scss">
@use './style.scss';
</style>
