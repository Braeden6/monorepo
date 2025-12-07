"use client";

import { SignedIn, UserButton } from "@clerk/nextjs";
import { AnimatedText } from "@workspace/ui/components/react-bits/animated-text";
import { RetroGrid } from "@workspace/ui/components/react-bits/retro-grid";
import { Meteors } from "@workspace/ui/components/shadcn/meteors";
import { motion } from "framer-motion";
import { Code2, Cpu, Globe, User } from "lucide-react";
import { CreateTokenButton } from "@/components/create-token-button";
import { CardCarousel } from "@/components/ui/card-carousel";
import { SocialLinks } from "@/components/ui/social-links";

const carouselItems = [
	{
		id: "about",
		title: "About Me",
		description:
			"My journey, skills, and philosophy on building digital products.",
		icon: User,
		color: "from-primary to-accent",
		spotlight: "rgba(168, 85, 247, 0.25)" as const, // Primary-ish
	},
	{
		id: "blog",
		title: "The Blog",
		description:
			"Thoughts on software engineering, design patterns, and the future.",
		icon: Globe,
		color: "from-accent to-secondary",
		spotlight: "rgba(236, 72, 153, 0.25)" as const, // Accent-ish
	},
	{
		id: "projects",
		title: "Projects",
		description:
			"A showcase of my recent work, open source contributions, and experiments.",
		icon: Cpu,
		color: "from-secondary to-primary",
		spotlight: "rgba(34, 197, 94, 0.25)" as const, // Secondary-ish
	},
];

export default function Page() {
	return (
		<div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-background text-foreground selection:bg-primary/30">
			{/* Vibrant Background Orbs */}
			<div className="absolute inset-0 z-0 overflow-hidden">
				<div className="absolute -left-[10%] top-[20%] h-[500px] w-[500px] rounded-full bg-primary/20 blur-[120px]" />
				<div className="absolute -right-[10%] bottom-[20%] h-[500px] w-[500px] rounded-full bg-secondary/20 blur-[120px]" />
				<div className="absolute left-[50%] top-[50%] h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-accent/10 blur-[100px]" />
			</div>

			{/* Retro Grid Background */}
			<RetroGrid className="z-0 opacity-60" />
			<div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
				<Meteors number={40} />
			</div>

			<div className="absolute top-4 right-4 z-50">
				<SignedIn>
					<div className="flex items-center gap-4">
						<CreateTokenButton />
						<UserButton />
					</div>
				</SignedIn>
			</div>

			{/* Content */}
			<div className="relative z-10 flex w-full max-w-5xl flex-col items-center px-4 text-center">
				{/* Hero Section */}
				<motion.div
					initial={{ opacity: 0, scale: 0.9 }}
					animate={{ opacity: 1, scale: 1 }}
					transition={{ duration: 0.8, ease: "easeOut" }}
					className="mb-8 flex items-center justify-center gap-2 rounded-full bg-card/30 px-4 py-1.5 text-sm font-medium text-foreground/90 backdrop-blur-md ring-1 ring-border transition-all hover:bg-card/50 hover:ring-border"
				>
					<Code2 className="h-4 w-4 text-primary" />
					<span>Full Stack Developer</span>
				</motion.div>

				<AnimatedText
					text={["Braeden"]}
					className="mb-2 text-6xl font-extrabold tracking-tight sm:text-8xl md:text-9xl bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent"
				/>

				<AnimatedText
					text={["Software Engineer"]}
					className="mb-8 text-2xl font-semibold tracking-wide text-muted-foreground sm:text-4xl md:text-5xl"
					repeatDelay={5000}
				/>

				<motion.p
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 1.2, duration: 0.8 }}
					className="mb-12 max-w-2xl text-lg text-muted-foreground sm:text-xl leading-relaxed"
				>
					Crafting robust and scalable digital experiences. Focused on
					performance, accessibility, and modern UI/UX.
				</motion.p>

				<div className="mb-20">
					<SocialLinks />
				</div>

				{/* Carousel */}
				<motion.div
					initial={{ opacity: 0, y: 40 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 1.5, duration: 0.8 }}
					className="w-full max-w-4xl"
				>
					<CardCarousel items={carouselItems} />
				</motion.div>
			</div>
		</div>
	);
}
