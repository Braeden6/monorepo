"use client";

import { SignedIn, SignedOut, UserButton } from "@clerk/nextjs";
import { BorderBeam } from "@workspace/ui/components/shadcn/border-beam";
import { Button } from "@workspace/ui/components/shadcn/button";
import { ShimmerButton } from "@workspace/ui/components/shadcn/shimmer-button";
import { motion } from "framer-motion";
import Link from "next/link";

export default function Home() {
	return (
		<div className="relative flex flex-col items-center gap-8">
			<motion.div
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 0.8, ease: "easeOut" }}
				className="relative flex flex-col items-center justify-center overflow-hidden rounded-xl border border-border bg-card/30 px-10 py-14 text-center shadow-2xl backdrop-blur-md sm:px-16"
			>
				<div className="z-10 flex flex-col items-center gap-6">
					<div className="space-y-2">
						<h1 className="bg-gradient-to-b from-foreground to-muted-foreground bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-6xl">
							Auth Service
						</h1>
						<p className="max-w-[400px] text-lg text-muted-foreground">
							Secure, fast, and simple authentication.
						</p>
					</div>

					<SignedIn>
						<div className="flex flex-col items-center gap-4">
							<div className="rounded-full border border-border bg-card/30 p-2 backdrop-blur-sm">
								<UserButton
									appearance={{
										elements: {
											avatarBox: "h-12 w-12",
										},
									}}
								/>
							</div>
							<p className="text-muted-foreground">Welcome back!</p>
						</div>
					</SignedIn>

					<SignedOut>
						<div className="flex flex-col gap-4 sm:flex-row">
							<Link href="/sign-in">
								<ShimmerButton className="shadow-2xl">
									<span className="whitespace-pre-wrap text-center text-sm font-medium leading-none tracking-tight text-primary-foreground dark:from-primary-foreground dark:to-primary/10 lg:text-lg">
										Sign In
									</span>
								</ShimmerButton>
							</Link>
							<Link href="/sign-up">
								<Button
									type="button"
									className="group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-full bg-secondary px-8 font-medium text-secondary-foreground transition-all duration-300 hover:bg-secondary/80 hover:text-foreground cursor-pointer"
								>
									<span className="mr-2">Create Account</span>
									<span className="transition-transform duration-300 group-hover:translate-x-1">
										→
									</span>
									<div className="absolute inset-0 -z-10 rounded-full bg-gradient-to-r from-primary/20 to-primary/10 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
								</Button>
							</Link>
						</div>
					</SignedOut>
				</div>
				<BorderBeam size={250} duration={12} delay={9} />
			</motion.div>
		</div>
	);
}
