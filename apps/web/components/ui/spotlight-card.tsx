"use client";

import { Card } from "@workspace/ui/components/shadcn/card";
import { motion } from "framer-motion";
import { type MouseEvent, useRef, useState } from "react";

export const SpotlightCard = ({
	children,
	className = "",
	spotlightColor = "rgba(255, 255, 255, 0.25)",
}: {
	children: React.ReactNode;
	className?: string;
	spotlightColor?: string;
}) => {
	const divRef = useRef<HTMLDivElement>(null);
	const [position, setPosition] = useState({ x: 0, y: 0 });
	const [opacity, setOpacity] = useState(0);

	const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
		if (!divRef.current) return;

		const div = divRef.current;
		const rect = div.getBoundingClientRect();

		setPosition({ x: e.clientX - rect.left, y: e.clientY - rect.top });
	};

	const handleFocus = () => {
		setOpacity(1);
	};

	const handleBlur = () => {
		setOpacity(0);
	};

	const handleMouseEnter = () => {
		setOpacity(1);
	};

	const handleMouseLeave = () => {
		setOpacity(0);
	};

	return (
		<Card
			ref={divRef}
			onMouseMove={handleMouseMove}
			onFocus={handleFocus}
			onBlur={handleBlur}
			onMouseEnter={handleMouseEnter}
			onMouseLeave={handleMouseLeave}
			className={`relative overflow-hidden rounded-2xl border border-border ${className}`}
		>
			<motion.div
				className="pointer-events-none absolute -inset-px z-10 opacity-0 transition-opacity duration-300"
				style={{
					opacity,
					background: `radial-gradient(600px circle at ${position.x}px ${position.y}px, ${spotlightColor}, transparent 40%)`,
				}}
			/>
			<div className="relative z-20 h-full">{children}</div>
		</Card>
	);
};
