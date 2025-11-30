"use client";

import { BorderBeam } from "@workspace/ui/components/shadcn/border-beam";
import { motion } from "framer-motion";
import type { ReactNode } from "react";

export function AuthCard({ children }: { children: ReactNode }) {
	return (
		<motion.div
			initial={{ opacity: 0, scale: 0.95 }}
			animate={{ opacity: 1, scale: 1 }}
			transition={{ duration: 0.5, ease: "easeOut" }}
			className="relative overflow-hidden rounded-[1.25rem] border border-border bg-card/40 p-2 shadow-2xl backdrop-blur-xl"
		>
			<div className="relative z-10">{children}</div>
			<BorderBeam size={300} duration={15} delay={0} borderWidth={2} />
		</motion.div>
	);
}
