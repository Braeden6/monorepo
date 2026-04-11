import { defineConfig } from "orval";

export default defineConfig({
	recipeApi: {
		input: {
			target: "http://localhost:8001/openapi.json",
		},
		output: {
			target: "./lib/api/generated",
			client: "react-query",
			httpClient: "axios",
			override: {
				mutator: {
					path: "./lib/api/axios-instance.ts",
					name: "customInstance",
				},
				query: {
					useQuery: true,
					useMutation: true,
					useSuspenseQuery: true,
				},
			},
			prettier: true,
			clean: true,
		},
	},
});
