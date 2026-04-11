"use client";

import { UserButton, useUser } from "@clerk/nextjs";
import { SignInButton } from "@workspace/ui/components/shared/sign-in-button";
import { Loader2 } from "lucide-react";

export function Header() {
	const { isSignedIn, isLoaded } = useUser();

	return (
		<header className="flex items-center justify-between border-b px-6 py-4">
			<div className="flex items-center gap-2 font-bold text-xl">
				Recipe Generator
			</div>
			{!isLoaded ? (
				<Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
			) : isSignedIn ? (
				<UserButton />
			) : (
				<SignInButton>Login</SignInButton>
			)}
		</header>
	);
}
