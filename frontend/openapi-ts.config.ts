import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
	input: "http://localhost:4173/api/openapi.json",
	output: "src/lib/client",
	plugins: [
		{ name: "@hey-api/client-axios", runtimeConfigPath: "./hey-api.ts" },
	],
});
