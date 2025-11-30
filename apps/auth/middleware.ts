import { clerkMiddleware } from "@clerk/nextjs/server";
import { env } from "@workspace/ui/env";

export default clerkMiddleware({
	authorizedParties: [env.NEXT_PUBLIC_DOMAIN],
});

export const config = {
	matcher: [
		"/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
		"/(api|trpc)(.*)",
	],
};
