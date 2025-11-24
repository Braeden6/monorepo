"use client";

import { motion } from "framer-motion";
import { Code2, Cpu, Globe, User } from "lucide-react";
import { AnimatedText } from "@/components/ui/animated-text";
import { CardCarousel } from "@/components/ui/card-carousel";
import { RetroGrid } from "@/components/ui/retro-grid";
import { SocialLinks } from "@/components/ui/social-links";

const carouselItems = [
	{
		id: "about",
		title: "About Me",
		description:
			"My journey, skills, and philosophy on building digital products.",
		icon: User,
		color: "from-blue-500 to-cyan-500",
		spotlight: "rgba(59, 130, 246, 0.25)",
	},
	{
		id: "blog",
		title: "The Blog",
		description:
			"Thoughts on software engineering, design patterns, and the future.",
		icon: Globe,
		color: "from-purple-500 to-pink-500",
		spotlight: "rgba(168, 85, 247, 0.25)",
	},
	{
		id: "projects",
		title: "Projects",
		description:
			"A showcase of my recent work, open source contributions, and experiments.",
		icon: Cpu,
		color: "from-emerald-500 to-lime-500",
		spotlight: "rgba(16, 185, 129, 0.25)",
	},
];

export default function Page() {
	return (
		<div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-black text-white selection:bg-purple-500/30">
			{/* Vibrant Background Orbs */}
			<div className="absolute inset-0 z-0 overflow-hidden">
				<div className="absolute -left-[10%] top-[20%] h-[500px] w-[500px] rounded-full bg-purple-600/20 blur-[120px]" />
				<div className="absolute -right-[10%] bottom-[20%] h-[500px] w-[500px] rounded-full bg-blue-600/20 blur-[120px]" />
				<div className="absolute left-[50%] top-[50%] h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-indigo-500/10 blur-[100px]" />
			</div>

			{/* Retro Grid Background */}
			<RetroGrid className="z-0 opacity-60" />

			{/* Content */}
			<div className="relative z-10 flex w-full max-w-5xl flex-col items-center px-4 text-center">
				{/* Hero Section */}
				<motion.div
					initial={{ opacity: 0, scale: 0.9 }}
					animate={{ opacity: 1, scale: 1 }}
					transition={{ duration: 0.8, ease: "easeOut" }}
					className="mb-8 flex items-center justify-center gap-2 rounded-full bg-white/5 px-4 py-1.5 text-sm font-medium text-white/90 backdrop-blur-md ring-1 ring-white/20 transition-all hover:bg-white/10 hover:ring-white/30"
				>
					<Code2 className="h-4 w-4 text-purple-400" />
					<span>Full Stack Developer</span>
				</motion.div>

				<AnimatedText
					text={["Braeden"]}
					className="mb-2 text-6xl font-extrabold tracking-tight sm:text-8xl md:text-9xl bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"
				/>

				<AnimatedText
					text={["Software Engineer"]}
					className="mb-8 text-2xl font-semibold tracking-wide text-gray-300 sm:text-4xl md:text-5xl"
					repeatDelay={5000}
				/>

				<motion.p
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 1.2, duration: 0.8 }}
					className="mb-12 max-w-2xl text-lg text-gray-400 sm:text-xl leading-relaxed"
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
