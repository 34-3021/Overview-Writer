import { z } from "zod";

// Define the ResponseType structure, where ZodType retains inference
type ResponseType<T extends { [key: string]: { schema: z.ZodType<any> } }> = {
  [K in keyof T]: {
    status: number[];
    schema: T[K]["schema"];
  };
};

// Transform ResponseType to a union type with accurate key and data typing
type ResponseUnion<T extends ResponseType<any>> = {
  [K in keyof T]: {
    key: K;
    data: z.infer<T[K]["schema"]>;
  };
}[keyof T];

// Example usage with specific schemas
const exampleSchema1 = z.object({
  id: z.number(),
  name: z.string(),
});

const exampleSchema2 = z.object({
  success: z.boolean(),
  message: z.string(),
});

// Define an example ResponseType
const responseTypeExample = {
  user: {
    status: [200],
    schema: exampleSchema1,
  },
  result: {
    status: [201],
    schema: exampleSchema2,
  },
};

// Example inferred union type
type ExampleUnion = ResponseUnion<typeof responseTypeExample>;

/* 
  ExampleUnion will now be:
  | { key: "user"; data: { id: number; name: string; } }
  | { key: "result"; data: { success: boolean; message: string; } }
*/

// Test example assignments
const example1: ExampleUnion = {
  key: "user",
  data: {
    id: 123,
    name: "John Doe",
  },
};

const example2: ExampleUnion = {
  key: "result",
  data: {
    success: true,
    message: "Operation successful",
  },
};