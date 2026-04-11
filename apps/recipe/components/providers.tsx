"use client";

import { useAuth } from "@clerk/nextjs";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { AXIOS_INSTANCE } from "@/lib/api/axios-instance";

function AxiosTokenSync() {
	const { getToken } = useAuth();

	useEffect(() => {
		const interceptorId = AXIOS_INSTANCE.interceptors.request.use(
			async (config) => {
				const token = await getToken();
				if (token) {
					config.headers.Authorization = `Bearer ${token}`;
				}
				return config;
			},
			(error) => Promise.reject(error),
		);

		return () => {
			AXIOS_INSTANCE.interceptors.request.eject(interceptorId);
		};
	}, [getToken]);

	return null;
}

export function Providers({ children }: { children: React.ReactNode }) {
	const [queryClient] = useState(() => new QueryClient());

	return (
		<QueryClientProvider client={queryClient}>
			<AxiosTokenSync />
			{children}
		</QueryClientProvider>
	);
}
