<!-- app/pages/documents.vue -->
<script setup lang="ts">
import { callApi } from '~/../api/api'
import { documentAPIs } from '~/../api/document'

const documents = ref<any[]>([])
const loading = ref(false)
const deleteLoading = ref<number | null>(null)

// 初始化加载文档
onMounted(async () => {
  await refreshDocuments()
})

// 刷新文档列表
const refreshDocuments = async () => {
  loading.value = true
  try {
    const { type, data } = await callApi(documentAPIs.list, {})
    if (type !== "success") {
      useToast().add({ title: '加载失败', color: 'warning' })
      return
    }
    documents.value = data
  } finally {
    loading.value = false
  }
}

// 创建文档
const handleCreate = async () => {
  try {
    await callApi(documentAPIs.create, {
      title: '新文档',
      content: { sections: [] },
      config: {}
    })
    await refreshDocuments()
    useToast().add({ title: '文档创建成功', color: 'primary' })
  } catch (error) {
    useToast().add({ title: '创建失败', color: 'warning' })
  }
}

// 删除文档
const handleDelete = async (docId: number) => {
  deleteLoading.value = docId
  try {
    await callApi(documentAPIs.delete, {}, { doc_id: docId.toString() })
    await refreshDocuments()
    useToast().add({ title: '文档删除成功', color: 'primary' })
  } finally {
    deleteLoading.value = null
  }
}
</script>

<template>
  <UCard class="max-w-4xl mx-auto">
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold">文档管理</h2>
        <div class="flex gap-2">
          <UButton
            icon="i-heroicons-plus"
            label="新建文档"
            @click="handleCreate"
          />
          <UButton
            icon="i-heroicons-arrow-path"
            color="neutral"
            @click="refreshDocuments"
          />
        </div>
      </div>
    </template>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <UProgress animation="elastic" />
    </div>

    <!-- 文档列表 -->
    <div v-if="documents.length" class="space-y-4">
      <div 
        v-for="doc in documents"
        :key="doc.id"
        class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
      >
        <div>
          <h3 class="font-medium">{{ doc.title }}</h3>
          <p class="text-sm text-gray-500 mt-1">
            创建于 {{ new Date(doc.created_at).toLocaleDateString() }}
          </p>
        </div>
        
        <UButton
          color="warning"
          variant="ghost"
          :loading="deleteLoading === doc.id"
          @click="handleDelete(doc.id)"
          icon="i-heroicons-trash"
        />
      </div>
    </div>

    <!-- 空状态 -->
    <UEmptyState
      v-else
      icon="i-heroicons-document"
      title="暂无文档"
      description="点击上方按钮创建第一个文档"
    />
  </UCard>
</template>
