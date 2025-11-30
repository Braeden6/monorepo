"use client";

import { motion, useMotionValue, useSpring } from "framer-motion";
import { ArrowLeft, Home, Sparkles } from "lucide-react";
import Link from "next/link";
import { useEffect } from "react";

export function NotFound() {
	const mouseX = useMotionValue(0);
	const mouseY = useMotionValue(0);

	const springConfig = { damping: 25, stiffness: 150, mass: 0.5 };
	const springX = useSpring(mouseX, springConfig);
	const springY = useSpring(mouseY, springConfig);

	useEffect(() => {
		const handleMouseMove = (e: MouseEvent) => {
			mouseX.set(e.clientX);
			mouseY.set(e.clientY);
		};

		window.addEventListener("mousemove", handleMouseMove);
		return () => window.removeEventListener("mousemove", handleMouseMove);
	}, [mouseX, mouseY]);

	const floatingAnimation = {
		y: [0, -20, 0],
		transition: {
			duration: 3,
			repeat: Number.POSITIVE_INFINITY as number,
			ease: "easeInOut" as const,
		},
	};

	const glowAnimation = {
		scale: [1, 1.2, 1],
		opacity: [0.5, 0.8, 0.5],
		transition: {
			duration: 2,
			repeat: Number.POSITIVE_INFINITY as number,
			ease: "easeInOut" as const,
		},
	};

	return (
		<div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background">
			{/* Animated background particles */}
			<div className="absolute inset-0">
				{[...Array(20)].map((_, i) => (
					<motion.div
						key={String(i)}
						className="absolute h-2 w-2 rounded-full bg-primary"
						initial={{
							x:
								typeof window !== "undefined"
									? Math.random() * window.innerWidth
									: 0,
							y:
								typeof window !== "undefined"
									? Math.random() * window.innerHeight
									: 0,
							opacity: Math.random() * 0.5,
						}}
						animate={{
							y:
								typeof window !== "undefined"
									? [null, Math.random() * window.innerHeight]
									: [0, 100],
							opacity: [null, Math.random() * 0.5],
						}}
						transition={{
							duration: Math.random() * 10 + 10,
							ease: "linear",
						}}
					/>
				))}
			</div>

			{/* Mouse follower glow */}
			<motion.div
				className="pointer-events-none fixed top-0 left-0 h-96 w-96 rounded-full bg-primary/20 blur-3xl"
				style={{
					x: springX,
					y: springY,
					translateX: "-50%",
					translateY: "-50%",
				}}
			/>

			{/* Main content */}
			<div className="relative z-10 px-4 text-center">
				{/* Animated 404 */}
				<motion.div
					className="mb-8"
					initial={{ opacity: 0, scale: 0.5 }}
					animate={{ opacity: 1, scale: 1 }}
					transition={{ duration: 0.5 }}
				>
					<motion.h1
						className="relative text-9xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary via-accent to-primary"
						animate={floatingAnimation}
					>
						404
						{/* Glowing effect behind text */}
						<motion.div
							className="absolute inset-0 -z-10 text-9xl font-bold text-primary blur-2xl"
							animate={glowAnimation}
						>
							404
						</motion.div>
					</motion.h1>
				</motion.div>

				{/* Sparkle icon */}
				<motion.div
					className="mb-6 flex justify-center"
					initial={{ opacity: 0, rotate: -180 }}
					animate={{ opacity: 1, rotate: 0 }}
					transition={{ delay: 0.3, duration: 0.8 }}
				>
					<motion.div
						animate={{
							rotate: [0, 360],
						}}
						transition={{
							duration: 20,
							repeat: Number.POSITIVE_INFINITY,
							ease: "linear",
						}}
					>
						<Sparkles className="h-16 w-16 text-primary" />
					</motion.div>
				</motion.div>

				{/* Text content */}
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 0.5, duration: 0.5 }}
				>
					<h2 className="mb-4 text-3xl font-bold text-foreground">
						Page Not Found
					</h2>
					<p className="mb-8 text-lg text-muted-foreground">
						Oops! The page you're looking for seems to have vanished into the
						void.
					</p>
				</motion.div>

				{/* Action buttons */}
				<motion.div
					className="flex flex-col gap-4 sm:flex-row sm:justify-center"
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 0.7, duration: 0.5 }}
				>
					<Link href="/">
						<motion.button
							className="group relative overflow-hidden rounded-lg bg-primary hover:bg-accent px-8 py-3 font-semibold text-primary-foreground shadow-lg transition-all hover:shadow-primary/50"
							whileHover={{ scale: 1.05 }}
							whileTap={{ scale: 0.95 }}
						>
							<span className="relative z-10 flex items-center gap-2 cursor-pointer">
								<Home className="h-5 w-5" />
								Go Home
							</span>
							<motion.div
								className="absolute inset-0 bg-gradient-to-r from-accent to-primary"
								initial={{ x: "100%" }}
								whileHover={{ x: 0 }}
								transition={{ duration: 0.3 }}
							/>
						</motion.button>
					</Link>

					<motion.button
						className="group relative overflow-hidden rounded-lg border-2 border-primary px-8 py-3 font-semibold text-primary transition-all hover:border-primary/80 hover:text-primary/80"
						whileHover={{ scale: 1.05 }}
						whileTap={{ scale: 0.95 }}
						onClick={() => window.history.back()}
					>
						<span className="relative z-10 flex items-center gap-2 cursor-pointer">
							<ArrowLeft className="h-5 w-5" />
							Go Back
						</span>
						<motion.div
							className="absolute inset-0 bg-primary/10"
							initial={{ x: "-100%" }}
							whileHover={{ x: 0 }}
							transition={{ duration: 0.3 }}
						/>
					</motion.button>
				</motion.div>

				{/* Floating decorative elements */}
				<div className="absolute left-1/2 top-1/2 -z-10 -translate-x-1/2 -translate-y-1/2">
					{[...Array(3)].map((_, i) => (
						<motion.div
							key={String(i)}
							className="absolute h-64 w-64 rounded-full border border-primary/20"
							initial={{ scale: 0, opacity: 0 }}
							animate={{
								scale: [1, 2, 3],
								opacity: [0.5, 0.2, 0],
							}}
							transition={{
								duration: 3,
								repeat: Number.POSITIVE_INFINITY,
								delay: i * 1,
								ease: "easeOut",
							}}
						/>
					))}
				</div>
			</div>
		</div>
	);
}
