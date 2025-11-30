import { ClerkProvider } from "@clerk/nextjs";
import { dark } from "@clerk/themes";
import { Meteors } from "@workspace/ui/components/shadcn/meteors";
import { env } from "@workspace/ui/env";
import "@workspace/ui/globals.css";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Script from "next/script";

export const metadata: Metadata = {
	title: "Braeden's Auth App",
	description: "Authentication for Braeden6 apps",
	icons: {
		icon: [{ url: "/icon.svg", type: "image/svg+xml" }],
		apple: [{ url: "/icon.svg", type: "image/svg+xml" }],
	},
};

const geistSans = Geist({
	variable: "--font-geist-sans",
	subsets: ["latin"],
});

const geistMono = Geist_Mono({
	variable: "--font-geist-mono",
	subsets: ["latin"],
});

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<ClerkProvider
			appearance={{
				baseTheme: dark,
				variables: { colorPrimary: "#a855f7" },
			}}
			allowedRedirectOrigins={env.NEXT_PUBLIC_REDIRECT_URL.split(",")}
		>
			<html lang="en" className="dark">
				<body
					className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-background text-foreground selection:bg-primary/30`}
				>
					<div className="fixed inset-0 -z-10 overflow-hidden">
						<div className="absolute -left-[10%] top-[20%] h-[500px] w-[500px] rounded-full bg-primary/20 blur-[120px]" />
						<div className="absolute -right-[10%] bottom-[20%] h-[500px] w-[500px] rounded-full bg-secondary/20 blur-[120px]" />
						<div className="absolute left-[50%] top-[50%] h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-accent/10 blur-[100px]" />
					</div>

					<div className="fixed inset-0 -z-10 overflow-hidden">
						<Meteors number={40} />
					</div>
					<main className="relative z-10 flex min-h-screen flex-col items-center justify-center">
						{children}
					</main>
					<Script
						src="https://umami.braeden6.com/script.js"
						data-website-id={env.NEXT_PUBLIC_UMAMI_WEBSITE_ID}
						strategy="afterInteractive"
					/>
				</body>
			</html>
		</ClerkProvider>
	);
}
