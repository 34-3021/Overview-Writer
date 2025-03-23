import { z } from "zod";

export type APIMock = (
  payload?: any,
  param?: any,
  token?: string,
) => {
  status: number;
  data: any;
};

// Define the ResponseType structure, where ZodType retains inference
type ResponseType<T extends { [key: string]: { schema: z.ZodType<object> } }> = {
  [K in keyof T]: {
    status: readonly number[];
    schema: T[K]["schema"];
  };
};

// Transform ResponseType to a union type with accurate key and data typing
export type ResponseUnion<T extends ResponseType<any>> = {
  [K in keyof T]: {
    type: K;
    data: z.infer<T[K]["schema"]>;
  };
}[keyof T];

export interface APISchema<
  RequestType extends object,
  ResponseComposedType extends ResponseType<any>,
> {
  name: string;
  path: string;
  method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
  token?: boolean;
  requestSchema: z.ZodType<RequestType>;
  responseSchema: ResponseComposedType;
  mock?: APIMock;
}

const ENABLE_MOCK = false; // TODO: get from runtime config

const logger = console
const objectToSnake = (x: any) => x;
const objectToCamel = (x: any) => x;

function responseSchemaMatch<
  RequestType extends object,
  ResponseComposedType extends ResponseType<any>,
>(
  schema: APISchema<RequestType, ResponseComposedType>,
  response: { status: number; data: any },
): ResponseUnion<ResponseComposedType> {
  const status = response.status;
  const data = objectToCamel(response.data);

  const responseSchema = Object.entries(schema.responseSchema).find(([key, value]) =>
    value.status.includes(status),
  );

  if (!responseSchema) {
    if (response.status === 401) {
      const toast = useToast()
      toast.add({ title: "401 Unauthorized", color: "red" });
      throw new Error(`[${schema.name}]: Unauthorized.`);
    } else if (response.status.toString().startsWith("5")) {
      const toast = useToast()
      toast.add({ title: "500 Server Error", color: "red" });
      throw new Error(`[${schema.name}]: Server Error.`);
    } else {
      throw new Error(`[${schema.name}]: Response status ${status} not matched.`);
    }
  }

  const zodSchema: z.ZodType<any> = responseSchema[1].schema;
  const parsedData = zodSchema.safeParse(data);

  if (parsedData.success) {
    return {
      type: responseSchema[0],
      data: parsedData.data,
    };
  }

  logger.error(
    `[${schema.name}]: Response pre-check failed. Response-data: ${JSON.stringify(data)}. Error: ${parsedData.error.message}`,
  );

  throw new Error(`[${schema.name}]: Response pre-check failed.`);
}

export async function callApi<
  RequestType extends object,
  ResponseComposedType extends ResponseType<any>,
>(
  schema: APISchema<RequestType, ResponseComposedType>,
  payload: RequestType,
  param: Record<string, string> = {},
  // cookie?: string | null,
): Promise<ResponseUnion<ResponseComposedType>> {
  /* 'param' is the parameters in the URL, like 'id' in /user/:id:/profile */

  // get environment variables
  const runtimeConfig = useRuntimeConfig()

  const basePath = runtimeConfig.public.httpBase
  // Check the request

  const parsedPayload = schema.requestSchema.safeParse(payload);
  if (!parsedPayload.success) {
    throw new Error(
      `[${schema.name}]: Request pre-check failed. Request-payload: ${JSON.stringify(payload)}`,
    );
  }

  const convertedPayload = objectToSnake(parsedPayload.data);

  // TODO: get token

  if (schema.mock && ENABLE_MOCK) {
    const response = schema.mock(convertedPayload, param);
    return responseSchemaMatch(schema, response);
  }

  const path = Object.entries(param).reduce((acc, [key, value]) => {
    return acc.replace(`:${key}:`, value);
  }, basePath + schema.path);

  // Send the request
  const urlParams = new URLSearchParams(convertedPayload as Record<string, string>);

  // Manual token handling
  const userStore = useUserStore();
  const token = userStore.token;

  logger.info(`[${schema.name}]: Sending request to ${path}`);
  logger.info(`[${schema.name}]: Request-payload: ${JSON.stringify(convertedPayload)}`);

  const fetchResponse = await fetch(
    schema.method === "GET" || schema.method === "DELETE" ? `${path}?${urlParams}` : path,
    {
      method: schema.method,
      headers: schema.token ? {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      } : {
        "Content-Type": "application/json",
      },
      body:
        schema.method === "POST" || schema.method === "PUT"
          ? JSON.stringify(convertedPayload)
          : undefined,
    },
  );

  const data = await fetchResponse.json();
  // if (!fetchResponse.ok) {
  //   if (fetchResponse.status === 401) {
  //     throw new Error(`[${schema.name}]: Unauthorized. Response-status: ${fetchResponse.status}`);
  //   }
  //   logger.error(
  //     `[${schema.name}]: Request failed. Response-status: ${fetchResponse.status}. Response: ${JSON.stringify(data)}`,
  //   );
  //   // throw new Error(`[${schema.name}]: Request failed. Response-status: ${fetchReponse.status}`);
  // }

  logger.info(`[${schema.name}]: Response-status: ${fetchResponse.status}.`);

  const response = {
    status: fetchResponse.status,
    data,
  };

  // Process the response schema
  return responseSchemaMatch(schema, response);
}