import type { APIMock } from "./api";

export const DebugMock: APIMock = (payload: any) => {
  console.log("MockData: ", payload);
  return {
    status: 200,
    data: payload,
  };
};