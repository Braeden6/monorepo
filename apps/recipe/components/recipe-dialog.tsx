"use client";

import { useUser } from "@clerk/nextjs";
import { useQueryClient } from "@tanstack/react-query";
import { Badge } from "@workspace/ui/components/shadcn/badge";
import { Button } from "@workspace/ui/components/shadcn/button";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogHeader,
	DialogTitle,
} from "@workspace/ui/components/shadcn/dialog";
import { ScrollArea } from "@workspace/ui/components/shadcn/scroll-area";
import { Separator } from "@workspace/ui/components/shadcn/separator";
import { cn } from "@workspace/ui/lib/utils";
import { Heart, ThumbsUp } from "lucide-react";
import { toast } from "sonner";
import { env } from "@/env";
import {
	type RecipeRead,
	RecipeStatus,
	useToggleFavoriteUsersRecipesRecipeIdFavoritePost,
	useToggleLikeUsersRecipesRecipeIdLikePost,
	useUpdateRecipeRecipesRecipeIdPatch,
} from "@/lib/api/generated/recipeAPI";

interface RecipeDialogProps {
	recipe: RecipeRead;
	open: boolean;
	onOpenChange: (open: boolean) => void;
}

export function RecipeDialog({
	recipe,
	open,
	onOpenChange,
}: RecipeDialogProps) {
	const { user } = useUser();
	const queryClient = useQueryClient();

	const { mutate: toggleLike } = useToggleLikeUsersRecipesRecipeIdLikePost({
		mutation: {
			onSuccess: () => {
				queryClient.invalidateQueries({ queryKey: ["/recipes/"] });
			},
			onError: () => {
				toast.error("Failed to update like status");
			},
		},
	});

	const { mutate: toggleFavorite } =
		useToggleFavoriteUsersRecipesRecipeIdFavoritePost({
			mutation: {
				onSuccess: () => {
					queryClient.invalidateQueries({ queryKey: ["/recipes/"] });
				},
				onError: () => {
					toast.error("Failed to update favorite status");
				},
			},
		});

	const handleLike = (e: React.MouseEvent) => {
		e.stopPropagation();
		if (!user) {
			const redirectUrl = window.location.href;
			const loginUrl = `${env.NEXT_PUBLIC_AUTH_URL}/sign-in?redirect_url=${encodeURIComponent(
				redirectUrl,
			)}`;
			window.location.href = loginUrl;
			return;
		}
		toggleLike({ recipeId: recipe.id });
	};

	const handleFavorite = (e: React.MouseEvent) => {
		e.stopPropagation();
		if (!user) {
			const redirectUrl = window.location.href;
			const loginUrl = `${env.NEXT_PUBLIC_AUTH_URL}/sign-in?redirect_url=${encodeURIComponent(
				redirectUrl,
			)}`;
			window.location.href = loginUrl;
			return;
		}
		toggleFavorite({ recipeId: recipe.id });
	};

	const { mutate: updateRecipe, isPending: isUpdating } =
		useUpdateRecipeRecipesRecipeIdPatch({
			mutation: {
				onSuccess: () => {
					queryClient.invalidateQueries({ queryKey: ["/recipes/"] });
					toast.success("Recipe published successfully");
					onOpenChange(false);
				},
				onError: () => {
					toast.error("Failed to publish recipe");
				},
			},
		});

	const handlePublish = () => {
		updateRecipe({
			recipeId: recipe.id,
			data: { status: RecipeStatus.PUBLISHED },
		});
	};

	return (
		<Dialog open={open} onOpenChange={onOpenChange}>
			<DialogContent className="max-h-[90vh] w-[min(96vw,720px)] flex flex-col gap-0 border border-primary/60 p-0 overflow-hidden">
				<div className="border-b px-6 py-5">
					<DialogHeader className="gap-4">
						<div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
							<div className="min-w-0">
								<DialogTitle className="flex flex-wrap items-center gap-2 text-2xl font-semibold">
									<span className="break-words">{recipe.name}</span>
									{recipe.status === RecipeStatus.DRAFT && (
										<Badge variant="outline" className="text-muted-foreground">
											Draft
										</Badge>
									)}
								</DialogTitle>
								{recipe.food_type && (
									<Badge variant="secondary" className="mt-2 capitalize">
										{recipe.food_type.toLowerCase()}
									</Badge>
								)}
							</div>
							<div className="flex flex-wrap items-center gap-2 sm:justify-end">
								{user?.id === recipe.created_by &&
									recipe.status === RecipeStatus.DRAFT && (
										<Button
											onClick={handlePublish}
											disabled={isUpdating}
											size="sm"
											className="whitespace-nowrap"
										>
											{isUpdating ? "Publishing..." : "Publish"}
										</Button>
									)}
								<Button
									variant="ghost"
									size="icon"
									className={cn(
										"h-9 w-9 shrink-0",
										recipe.is_liked && "text-blue-500",
									)}
									onClick={handleLike}
								>
									<ThumbsUp
										className={cn("h-5 w-5", recipe.is_liked && "fill-current")}
									/>
									<span className="sr-only">Like</span>
								</Button>
								<Button
									variant="ghost"
									size="icon"
									className={cn(
										"h-9 w-9 shrink-0",
										recipe.is_favorited && "text-red-500",
									)}
									onClick={handleFavorite}
								>
									<Heart
										className={cn(
											"h-5 w-5",
											recipe.is_favorited && "fill-current",
										)}
									/>
									<span className="sr-only">Favorite</span>
								</Button>
							</div>
						</div>
						<DialogDescription className="break-words text-base leading-6 text-muted-foreground">
							{recipe.description}
						</DialogDescription>
					</DialogHeader>
				</div>
				<ScrollArea className="flex-1 min-h-0">
					<div className="space-y-6 p-6">
						<div>
							<h3 className="mb-3 text-lg font-semibold">Ingredients</h3>
							<div className="grid gap-3 sm:grid-cols-2">
								{recipe.ingredients.map((ingredient) => (
									<div
										key={ingredient.name}
										className="flex items-start gap-2 rounded-md border bg-muted/50 p-3 text-sm leading-snug"
									>
										<div className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
										<span className="min-w-0 break-words">
											{ingredient.amount} {ingredient.unit} {ingredient.name}
										</span>
									</div>
								))}
							</div>
						</div>

						<Separator />

						<div>
							<h3 className="mb-3 text-lg font-semibold">Instructions</h3>
							<div className="whitespace-pre-wrap break-words text-sm leading-6 text-muted-foreground">
								{recipe.instructions}
							</div>
						</div>

						<div className="mt-6 flex flex-col gap-2 border-t py-4 text-xs text-muted-foreground sm:flex-row sm:items-center sm:justify-between">
							<div>
								Created: {new Date(recipe.created_at).toLocaleDateString()}
							</div>
							<div className="flex flex-wrap gap-4">
								<span>{recipe.like_count} likes</span>
								<span>{recipe.favorite_count} favorites</span>
							</div>
						</div>
					</div>
				</ScrollArea>
			</DialogContent>
		</Dialog>
	);
}
