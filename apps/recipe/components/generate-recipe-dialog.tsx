"use client";

import { useUser } from "@clerk/nextjs";
import { useQueryClient } from "@tanstack/react-query";
import { Button } from "@workspace/ui/components/shadcn/button";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
} from "@workspace/ui/components/shadcn/dialog";
import { Label } from "@workspace/ui/components/shadcn/label";
import { Textarea } from "@workspace/ui/components/shadcn/textarea";
import { Loader2, Sparkles } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import {
	useGetGenerationStatusGenerateWorkflowIdGet,
	useStartGenerationGeneratePost,
} from "@/lib/api/generated/recipeAPI";

interface GenerateRecipeDialogProps {
	open: boolean;
	onOpenChange: (open: boolean) => void;
}

export function GenerateRecipeDialog({
	open,
	onOpenChange,
}: GenerateRecipeDialogProps) {
	const { user } = useUser();
	const [prompt, setPrompt] = useState("");
	const [workflowId, setWorkflowId] = useState<string | null>(null);
	const queryClient = useQueryClient();

	const { mutate: generate, isPending: isStarting } =
		useStartGenerationGeneratePost({
			mutation: {
				onSuccess: (data) => {
					setWorkflowId(data.workflow_id);
				},
				onError: () => {
					toast.error("Failed to start generation");
				},
			},
		});

	const { data: status } = useGetGenerationStatusGenerateWorkflowIdGet(
		workflowId ?? "",
		{
			query: {
				enabled: !!workflowId,
				refetchInterval: (query) => {
					const data = query.state.data;
					if (data?.status === "completed" || data?.status === "failed") {
						return false;
					}
					return 1000;
				},
			},
		},
	);

	// Handle completion
	if (status?.status === "completed" && workflowId) {
		setWorkflowId(null);
		setPrompt("");
		onOpenChange(false);
		toast.success("Recipes generated successfully!");
		queryClient.invalidateQueries({ queryKey: ["/recipes/"] });
	}

	if (status?.status === "failed" && workflowId) {
		setWorkflowId(null);
		toast.error(status.error || "Generation failed");
	}

	const handleGenerate = () => {
		if (!user) {
			toast.error("You must be logged in to generate recipes");
			return;
		}
		if (!prompt.trim()) {
			toast.error("Please enter a prompt");
			return;
		}

		generate({
			data: {
				prompt,
				amount: 3,
			},
		});
	};

	const isLoading =
		isStarting ||
		(!!workflowId &&
			status?.status !== "completed" &&
			status?.status !== "failed");

	return (
		<Dialog open={open} onOpenChange={onOpenChange}>
			<DialogContent className="sm:max-w-[425px]">
				<DialogHeader>
					<DialogTitle className="flex items-center gap-2">
						<Sparkles className="h-5 w-5 text-primary" />
						Generate Recipes
					</DialogTitle>
					<DialogDescription>
						Describe what you want to cook, and AI will generate 3 unique
						recipes for you.
					</DialogDescription>
				</DialogHeader>
				<div className="grid gap-4 py-4">
					<div className="grid gap-2">
						<Label htmlFor="prompt">What are you craving?</Label>
						<Textarea
							id="prompt"
							placeholder="e.g., A healthy chicken dinner with mediterranean flavors..."
							value={prompt}
							onChange={(e) => setPrompt(e.target.value)}
							rows={4}
							disabled={isLoading}
						/>
					</div>
					{isLoading && (
						<div className="flex flex-col items-center justify-center gap-2 py-4">
							<Loader2 className="h-8 w-8 animate-spin text-primary" />
							<p className="text-sm text-muted-foreground animate-pulse">
								{status?.current_step
									? `Status: ${status.current_step}...`
									: "Starting generation..."}
							</p>
						</div>
					)}
				</div>
				<DialogFooter>
					<Button
						type="submit"
						onClick={handleGenerate}
						disabled={isLoading || !prompt.trim()}
					>
						{isLoading ? "Generating..." : "Generate"}
					</Button>
				</DialogFooter>
			</DialogContent>
		</Dialog>
	);
}
