import type { CreateClientConfig } from "./src/lib/client/client.gen";

export const createClientConfig: CreateClientConfig = (config) => ({
	...config,
	baseURL: "",
});
