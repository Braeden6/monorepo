"use client";

import { env } from "@workspace/ui/env";
import { Button } from "../shadcn/button";

export function SignInButton(props: React.ComponentProps<typeof Button>) {
	const handleLogin = () => {
		const redirectUrl = window.location.href;
		const loginUrl = `${env.NEXT_PUBLIC_AUTH_URL}/sign-in?redirect_url=${encodeURIComponent(
			redirectUrl,
		)}`;
		window.location.href = loginUrl;
	};

	return (
		<Button onClick={handleLogin} {...props}>
			{props.children || "Sign In"}
		</Button>
	);
}
