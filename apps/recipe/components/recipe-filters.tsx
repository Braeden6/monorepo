"use client";

import { Button } from "@workspace/ui/components/shadcn/button";
import { Checkbox } from "@workspace/ui/components/shadcn/checkbox";
import { Label } from "@workspace/ui/components/shadcn/label";
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from "@workspace/ui/components/shadcn/popover";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@workspace/ui/components/shadcn/select";
import { Separator } from "@workspace/ui/components/shadcn/separator";
import { Switch } from "@workspace/ui/components/shadcn/switch";
import { Filter, SortAsc, SortDesc } from "lucide-react";
import type {
	FoodType,
	SortField,
	SortOrder,
} from "@/lib/api/generated/recipeAPI";

interface RecipeFiltersProps {
	foodTypes: FoodType[];
	setFoodTypes: (types: FoodType[]) => void;
	sortBy: SortField;
	setSortBy: (field: SortField) => void;
	sortOrder: SortOrder;
	setSortOrder: (order: SortOrder) => void;
	onlyMine: boolean;
	setOnlyMine: (val: boolean) => void;
	onlyFavorites: boolean;
	setOnlyFavorites: (val: boolean) => void;
	isLoggedIn: boolean;
}

const FOOD_TYPE_OPTIONS: FoodType[] = [
	"BREAKFAST",
	"LUNCH",
	"DINNER",
	"DESSERT",
	"SNACK",
	"DRINK",
];

const SORT_FIELD_OPTIONS: { value: SortField; label: string }[] = [
	{ value: "created_at", label: "Date Created" },
	{ value: "updated_at", label: "Date Updated" },
	{ value: "like_count", label: "Most Liked" },
	{ value: "favorite_count", label: "Most Favorited" },
	{ value: "relevance", label: "Relevance" },
];

export function RecipeFilters({
	foodTypes,
	setFoodTypes,
	sortBy,
	setSortBy,
	sortOrder,
	setSortOrder,
	onlyMine,
	setOnlyMine,
	onlyFavorites,
	setOnlyFavorites,
	isLoggedIn,
}: RecipeFiltersProps) {
	const activeFilterCount =
		foodTypes.length + (onlyMine ? 1 : 0) + (onlyFavorites ? 1 : 0);

	return (
		<Popover>
			<PopoverTrigger asChild>
				<Button variant="outline" className="relative">
					<Filter className="mr-2 h-4 w-4" />
					Filters
					{activeFilterCount > 0 && (
						<span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[10px] text-primary-foreground">
							{activeFilterCount}
						</span>
					)}
				</Button>
			</PopoverTrigger>
			<PopoverContent className="w-80 p-4" align="end">
				<div className="space-y-4">
					<div className="space-y-2">
						<h4 className="font-medium leading-none text-sm">Sorting</h4>
						<div className="flex gap-2">
							<div className="flex-1">
								<Select
									value={sortBy}
									onValueChange={(val) => setSortBy(val as SortField)}
								>
									<SelectTrigger>
										<SelectValue placeholder="Sort by" />
									</SelectTrigger>
									<SelectContent>
										{SORT_FIELD_OPTIONS.map((opt) => (
											<SelectItem key={opt.value} value={opt.value}>
												{opt.label}
											</SelectItem>
										))}
									</SelectContent>
								</Select>
							</div>
							<Button
								variant="outline"
								size="icon"
								onClick={() =>
									setSortOrder(sortOrder === "asc" ? "desc" : "asc")
								}
								title={`Sort ${sortOrder === "asc" ? "Ascending" : "Descending"}`}
							>
								{sortOrder === "asc" ? (
									<SortAsc className="h-4 w-4" />
								) : (
									<SortDesc className="h-4 w-4" />
								)}
							</Button>
						</div>
					</div>

					<Separator />

					<div className="space-y-2">
						<h4 className="font-medium leading-none text-sm">Food Types</h4>
						<div className="grid grid-cols-2 gap-2">
							{FOOD_TYPE_OPTIONS.map((type) => (
								<div key={type} className="flex items-center space-x-2">
									<Checkbox
										id={`type-${type}`}
										checked={foodTypes.includes(type)}
										onCheckedChange={(checked) => {
											if (checked) {
												setFoodTypes([...foodTypes, type]);
											} else {
												setFoodTypes(foodTypes.filter((t) => t !== type));
											}
										}}
									/>
									<Label
										htmlFor={`type-${type}`}
										className="text-xs font-normal capitalize cursor-pointer"
									>
										{type.toLowerCase()}
									</Label>
								</div>
							))}
						</div>
					</div>

					<Separator />

					<div className="space-y-3">
						<div className="flex items-center justify-between">
							<Label
								htmlFor="only-mine"
								className="text-sm font-normal flex flex-col gap-1"
							>
								<span>My Recipes</span>
								<span className="text-[10px] text-muted-foreground">
									Only recipes created by you
								</span>
							</Label>
							<Switch
								id="only-mine"
								disabled={!isLoggedIn}
								checked={onlyMine}
								onCheckedChange={setOnlyMine}
							/>
						</div>

						<div className="flex items-center justify-between">
							<Label
								htmlFor="only-favorites"
								className="text-sm font-normal flex flex-col gap-1"
							>
								<span>Favorites</span>
								<span className="text-[10px] text-muted-foreground">
									Only recipes you favorited
								</span>
							</Label>
							<Switch
								id="only-favorites"
								disabled={!isLoggedIn}
								checked={onlyFavorites}
								onCheckedChange={setOnlyFavorites}
							/>
						</div>
					</div>

					{!isLoggedIn && (
						<p className="text-[10px] text-muted-foreground italic">
							Log in to filter by your recipes and favorites.
						</p>
					)}
				</div>
			</PopoverContent>
		</Popover>
	);
}
