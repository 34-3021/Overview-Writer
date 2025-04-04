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
const showAIPromptModal = ref(false)
const currentSectionId = ref('')

const form = reactive({
  aiPrompt: '',
  aiMessage: '',
})

// AI Chat state
const aiMessages = ref<Array<{role: string, content: string}>>([])
// const aiMessage = ref('')

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
    // content: type.includes('heading') ? '' : 'Start writing here...',
    content: '',
    isAI: false
  }
  
  document.value.content.sections.push(newItem)
}

// Move section up/down
const moveSection = (sectionId: string, direction: 'up' | 'down') => {
  if (!document.value) return
  
  const sections = document.value.content.sections
  const index = sections.findIndex((s: any) => s.id === sectionId)
  
  if (direction === 'up' && index > 0) {
    // Move section up
    const temp = sections[index - 1]
    sections[index - 1] = sections[index]
    sections[index] = temp
  } else if (direction === 'down' && index < sections.length - 1) {
    // Move section down
    const temp = sections[index + 1]
    sections[index + 1] = sections[index]
    sections[index] = temp
  }
}

// Open AI prompt modal
const openAIPrompt = (sectionId: string) => {
  currentSectionId.value = sectionId
  showAIPromptModal.value = true
}

// Generate AI content
const generateAI = async () => {
  if (!document.value || !currentSectionId.value) return
  
  // First save the document
  await saveDocument(true)
  
  generating.value = true
  try {
    const section = document.value.content.sections.find((s: any) => s.id === currentSectionId.value)
    if (!section) return
    
    // Call API with prompt
    const { type, data } = await callApi(
      documentAPIs.generate, 
      { 
        type: section.type,
        prompt: form.aiPrompt 
      }, 
      { doc_id: docId.value }
    )
    
    if (type === 'success') {
      section.content = data.content
      
      // is it necessary?????????????
      // Add to chat history
      aiMessages.value.push({
        role: 'user',
        content: form.aiPrompt
      })
      aiMessages.value.push({
        role: 'assistant',
        content: data.content
      })
    }
  } catch (error) {
    toast.add({ title: 'Failed to generate content', color: 'error' })
  } finally {
    generating.value = false
    showAIPromptModal.value = false
    form.aiPrompt = ''
  }
}

// Send AI chat message
const sendAIMessage = async () => {
  if (!form.aiMessage.trim()) return
  
  // Add user message
  aiMessages.value.push({
    role: 'user',
    content: form.aiMessage
  })
  
  const currentMessage = form.aiMessage
  form.aiMessage = ''
  
  try {
    // Call API with chat message
    const { type, data } = await callApi(
      documentAPIs.generate, 
      { 
        type: 'chat',
        prompt: currentMessage
      }, 
      { doc_id: docId.value }
    )
    
    if (type === 'success') {
      // Add AI response
      aiMessages.value.push({
        role: 'assistant',
        content: data.content
      })
    }
  } catch (error) {
    toast.add({ title: 'Failed to get AI response', color: 'error' })
  }
}

// Save document
const saveDocument = async (quite: boolean) => {
  if (!document.value) return
  
  saving.value = true
  try {
    const payload = {
      content: {
        sections: document.value.content.sections.map((section: any) => ({
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
    
    if (type === 'success' && !quite) {
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
    <div v-else-if="document" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left column - document editor -->
      <div class="lg:col-span-2 space-y-6">
        <UCard class="h-full">
          <template #header>
            <div class="flex items-center justify-between">
              <h1 class="text-2xl font-bold">{{ document.title }}</h1>
              <UButton
                color="primary"
                :loading="saving"
                @click="saveDocument(false)"
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
          <div class="space-y-4">
            <div
              v-for="(section, index) in document.content.sections"
              :key="section.id"
              class="group relative p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              <!-- Section controls -->
              <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 flex gap-1">
                <UButton
                  v-if="index > 0"
                  @click="moveSection(section.id, 'up')"
                  icon="i-heroicons-arrow-up"
                  color="neutral"
                  variant="ghost"
                  size="xs"
                  title="Move up"
                />
                <UButton
                  v-if="index < document.content.sections.length - 1"
                  @click="moveSection(section.id, 'down')"
                  icon="i-heroicons-arrow-down"
                  color="neutral"
                  variant="ghost"
                  size="xs"
                  title="Move down"
                />
                <UButton
                  v-if="!section.isAI"
                  @click="openAIPrompt(section.id)"
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

              <!-- Heading 1 -->
              <div v-if="section.type === 'heading1'" class="space-y-2">
                <p>Title</p>
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
                <p>Subtitle</p>
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
                <p>Paragraph</p>
                <UTextarea
                  v-model="section.content"
                  placeholder="Write your content here..."
                  resize
                  class="w-full"
                  :rows="4"
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

      <!-- Right column - AI chat -->
      <div class="lg:col-span-1">
        <UCard class="h-full">
          <template #header>
            <h2 class="text-lg font-semibold">AI Writing Assistant</h2>
          </template>

          <!-- Chat messages -->
          <div class="space-y-4 h-96 overflow-y-auto">
            <div
              v-for="(message, index) in aiMessages"
              :key="index"
              class="p-3 rounded-lg"
              :class="{
                'bg-primary-50 dark:bg-primary-900': message.role === 'assistant',
                'bg-gray-50 dark:bg-gray-800': message.role === 'user'
              }"
            >
              <div class="font-medium mb-1">
                {{ message.role === 'assistant' ? 'AI Assistant' : 'You' }}
              </div>
              <div class="text-sm">{{ message.content }}</div>
            </div>
          </div>

          <!-- Chat input -->
          <template #footer>
            <UTextarea
              v-model="form.aiMessage"
              placeholder="Ask the AI for help..."
              resize
              :rows="2"
              class="w-full mb-3"
            />
            <UButton
              type="submit"
              label="Send"
              color="primary"
              :disabled="! form.aiMessage.trim()"
              class="w-full"
              @click="sendAIMessage"
            />
          </template>
        </UCard>
      </div>
    </div>

    <!-- AI Prompt Modal -->
    <UModal v-model:open="showAIPromptModal">
      <template #content>
        <UCard>
          <template #header>
            <h3 class="font-semibold text-lg">AI Content Generation</h3>
          </template>
  
          <UForm :state="form" class="space-y-4">
            <UFormField label="Instructions" name="prompt">
              <UTextarea
                v-model="form.aiPrompt"
                placeholder="Tell the AI what to write..."
                resize
                :rows="4"
                class="w-full"
              />
            </UFormField>
          </UForm>
          <template #footer>
            <UButton
              label="Cancel"
              color="neutral"
              @click="showAIPromptModal = false"
              class="mr-3"
            />
            <UButton
              type="submit"
              label="Generate"
              color="primary"
              @click="generateAI"
              :loading="generating"
              :disabled="!form.aiPrompt.trim()"
            />
          </template>
        </UCard>
      </template>
    </UModal>
  </UContainer>
</template>
