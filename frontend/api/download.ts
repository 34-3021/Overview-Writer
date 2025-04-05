// api/download.ts
import type { APISchema, ResponseUnion, ResponseType } from "~/../api/api";
import { useToast } from "#imports";

const logger = console;
const objectToSnake = (x: any) => x;
const objectToCamel = (x: any) => x;

export async function downloadApi<
  RequestType extends object,
  ResponseComposedType extends ResponseType<any>
>(
  schema: APISchema<RequestType, ResponseComposedType>,
  payload: RequestType,
  param: Record<string, string> = {},
  cookie?: string | null
): Promise<ResponseUnion<ResponseComposedType>> {
  // 获取环境变量
  const runtimeConfig = useRuntimeConfig();
  const basePath = runtimeConfig.public.httpBase;

  // 请求验证
  const parsedPayload = schema.requestSchema.safeParse((payload as any)["_vts"] ? (payload as any).data : payload);
  if (!parsedPayload.success) {
    throw new Error(
      `[${schema.name}]: Request pre-check failed. Request-payload: ${JSON.stringify(payload)}`
    );
  }

  // 构建路径
  const path = Object.entries(param).reduce((acc, [key, value]) => {
    return acc.replace(`:${key}:`, value);
  }, basePath + schema.path);

  logger.info(`[${schema.name}]: Sending download request to ${path}`);

  // 手动处理token
  const userStore = useUserStore();
  const token = userStore.token;

  const fetchConfig: any = {
    method: schema.method,
    headers: {
      "Content-Type": "application/json",
    },
    body:
    schema.method === "POST" || schema.method === "PUT"
      ? JSON.stringify(parsedPayload.data)
      : undefined,
  };

  if (schema.token) {
    if (userStore.token === "") {
      throw new Error(`[${schema.name}]: Token is required for this request.`);
    }
    fetchConfig.headers = {
      ...fetchConfig.headers,
      Authorization: `Bearer ${userStore.token}`,
    };
  }

  console.log("fetchConfig", fetchConfig);

  // 发送请求
  const fetchResponse = await fetch(path, fetchConfig);

  // 处理非200响应
  if (!fetchResponse.ok) {
    let errorMessage = `[${schema.name}]: Request failed with status ${fetchResponse.status}`;
    
    try {
      const errorData = await fetchResponse.json();
      errorMessage = errorData.message || errorMessage;
    } catch (error) {
      logger.error(`[${schema.name}]: Failed to parse error response`);
    }

    const toast = useToast();
    toast.add({
      title: "下载失败",
      description: errorMessage,
      color: "error",
    });

    throw new Error(errorMessage);
  }

  // 检查响应类型是否为文件
  const contentType = fetchResponse.headers.get("content-type") || "";
  const isFileDownload =
    contentType.includes("application/octet-stream") ||
    contentType.includes("application/pdf") ||
    contentType.includes("application/zip") ||
    contentType.includes("text/markdown");

  if (!isFileDownload) {
    // 如果不是文件下载，尝试解析为JSON
    try {
      const data = await fetchResponse.json();
      const camelData = objectToCamel(data);
      
      const response = {
        status: fetchResponse.status,
        data: camelData,
      };

      const responseSchema = Object.entries(schema.responseSchema).find(([key, value]) =>
        value.status.includes(fetchResponse.status)
      );

      if (!responseSchema) {
        throw new Error(`[${schema.name}]: Response status ${fetchResponse.status} not matched.`);
      }

      const zodSchema = responseSchema[1].schema;
      const parsedData = zodSchema.safeParse(camelData);

      if (parsedData.success) {
        return {
          type: responseSchema[0],
          data: parsedData.data,
        };
      }

      throw new Error(`[${schema.name}]: Response pre-check failed.`);
    } catch (error) {
      throw new Error(`[${schema.name}]: Response parsing failed - ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  // 处理文件下载
  const blob = await fetchResponse.blob();
  const contentDisposition = fetchResponse.headers.get("content-disposition") || "";
  let filename = "download";

  // 从content-disposition中提取文件名
  const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
  if (filenameMatch && filenameMatch[1]) {
    filename = filenameMatch[1];
  } else {
    // 根据content-type设置默认文件名
    if (contentType.includes("pdf")) {
      filename += ".pdf";
    } else if (contentType.includes("zip")) {
      filename += ".zip";
    } else if (contentType.includes("markdown")) {
      filename += ".md";
    }
  }

  // 创建下载链接
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);

  // 返回成功响应
  return {
    type: "success",
    data: {
      message: "File download initiated",
      filename,
    },
  };
}
