"use client";

import { useUser } from "@clerk/nextjs";
import { Button } from "@workspace/ui/components/shadcn/button";
import { env } from "@workspace/ui/env";
import { Loader2, Plus, X } from "lucide-react";
import { useState } from "react";

import { GenerateRecipeDialog } from "@/components/generate-recipe-dialog";
import { RecipeCard } from "@/components/recipe-card";
import { RecipeFilters } from "@/components/recipe-filters";
import { RecipeSearch } from "@/components/recipe-search";
import {
	type FoodType,
	type SortField,
	type SortOrder,
	useListRecipesRecipesGet,
} from "@/lib/api/generated/recipeAPI";

export default function Page() {
	const { user } = useUser();
	const [isGenerateOpen, setIsGenerateOpen] = useState(false);
	const [query, setQuery] = useState("");
	const [foodTypes, setFoodTypes] = useState<FoodType[]>([]);
	const [sortBy, setSortBy] = useState<SortField>("created_at");
	const [sortOrder, setSortOrder] = useState<SortOrder>("desc");
	const [onlyMine, setOnlyMine] = useState(false);
	const [onlyFavorites, setOnlyFavorites] = useState(false);

	const {
		data: recipeResponse,
		isLoading,
		error: listError,
	} = useListRecipesRecipesGet({
		query: query || undefined,
		food_types: foodTypes.length > 0 ? foodTypes : undefined,
		sort_by: sortBy,
		sort_order: sortOrder,
		only_mine: onlyMine,
		only_favorites: onlyFavorites,
	});

	const handleSearch = (newQuery: string) => {
		setQuery(newQuery);
	};

	const handleClearSearch = () => {
		setQuery("");
		setFoodTypes([]);
		setSortBy("created_at");
		setSortOrder("desc");
		setOnlyMine(false);
		setOnlyFavorites(false);
	};

	const recipes = recipeResponse?.results;
	const isSearching =
		query !== "" || foodTypes.length > 0 || onlyMine || onlyFavorites;

	if (listError) {
		return (
			<div className="flex h-[50vh] w-full items-center justify-center text-destructive">
				Error loading recipes
			</div>
		);
	}

	return (
		<div className="container mx-auto py-10 px-4">
			<div className="flex flex-col gap-8">
				<div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
					<div>
						<h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent pb-2">
							Recipes
						</h1>
						<p className="text-muted-foreground mt-1">
							Discover and generate delicious recipes with AI.
						</p>
					</div>
					<div className="flex items-center gap-4">
						<Button
							onClick={() => {
								if (!user) {
									const redirectUrl = window.location.href;
									const loginUrl = `${env.NEXT_PUBLIC_AUTH_URL}/sign-in?redirect_url=${encodeURIComponent(
										redirectUrl,
									)}`;
									window.location.href = loginUrl;
									return;
								}
								setIsGenerateOpen(true);
							}}
							className="shadow-lg hover:shadow-xl transition-all"
						>
							<Plus className="mr-2 h-4 w-4" />
							Generate Recipe
						</Button>
					</div>
				</div>

				<div className="flex flex-col gap-4 sm:flex-row sm:items-center justify-between bg-muted/30 p-4 rounded-xl border">
					<div className="flex flex-1 items-center gap-4">
						<RecipeSearch
							value={query}
							onChange={handleSearch}
							onClear={handleClearSearch}
						/>
						<RecipeFilters
							foodTypes={foodTypes}
							setFoodTypes={setFoodTypes}
							sortBy={sortBy}
							setSortBy={setSortBy}
							sortOrder={sortOrder}
							setSortOrder={setSortOrder}
							onlyMine={onlyMine}
							setOnlyMine={setOnlyMine}
							onlyFavorites={onlyFavorites}
							setOnlyFavorites={setOnlyFavorites}
							isLoggedIn={!!user}
						/>
					</div>
					{isSearching && (
						<Button
							variant="ghost"
							onClick={handleClearSearch}
							size="sm"
							className="text-muted-foreground hover:text-foreground"
						>
							<X className="mr-2 h-4 w-4" />
							Clear Filters
						</Button>
					)}
				</div>

				{isLoading ? (
					<div className="flex h-[50vh] w-full items-center justify-center">
						<Loader2 className="h-10 w-10 animate-spin text-primary" />
					</div>
				) : (
					<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
						{recipes?.map((recipe) => (
							<RecipeCard key={recipe.id} recipe={recipe} />
						))}
						{recipes?.length === 0 && (
							<div className="col-span-full flex h-60 flex-col items-center justify-center rounded-xl border border-dashed bg-muted/10 text-muted-foreground gap-4">
								<p className="text-lg font-medium">No recipes found</p>
								{isSearching && (
									<Button variant="outline" onClick={handleClearSearch}>
										Clear Search
									</Button>
								)}
							</div>
						)}
					</div>
				)}
			</div>

			<GenerateRecipeDialog
				open={isGenerateOpen}
				onOpenChange={setIsGenerateOpen}
			/>
		</div>
	);
}
