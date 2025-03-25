<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { callApi } from '~/../api/api'
import { fileAPIs } from '~/../api/file'
import { uploadApi } from '~~/api/upload'

// 文件列表数据
const files = ref<any[]>([])
const loading = ref(false)
const uploadLoading = ref(false)
const uploadError = ref('')

// 初始化加载文件
onMounted(async () => {
  await refreshFiles()
})

// 刷新文件列表
const refreshFiles = async () => {
  loading.value = true
  try {
    const { data } = await callApi(fileAPIs.list, {})
    files.value = data as any[]
  } catch (error) {
    console.error('获取文件列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return

  uploadLoading.value = true
  uploadError.value = ''
  
  try {
    for (const file of input.files) {
      await uploadApi(fileAPIs.upload, { file })
    }
    await refreshFiles()
    useToast().add({ title: '文件上传成功', color: 'primary' })
  } catch (error: any) {
    uploadError.value = error.message || '文件上传失败'
  } finally {
    uploadLoading.value = false
    input.value = '' // 清空输入
  }
}

// 文件删除处理
const deleteLoading = ref<number | null>(null)

const handleDelete = async (fileId: number) => {
  deleteLoading.value = fileId
  try {
    await callApi(fileAPIs.delete, {}, { file_id: fileId.toString() })
    await refreshFiles()
    useToast().add({ title: '文件删除成功', color: 'primary' })
  } finally {
    deleteLoading.value = null
  }
}

// 文件大小格式化
const formatSize = (bytes: number) => {
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${size.toFixed(1)} ${units[unitIndex]}`
}

// 手动打开文件选择
const fileInput = ref<HTMLInputElement>()
const triggerFileSelect = () => fileInput.value?.click()
</script>

<template>
  <UCard class="max-w-4xl mx-auto">
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold">文件管理</h2>
        <UButton
          icon="i-heroicons-arrow-path-20-solid"
          color="neutral"
          variant="ghost"
          @onclick="refreshFiles"
        />
      </div>
    </template>

    <!-- 自定义上传区域 -->
    <div
      class="mb-6 border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors"
      :class="[
        uploadLoading ? 'border-primary-200 dark:border-primary-800' : 'border-gray-300 dark:border-gray-600',
        'hover:border-primary-500 hover:bg-primary-50/50 dark:hover:bg-primary-900/10'
      ]"
      @click="triggerFileSelect"
    >
      <input
        ref="fileInput"
        type="file"
        multiple
        accept=".pdf,.zip"
        class="hidden"
        @change="handleFileUpload"
      >
      
      <div class="space-y-3">
        <UIcon
          name="i-heroicons-cloud-arrow-up"
          class="w-12 h-12 mx-auto text-gray-400"
          :class="{ 'animate-pulse': uploadLoading }"
        />
        <div>
          <p class="font-medium">
            {{ uploadLoading ? '文件上传中...' : '点击上传或拖放文件' }}
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            支持 PDF 和 LaTeX ZIP 文件（最大 100MB）
          </p>
        </div>
      </div>
    </div>

    <!-- 错误提示 -->
    <UAlert
      v-if="uploadError"
      title="上传错误"
      :description="uploadError"
      icon="i-heroicons-exclamation-triangle"
      color="error"
      variant="solid"
      class="mb-4"
    />

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <svg
        class="animate-spin h-8 w-8 text-primary-600"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </div>

    <!-- 文件列表 -->
    <div v-if="!loading && files?.length" class="border rounded-lg overflow-hidden">
      <div
        v-for="file in files"
        :key="file.id"
        class="flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-gray-800 border-b last:border-b-0"
      >
        <div class="min-w-0">
          <p class="font-medium truncate">{{ file.filename }}</p>
          <p class="text-sm text-gray-500 mt-1">
            {{ file.file_type == "application/pdf" ? "PDF" : "LaTeX" }} • {{ formatSize(file.size) }} •
            {{ new Date(file.upload_time).toLocaleDateString() }}
          </p>
        </div>
        
        <UButton
          color="warning"
          variant="ghost"
          :loading="deleteLoading === file.id"
          @click="handleDelete(file.id)"
        >
          <template #leading>
            <UIcon name="i-heroicons-trash-20-solid" class="w-5 h-5" />
          </template>
        </UButton>
      </div>
    </div>

    <!-- 空状态 -->
    <UEmptyState
      v-else-if="!loading"
      icon="i-heroicons-document-arrow-up"
      title="暂无文件"
      description="上传您的第一个文件以开始使用"
      class="py-8"
    >
      <UButton
        label="立即上传"
        color="primary"
        :loading="uploadLoading"
        @click="triggerFileSelect"
      />
    </UEmptyState>
  </UCard>
</template>
