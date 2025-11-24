import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

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
			</body>
		</html>
	);
}
