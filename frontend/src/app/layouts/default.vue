<script lang="ts" setup>

</script>

<template>
  <div class="min-h-screen w-full flex flex-col">
    <LayoutHeader />
    <main class="flex-1 container mx-auto px-5 flex flex-col">
      <slot />
    </main>
    <LayoutFooter />
  </div>
</template>
