import { z } from "zod";

export const generateContentSchema = z.object({
  content: z.string(),
  type: z.string()
});

export const documentSectionSchema = z.object({
  id: z.string(),
  type: z.string(),
  content: z.string()
});

export const documentContentSchema = z.object({
  sections: z.array(documentSectionSchema)
});

export const documentSchema = z.object({
  id: z.number(),
  title: z.string(),
  config: z.record(z.any()),
  content: documentContentSchema,
  created_at: z.string(),
  user_id: z.number()
});

export const documentAPIs = {
  create: {
    name: "createDocument",
    path: "/documents/",
    method: "POST",
    token: true,
    requestSchema: z.object({
      title: z.string(),
      config: z.record(z.any()).optional(),
      content: z.record(z.any())
    }),
    responseSchema: {
      success: { status: [200, 201], schema: documentSchema },
      fail: { status: [400, 401], schema: z.object({ message: z.string() }) }
    }
  } as const,
  list: {
    name: "listDocuments",
    path: "/documents/",
    method: "GET",
    token: true,
    requestSchema: z.object({}),
    responseSchema: {
      success: { status: [200], schema: z.array(documentSchema) },
      fail: { status: [401], schema: z.object({ message: z.string() }) }
    }
  } as const,
  get: {
    name: "getDocument",
    path: "/documents/:doc_id:",
    method: "GET",
    token: true,
    requestSchema: z.object({}),
    responseSchema: {
      success: { status: [200], schema: documentSchema },
      fail: { status: [401, 404], schema: z.object({ message: z.string() }) }
    }
  } as const,
  update: {
    name: "updateDocument",
    path: "/documents/:doc_id:",
    method: "PUT",
    token: true,
    requestSchema: z.object({
      title: z.string().optional(),
      config: z.record(z.any()).optional(),
      content: documentContentSchema.optional()
    }),
    responseSchema: {
      success: { status: [200], schema: documentSchema },
      fail: { status: [400, 401, 404], schema: z.object({ message: z.string() }) }
    }
  } as const,
  delete: {
    name: "deleteDocument",
    path: "/documents/:doc_id:",
    method: "DELETE",
    token: true,
    requestSchema: z.object({}),
    responseSchema: {
      success: { status: [200], schema: z.object({ message: z.string() }) },
      fail: { status: [401, 404], schema: z.object({ message: z.string() }) }
    }
  } as const,
  generate: {
    name: "generateDocumentContent",
    path: "/documents/:doc_id:/generate",
    method: "POST",
    token: true,
    requestSchema: z.object({
      type: z.string(),
      prompt: z.string(),
    }),
    responseSchema: {
      success: { status: [200], schema: generateContentSchema },
      fail: { status: [400, 401, 404], schema: z.object({ message: z.string() }) }
    }
  } as const
};
