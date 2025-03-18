<script setup lang="ts">
const { $ui } = useNuxtApp()

const links = []
</script>

<template>
  <UFooter :links="links">
    <template #left>
      <NuxtLink to="https://github.com/34-3021/Overview-Writer" target="_blank" class="text-sm text-gray-500 dark:text-gray-400">
        Published under <span class="text-gray-900 dark:text-white">MIT License</span>
      </NuxtLink>
    </template>

    <template #right>
      <UButton icon="i-simple-icons-nuxtdotjs" to="https://github.com/34-3021/Overview-Writer" target="_blank" v-bind="($ui.button.secondary as any)" />
      <UButton icon="i-simple-icons-github" to="https://github.com/Zecyel" target="_blank" v-bind="($ui.button.secondary as any)" />
    </template>
  </UFooter>
</template>
