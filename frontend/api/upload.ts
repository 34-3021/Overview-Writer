import type { APISchema, ResponseUnion, ResponseType } from "~/../api/api"; 

const logger = console
const objectToSnake = (x: any) => x;
const objectToCamel = (x: any) => x;

export async function uploadApi<
  RequestType extends object,
  ResponseComposedType extends ResponseType<any>,
>(
  schema: APISchema<RequestType, ResponseComposedType>,
  payload: RequestType,
  param: Record<string, string> = {},
  cookie?: string | null,
): Promise<ResponseUnion<ResponseComposedType>> {

  const runtimeConfig = useRuntimeConfig()
  const basePath = runtimeConfig.public.httpBase

  // 复用原有的请求验证
  const parsedPayload = schema.requestSchema.safeParse(payload);
  if (!parsedPayload.success) {
    throw new Error(
      `[${schema.name}]: Request pre-check failed. Request-payload: ${JSON.stringify(payload)}`,
    );
  }

  // 复用原有的路径构建
  const path = Object.entries(param).reduce((acc, [key, value]) => {
    return acc.replace(`:${key}:`, value);
  }, basePath + schema.path);

  logger.info(`[${schema.name}]: Sending file upload request to ${path}`);

  // 构建 FormData
  const formData = new FormData();
  Object.entries(payload).forEach(([key, value]) => {
    formData.append(key, value);
  });

  const userStore = useUserStore();
  const token = userStore.token;

  const fetchConfig = {
    method: schema.method,
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  };

  const fetchResponse = await fetch(path, fetchConfig);
  const responseText = await fetchResponse.text();

  let data;
  try {
    data = JSON.parse(responseText);
  } catch (error) {
    logger.error(`[${schema.name}]: Failed to parse response as JSON`, {
      status: fetchResponse.status,
      contentType: fetchResponse.headers.get('content-type'),
      responsePreview: responseText.slice(0, 200)
    });
    throw new Error(`[${schema.name}]: Response parsing failed - ${error instanceof Error ? error.message : 'Unknown error'}`);
  }

  if (!fetchResponse.ok) {
    logger.error(
      `[${schema.name}]: Request failed. Response-status: ${fetchResponse.status}. Response: ${responseText}`,
    );
    throw new Error(`[${schema.name}]: Request failed with status ${fetchResponse.status}`);
  }

  const response = {
    status: fetchResponse.status,
    data,
  };

  const status = response.status;
  const camelData = objectToCamel(response.data);
  const responseSchema = Object.entries(schema.responseSchema).find(([key, value]) =>
    value.status.includes(status),
  );

  if (!responseSchema) {
    throw new Error(`[${schema.name}]: Response status ${status} not matched.`);
  }

  const zodSchema = responseSchema[1].schema;
  const parsedData = zodSchema.safeParse(camelData);

  if (parsedData.success) {
    return {
      type: responseSchema[0],
      data: parsedData.data,
    };
  }

  logger.error(
    `[${schema.name}]: Response pre-check failed. Response-data: ${JSON.stringify(camelData)}. Error: ${parsedData.error.message}`,
  );

  throw new Error(`[${schema.name}]: Response pre-check failed.`);
}