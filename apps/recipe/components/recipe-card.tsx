"use client";

import { useUser } from "@clerk/nextjs";
import { useQueryClient } from "@tanstack/react-query";
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
	AlertDialogTrigger,
} from "@workspace/ui/components/shadcn/alert-dialog";
import { Badge } from "@workspace/ui/components/shadcn/badge";
import { Button } from "@workspace/ui/components/shadcn/button";
import {
	Card,
	CardContent,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@workspace/ui/components/shadcn/card";
import { cn } from "@workspace/ui/lib/utils";
import { Heart, ThumbsUp, Trash2 } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { env } from "@/env";
import {
	type RecipeRead,
	useDeleteRecipeRecipesRecipeIdDelete,
	useToggleFavoriteUsersRecipesRecipeIdFavoritePost,
	useToggleLikeUsersRecipesRecipeIdLikePost,
} from "@/lib/api/generated/recipeAPI";
import { RecipeDialog } from "./recipe-dialog";

interface RecipeCardProps {
	recipe: RecipeRead;
}

export function RecipeCard({ recipe }: RecipeCardProps) {
	const { user } = useUser();
	const [showDetails, setShowDetails] = useState(false);
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

	const { mutate: deleteRecipe, isPending: isDeleting } =
		useDeleteRecipeRecipesRecipeIdDelete({
			mutation: {
				onSuccess: () => {
					queryClient.invalidateQueries({ queryKey: ["/recipes/"] });
					toast.success("Recipe deleted");
				},
				onError: () => {
					toast.error("Failed to delete recipe");
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

	const handleDelete = (e: React.MouseEvent) => {
		e.stopPropagation();
		deleteRecipe({ recipeId: recipe.id });
	};

	return (
		<>
			<Card
				className="group relative overflow-hidden transition-all hover:shadow-lg cursor-pointer hover:border-primary/50"
				onClick={() => setShowDetails(true)}
			>
				<CardHeader className="pb-4">
					<div className="flex items-start justify-between gap-4">
						<CardTitle className="line-clamp-1 text-xl">
							{recipe.name}
						</CardTitle>
						{recipe.food_type && (
							<Badge variant="outline" className="capitalize shrink-0">
								{recipe.food_type.toLowerCase()}
							</Badge>
						)}
					</div>
				</CardHeader>
				<CardContent className="pb-4">
					<p className="line-clamp-3 text-sm text-muted-foreground">
						{recipe.description}
					</p>
					<div className="mt-4 flex flex-wrap gap-2">
						{recipe.ingredients.slice(0, 3).map((ingredient, i) => (
							<Badge
								key={`${ingredient.name}-${i}`}
								variant="secondary"
								className="text-xs font-normal"
							>
								{ingredient.name}
							</Badge>
						))}
						{recipe.ingredients.length > 3 && (
							<Badge variant="secondary" className="text-xs font-normal">
								+{recipe.ingredients.length - 3} more
							</Badge>
						)}
					</div>
				</CardContent>
				<CardFooter className="pt-0">
					<div className="flex w-full items-center justify-between text-muted-foreground">
						<div className="flex gap-4 text-xs">
							<span className="flex items-center gap-1">
								<ThumbsUp className="h-3 w-3" />
								{recipe.like_count}
							</span>
							<span className="flex items-center gap-1">
								<Heart className="h-3 w-3" />
								{recipe.favorite_count}
							</span>
						</div>
						<div className="flex gap-1">
							{user?.id === recipe.created_by && (
								<AlertDialog>
									<AlertDialogTrigger asChild>
										<Button
											variant="ghost"
											size="icon"
											className="h-8 w-8 text-destructive hover:text-destructive/80 hover:bg-destructive/10"
											onClick={(e) => e.stopPropagation()}
											disabled={isDeleting}
										>
											<Trash2 className="h-4 w-4" />
											<span className="sr-only">Delete</span>
										</Button>
									</AlertDialogTrigger>
									<AlertDialogContent onClick={(e) => e.stopPropagation()}>
										<AlertDialogHeader>
											<AlertDialogTitle>
												Are you absolutely sure?
											</AlertDialogTitle>
											<AlertDialogDescription>
												This action cannot be undone. This will permanently
												delete your recipe "{recipe.name}".
											</AlertDialogDescription>
										</AlertDialogHeader>
										<AlertDialogFooter>
											<AlertDialogCancel>Cancel</AlertDialogCancel>
											<AlertDialogAction
												onClick={handleDelete}
												className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
											>
												Delete
											</AlertDialogAction>
										</AlertDialogFooter>
									</AlertDialogContent>
								</AlertDialog>
							)}
							<Button
								variant="ghost"
								size="icon"
								className={cn(
									"h-8 w-8",
									recipe.is_liked && "text-blue-500 hover:text-blue-600",
								)}
								onClick={handleLike}
							>
								<ThumbsUp
									className={cn("h-4 w-4", recipe.is_liked && "fill-current")}
								/>
								<span className="sr-only">Like</span>
							</Button>
							<Button
								variant="ghost"
								size="icon"
								className={cn(
									"h-8 w-8",
									recipe.is_favorited && "text-red-500 hover:text-red-600",
								)}
								onClick={handleFavorite}
							>
								<Heart
									className={cn(
										"h-4 w-4",
										recipe.is_favorited && "fill-current",
									)}
								/>
								<span className="sr-only">Favorite</span>
							</Button>
						</div>
					</div>
				</CardFooter>
			</Card>

			<RecipeDialog
				recipe={recipe}
				open={showDetails}
				onOpenChange={setShowDetails}
			/>
		</>
	);
}
