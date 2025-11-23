"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";
import React, { useRef, useState, useEffect } from "react";
import { SpotlightCard } from "./spotlight-card";

type CardItem = {
    id: string;
    title: string;
    description: string;
    icon: LucideIcon;
    color: string;
    spotlight: string;
};

type CardCarouselProps = {
    items: CardItem[];
};

export function CardCarousel({ items }: CardCarouselProps) {
    const carouselRef = useRef<HTMLDivElement>(null);
    const [width, setWidth] = useState(0);

    useEffect(() => {
        if (carouselRef.current) {
            setWidth(
                carouselRef.current.scrollWidth - carouselRef.current.offsetWidth
            );
        }
    }, [items]);

    return (
        <div className="w-full overflow-hidden px-4 sm:px-0">
            <motion.div
                ref={carouselRef}
                className="flex cursor-grab gap-6 active:cursor-grabbing"
                drag="x"
                dragConstraints={{ right: 0, left: -width }}
                whileTap={{ cursor: "grabbing" }}
            >
                {items.map((item) => (
                    <motion.div key={item.id} className="h-[250px] w-[280px] flex-shrink-0">
                        <SpotlightCard
                            className="h-full p-6 backdrop-blur-sm transition-all hover:bg-white/10"
                            spotlightColor={item.spotlight}
                        >
                            <div
                                className={`absolute inset-0 -z-10 bg-gradient-to-br ${item.color} opacity-0 transition-opacity duration-500 group-hover:opacity-20`}
                            />

                            <div className="mb-4 flex items-center justify-between">
                                <div className="rounded-full bg-white/10 p-2 ring-1 ring-white/20">
                                    <item.icon className="h-5 w-5 text-white" />
                                </div>
                                <span className="rounded-full bg-white/10 px-2 py-1 text-[10px] font-medium uppercase tracking-wider text-white/60 ring-1 ring-white/10">
                                    Coming Soon
                                </span>
                            </div>

                            <h3 className="mb-2 text-xl font-bold text-white">{item.title}</h3>
                            <p className="text-sm text-gray-400">{item.description}</p>

                            <div className="absolute bottom-6 left-6 right-6 h-1 rounded-full bg-white/10">
                                <motion.div
                                    className="h-full rounded-full bg-white/40"
                                    initial={{ width: "0%" }}
                                    whileHover={{ width: "100%" }}
                                    transition={{ duration: 0.3 }}
                                />
                            </div>
                        </SpotlightCard>
                    </motion.div>
                ))}
            </motion.div>
        </div>
    );
}
