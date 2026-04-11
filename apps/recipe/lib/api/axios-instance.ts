import axios, { type AxiosRequestConfig } from "axios";
import { env } from "@/env";

export const AXIOS_INSTANCE = axios.create({
	baseURL: env.NEXT_PUBLIC_RECIPE_API_URL,
	paramsSerializer: (params) => {
		const searchParams = new URLSearchParams();
		for (const [key, value] of Object.entries(params)) {
			if (Array.isArray(value)) {
				for (const item of value) {
					if (item !== null && item !== undefined) {
						searchParams.append(key, item.toString());
					}
				}
			} else if (value !== null && value !== undefined) {
				searchParams.append(key, value.toString());
			}
		}
		return searchParams.toString();
	},
});

export const customInstance = <T>(
	config: AxiosRequestConfig,
	options?: AxiosRequestConfig,
): Promise<T> => {
	const source = axios.CancelToken.source();
	const promise = AXIOS_INSTANCE({
		...config,
		...options,
		cancelToken: source.token,
	}).then(({ data }) => data);

	// @ts-expect-error
	promise.cancel = () => {
		source.cancel("Query was cancelled");
	};

	return promise;
};
