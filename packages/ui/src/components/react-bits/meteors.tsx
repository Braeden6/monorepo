"use client";

import { cn } from "@workspace/ui/lib/utils.js";
import React, { useEffect, useState } from "react";

interface MeteorsProps {
	number?: number;
	className?: string;
}

export const Meteors = ({ number = 20, className }: MeteorsProps) => {
	const [meteorStyles, setMeteorStyles] = useState<Array<React.CSSProperties>>(
		[],
	);

	useEffect(() => {
		const styles = [...new Array(number)].map(() => ({
			top: Math.floor(Math.random() * -150) + "px", // Spawn from -150px to 0px
			left: Math.floor(Math.random() * (window.innerWidth + 800) - 400) + "px", // Spawn from -400px to width+400px
			animationDelay: Math.random() * 1 + 0.2 + "s",
			animationDuration: Math.floor(Math.random() * 8 + 2) + "s",
		}));
		setMeteorStyles(styles);
	}, [number]);

	return (
		<>
			{meteorStyles.map((style, idx) => (
				// biome-ignore lint/suspicious/noArrayIndexKey: <explanation>
				<span
					key={idx}
					className={cn(
						"pointer-events-none absolute left-1/2 top-1/2 h-1 w-1 rotate-[215deg] animate-meteor rounded-[9999px] bg-white shadow-[0_0_0_1px_#ffffff10]",
						className,
					)}
					style={style}
				>
					{/* Meteor Tail */}
					<div className="pointer-events-none absolute top-1/2 -z-10 h-[1px] w-[50px] -translate-y-1/2 bg-gradient-to-r from-white to-transparent" />
				</span>
			))}
		</>
	);
};
