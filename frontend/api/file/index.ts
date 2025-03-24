import { z } from "zod";

// 文件元数据Schema
export const fileSchema = z.object({
  id: z.number(),
  filename: z.string(),
  file_type: z.string(),
  size: z.number(),
  upload_time: z.string().datetime(),
  processed: z.boolean(),
});

// 文件上传请求Schema
export const uploadRequestSchema = z.object({
  file: z.instanceof(File), // 浏览器环境下使用
});

export const uploadResponseSchema = z.object({
  ...fileSchema.shape,
  message: z.string().optional(),
});

// 文件列表请求Schema
export const listFilesRequestSchema = z.object({
  page: z.number().min(1).default(1),
  per_page: z.number().min(1).max(100).default(10),
});

export const listFilesResponseSchema = z.array(fileSchema);

// 文件更新请求Schema
export const updateFileRequestSchema = z.object({
  new_filename: z.string().min(1),
});

// 接口配置
export const fileAPIs = {
  upload: {
    name: "uploadFile",
    path: "/files/",
    method: "POST",
    token: true,
    requestSchema: uploadRequestSchema,
    responseSchema: {
      success: {
        status: [201],
        schema: uploadResponseSchema,
      },
      fail: {
        status: [400, 401, 403, 413],
        schema: z.object({ message: z.string() }),
      },
    },
  } as const,

  list: {
    name: "listFiles",
    path: "/files/",
    method: "GET",
    token: true,
    requestSchema: listFilesRequestSchema,
    responseSchema: {
      success: {
        status: [200],
        schema: listFilesResponseSchema,
      },
      fail: {
        status: [401, 403],
        schema: z.object({ message: z.string() }),
      },
    },
  } as const,

  get: {
    name: "getFile",
    path: "/files/{file_id}",
    method: "GET",
    token: true,
    requestSchema: z.object({}), // 无请求体
    responseSchema: {
      success: {
        status: [200],
        schema: fileSchema,
      },
      fail: {
        status: [401, 403, 404],
        schema: z.object({ message: z.string() }),
      },
    },
  } as const,

  update: {
    name: "updateFile",
    path: "/files/{file_id}",
    method: "PUT",
    token: true,
    requestSchema: updateFileRequestSchema,
    responseSchema: {
      success: {
        status: [200],
        schema: fileSchema,
      },
      fail: {
        status: [400, 401, 403, 404],
        schema: z.object({ message: z.string() }),
      },
    },
  } as const,

  delete: {
    name: "deleteFile",
    path: "/files/{file_id}",
    method: "DELETE",
    token: true,
    requestSchema: z.object({}),
    responseSchema: {
      success: {
        status: [200],
        schema: z.object({ message: z.string() }),
      },
      fail: {
        status: [401, 403, 404],
        schema: z.object({ message: z.string() }),
      },
    },
  } as const,
};
