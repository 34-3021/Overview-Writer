import { z } from "zod";

export const documentSchema = z.object({
  id: z.number(),
  title: z.string(),
  config: z.record(z.any()),
  content: z.record(z.any()),
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
  } as const
};
