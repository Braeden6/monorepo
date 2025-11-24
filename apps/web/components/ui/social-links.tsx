"use client";

import { motion } from "framer-motion";
import { Github, Linkedin } from "lucide-react";
import Link from "next/link";

const socialLinks = [
	{
		name: "GitHub",
		icon: Github,
		href: "https://github.com/braeden6",
		color: "hover:text-white",
	},
	{
		name: "LinkedIn",
		icon: Linkedin,
		href: "https://www.linkedin.com/in/braeden6/",
		color: "hover:text-blue-600",
	},
];

export function SocialLinks() {
	return (
		<div className="flex gap-6">
			{socialLinks.map((social, index) => (
				<motion.div
					key={social.name}
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 0.5 + index * 0.1, duration: 0.5 }}
				>
					<Link
						href={social.href}
						target="_blank"
						rel="noopener noreferrer"
						className={`transition-colors duration-300 text-gray-400 ${social.color}`}
					>
						<social.icon className="h-6 w-6" />
						<span className="sr-only">{social.name}</span>
					</Link>
				</motion.div>
			))}
		</div>
	);
}
