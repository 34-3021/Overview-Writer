import { z } from "zod";

const loginRequestSchema = z.object({
    username: z.string(),
    password: z.string()
});

export const loginSuccessfulResponseSchema = z.object({
    access: z.string(),
    refresh: z.string(),
    message: z.string()
});

export const loginFailedResponseSchema = z.object({
    code: z.number(),
    message: z.string(),
    detail: z.array(z.any()).optional()
});

export const loginSchema = {
    name: 'login',
    base: 'AUTH',
    path: '/login',
    method: 'POST',
    token: false,
    requestSchema: loginRequestSchema,
    responseSchema: {
        success: {
            status: [200],
            schema: loginSuccessfulResponseSchema,
        },
        fail: {
            status: [400, 401, 403],
            schema: loginFailedResponseSchema
        }
    }
} as const;
