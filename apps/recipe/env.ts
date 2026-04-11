import { createEnv } from "@t3-oss/env-nextjs";
import { env as uiEnv } from "@workspace/ui/env";
import { z } from "zod";

export const env = createEnv({
	extends: [uiEnv],
	client: {
		NEXT_PUBLIC_RECIPE_API_URL: z.string(),
	},
	runtimeEnv: {
		NEXT_PUBLIC_RECIPE_API_URL: process.env.NEXT_PUBLIC_RECIPE_API_URL,
	},
});
