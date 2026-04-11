"use client";

import { Button } from "@workspace/ui/components/shadcn/button";
import { Input } from "@workspace/ui/components/shadcn/input";
import { Search, X } from "lucide-react";
import { useEffect, useState } from "react";

interface RecipeSearchProps {
	value: string;
	onChange: (value: string) => void;
	onClear: () => void;
}

export function RecipeSearch({ value, onChange, onClear }: RecipeSearchProps) {
	const [localValue, setLocalValue] = useState(value);

	useEffect(() => {
		setLocalValue(value);
	}, [value]);

	useEffect(() => {
		const timer = setTimeout(() => {
			if (localValue !== value) {
				onChange(localValue);
			}
		}, 500);

		return () => clearTimeout(timer);
	}, [localValue, onChange, value]);

	return (
		<div className="relative w-full max-w-sm">
			<Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
			<Input
				type="search"
				placeholder="Search recipes..."
				className="pl-9"
				value={localValue}
				onChange={(e) => setLocalValue(e.target.value)}
			/>
			{localValue && (
				<Button
					type="button"
					variant="ghost"
					size="icon"
					onClick={() => {
						setLocalValue("");
						onClear();
					}}
					className="absolute right-0 top-0 h-full px-3 text-muted-foreground hover:text-foreground"
				>
					<X className="h-4 w-4" />
					<span className="sr-only">Clear search text</span>
				</Button>
			)}
		</div>
	);
}
