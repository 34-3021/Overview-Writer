<!-- app/pages/documents/[id].vue -->

<script setup lang="ts">
import { callApi } from '~/../api/api'
import { documentAPIs } from '~/../api/document'
import { z } from 'zod'

const route = useRoute()
const toast = useToast()
const docId = computed(() => route.params.id as string)

// Document state
const document = ref<any>(null)
const loading = ref(true)
const saving = ref(false)
const generating = ref(false)

// Form state for new content
const newContent = reactive({
  type: 'paragraph',
  text: ''
})

// Fetch document on mount
onMounted(async () => {
  try {
    const { type, data } = await callApi(documentAPIs.get, {}, { doc_id: docId.value })
    if (type === 'success') {
      document.value = data
      // Initialize empty content if none exists
      if (!document.value.content?.sections) {
        document.value.content = { sections: [] }
      }
    }
  } catch (error) {
    toast.add({ title: 'Failed to load document', color: 'error' })
  } finally {
    loading.value = false
  }
})

// Add new content to document
const addContent = (type: string) => {
  if (!document.value) return
  
  const newItem = {
    id: Date.now().toString(),
    type,
    content: type.includes('heading') ? '' : 'Start writing here...',
    isAI: false
  }
  
  document.value.content.sections.push(newItem)
}

// Generate AI content
const generateAI = async (sectionId: string) => {
  if (!document.value) return
  
  generating.value = true
  try {
    const section = document.value.content.sections.find((s: any) => s.id === sectionId)
    if (!section) return
    
    const { type, data } = await callApi(
      documentAPIs.generate, 
      { type: section.type }, 
      { doc_id: docId.value }
    )
    
    if (type === 'success') {
      section.content = data.content
    }
  } catch (error) {
    toast.add({ title: 'Failed to generate content', color: 'error' })
  } finally {
    generating.value = false
  }
}

// Save document
const saveDocument = async () => {
  if (!document.value) return
  
  saving.value = true
  try {
    const payload = {
      content: {
        sections: document.value.content.sections.map(section => ({
          id: section.id,
          type: section.type,
          content: section.content
        }))
      }
    }

    const { type } = await callApi(
      documentAPIs.update, 
      payload, 
      { doc_id: docId.value }
    )
    
    if (type === 'success') {
      toast.add({ title: 'Document saved', color: 'primary' })
    }
  } catch (error) {
    toast.add({ 
      title: 'Failed to save document', 
      description: error.message,
      color: 'error' 
    })
  } finally {
    saving.value = false
  }
}

// Delete a section
const deleteSection = (sectionId: string) => {
  if (!document.value) return
  
  document.value.content.sections = document.value.content.sections.filter(
    (s: any) => s.id !== sectionId
  )
}
</script>

<template>
  <UContainer class="py-8">
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center py-12">
      <UProgress animation="elastic" />
    </div>

    <!-- Document editor -->
    <div v-else-if="document" class="space-y-6">
      <UCard class="">
        <template #header>
          <div class="flex items-center justify-between">
            <h1 class="text-2xl font-bold">{{ document.title }}</h1>
            <UButton
              color="primary"
              :loading="saving"
              @click="saveDocument"
              icon="i-heroicons-document-arrow-down"
              label="Save Document"
            />
          </div>
        </template>

        <!-- Content controls -->
        <div class="flex gap-2 mb-6">
          <UButton
            @click="addContent('heading1')"
            icon="i-heroicons-hashtag"
            label="Add Heading 1"
            color="neutral"
            variant="outline"
          />
          <UButton
            @click="addContent('heading2')"
            icon="i-heroicons-hashtag"
            label="Add Heading 2"
            color="neutral"
            variant="outline"
          />
          <UButton
            @click="addContent('paragraph')"
            icon="i-heroicons-document-text"
            label="Add Paragraph"
            color="neutral"
            variant="outline"
          />
        </div>

        <!-- Document content -->
        <div class="space-y-8">
          <div
            v-for="section in document.content.sections"
            :key="section.id"
            class="group relative p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            <!-- Heading 1 -->
            <div v-if="section.type === 'heading1'" class="space-y-2">
              <h2 class="text-xl font-semibold">
                <UInput
                  v-model="section.content"
                  placeholder="Heading 1"
                  class="text-xl font-semibold"
                />
              </h2>
            </div>

            <!-- Heading 2 -->
            <div v-else-if="section.type === 'heading2'" class="space-y-2">
              <h3 class="text-lg font-medium">
                <UInput
                  v-model="section.content"
                  placeholder="Heading 2"
                  class="text-lg font-medium"
                />
              </h3>
            </div>

            <!-- Paragraph -->
            <div v-else class="space-y-2">
              <UTextarea
                v-model="section.content"
                placeholder="Write your content here..."
                resize
                :rows="4"
              />
            </div>

            <!-- Section controls -->
            <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 flex gap-1">
              <UButton
                v-if="!section.isAI"
                @click="generateAI(section.id)"
                :loading="generating"
                icon="i-heroicons-sparkles"
                color="primary"
                variant="ghost"
                size="xs"
                title="Generate with AI"
              />
              <UButton
                @click="deleteSection(section.id)"
                icon="i-heroicons-trash"
                color="error"
                variant="ghost"
                size="xs"
                title="Delete section"
              />
            </div>

          </div>

          <!-- Empty state -->
          <div
            v-if="document.content.sections.length === 0"
            class="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg text-center"
          >
            <UIcon name="i-heroicons-document-text" class="w-12 h-12 text-gray-400 mb-4" />
            <h3 class="text-lg font-medium text-gray-600 dark:text-gray-300">
              No content yet
            </h3>
            <p class="text-gray-500 dark:text-gray-400 mt-1">
              Add your first section to get started
            </p>
          </div>
        </div>
      </UCard>
    </div>

    <!-- Error state -->
    <div v-else class="flex flex-col items-center justify-center py-12">
      <UIcon name="i-heroicons-exclamation-triangle" class="w-12 h-12 text-red-500" />
      <h2 class="mt-4 text-xl font-medium">Document not found</h2>
      <UButton
        to="/documents"
        label="Back to documents"
        color="neutral"
        variant="ghost"
        class="mt-4"
      />
    </div>
  </UContainer>
</template>
