import { z } from "zod";

export const tokenSchema = z.object({
  access_token: z.string(),
  token_type: z.string(),
});

export type TokenResponse = z.infer<typeof tokenSchema>;
