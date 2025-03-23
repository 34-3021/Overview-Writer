import { z } from "zod";

const loginRequestSchema = z.object({
    username: z.string(),
    password: z.string()
});

export const loginSuccessfulResponseSchema = z.object({
    token: z.string(),
    message: z.string()
});

export const loginFailedResponseSchema = z.object({
    message: z.string(),
});

export const loginSchema = {
    name: 'login',
    path: '/auth/login',
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
