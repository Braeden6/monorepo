import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Script from "next/script";

import { Providers } from "@/components/providers";
import "@workspace/ui/globals.css";
import "./custom.css";

export const metadata: Metadata = {
	title: "Braeden's Web App",
	description: "Personal web application",
	icons: {
		icon: [{ url: "/logo.svg", type: "image/svg+xml" }],
		apple: [{ url: "/logo.svg", type: "image/svg+xml" }],
	},
};

const fontSans = Geist({
	subsets: ["latin"],
	variable: "--font-sans",
});

const fontMono = Geist_Mono({
	subsets: ["latin"],
	variable: "--font-mono",
});

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en" suppressHydrationWarning>
			<body
				className={`${fontSans.variable} ${fontMono.variable} font-sans antialiased`}
			>
				<Providers>{children}</Providers>
				{/* No best practice to have id hardcode, but 🤷 */}
				<Script
					src="https://umami.braeden6.com/script.js"
					data-website-id="8547cec2-6e15-47e4-825e-48524c3bd914"
					strategy="afterInteractive"
				/>
			</body>
		</html>
	);
}
