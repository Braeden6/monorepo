from typing import Any

from sqlalchemy import ColumnElement, func, or_
from sqlmodel import Session, col, select

from recipe_api.features.recipes.schemas import (
    PaginationMeta,
    RecipeQueryRequest,
    RecipeQueryResponse,
    RecipeRead,
    SortField,
    SortOrder,
)
from recipe_api.shared.models.recipe import Recipe, RecipeStatus
from recipe_api.shared.models.user_interaction import UserRecipeInteraction
from recipe_api.shared.services.embeddings import EmbeddingService
from recipe_api.shared.utils.pagination import CursorData, decode_cursor, encode_cursor


class RecipeQueryHandler:
    def __init__(self, session: Session, embedding_service: EmbeddingService):
        self.session = session
        self.embedding_service = embedding_service

    def query_recipes(
        self,
        request: RecipeQueryRequest,
        user_id: str | None = None,
    ) -> RecipeQueryResponse:
        if request.sort_by == SortField.RELEVANCE and not request.query:
            request.sort_by = SortField.CREATED_AT

        cursor_data = decode_cursor(request.cursor) if request.cursor else None

        if request.query:
            results, total = self._execute_semantic_search(
                request=request,
                user_id=user_id,
                cursor_data=cursor_data,
            )
        else:
            results, total = self._execute_filtered_list(
                request=request,
                user_id=user_id,
                cursor_data=cursor_data,
            )

        pagination = self._build_pagination(
            results=results,
            limit=request.limit,
            sort_by=request.sort_by,
            total=total,
            cursor_data=cursor_data,
        )

        enriched_results = self._enrich_with_interactions(results, user_id)

        return RecipeQueryResponse(
            results=enriched_results,
            pagination=pagination,
            query=request.query,
            filters_applied=self._summarize_filters(request),
        )

    def _execute_semantic_search(
        self,
        request: RecipeQueryRequest,
        user_id: str | None,
        cursor_data: CursorData | None,
    ) -> tuple[list[RecipeRead], int]:
        query_text = request.query or ""
        query_embedding = self.embedding_service.encode(query_text)

        desc_similarity = 1 - Recipe.description_embedding.cosine_distance(query_embedding)
        ing_similarity = 1 - Recipe.ingredient_embedding.cosine_distance(query_embedding)
        max_similarity = func.greatest(desc_similarity, ing_similarity)

        base_conditions = self._build_conditions(request, user_id)
        base_conditions.append(Recipe.description_embedding.is_not(None))
        base_conditions.append(Recipe.ingredient_embedding.is_not(None))

        count_stmt = select(func.count(col(Recipe.id))).where(*base_conditions)
        total = self.session.exec(count_stmt).one()

        stmt = select(Recipe, max_similarity.label("similarity_score")).where(*base_conditions)

        if request.sort_by == SortField.RELEVANCE:
            stmt = stmt.order_by(max_similarity.desc())
        else:
            stmt = self._apply_sorting(stmt, request.sort_by, request.sort_order)

        offset = cursor_data.offset if cursor_data else 0
        stmt = stmt.offset(offset).limit(request.limit + 1)

        raw_results = self.session.exec(stmt).all()

        results = []
        for row in raw_results[: request.limit]:
            recipe = row[0]
            similarity = float(row[1]) if row[1] is not None else None

            if request.boost_popular and similarity is not None:
                popularity_score = (recipe.like_count + recipe.favorite_count * 2) / 100
                similarity = similarity * 0.7 + popularity_score * 0.3

            read = RecipeRead.model_validate(recipe)
            read.similarity_score = similarity
            results.append(read)

        if request.boost_popular and request.sort_by == SortField.RELEVANCE:
            results.sort(key=lambda x: x.similarity_score or 0, reverse=True)

        return results, total

    def _execute_filtered_list(
        self,
        request: RecipeQueryRequest,
        user_id: str | None,
        cursor_data: CursorData | None,
    ) -> tuple[list[RecipeRead], int]:
        base_conditions = self._build_conditions(request, user_id)

        count_stmt = select(func.count(col(Recipe.id))).where(*base_conditions)
        total = self.session.exec(count_stmt).one()

        stmt = select(Recipe).where(*base_conditions)
        stmt = self._apply_sorting(stmt, request.sort_by, request.sort_order)

        offset = cursor_data.offset if cursor_data else 0
        stmt = stmt.offset(offset).limit(request.limit + 1)

        raw_results = self.session.exec(stmt).all()

        results = [RecipeRead.model_validate(r) for r in raw_results[: request.limit]]
        return results, total

    def _build_conditions(
        self, request: RecipeQueryRequest, user_id: str | None
    ) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []

        if user_id and request.include_drafts:
            conditions.append(
                or_(
                    col(Recipe.status) == RecipeStatus.PUBLISHED,
                    col(Recipe.created_by) == user_id,
                )
            )
        else:
            conditions.append(col(Recipe.status) == RecipeStatus.PUBLISHED)

        if request.food_types:
            conditions.append(col(Recipe.food_type).in_(request.food_types))

        if request.only_mine and user_id:
            conditions.append(col(Recipe.created_by) == user_id)

        if request.only_favorites and user_id:
            conditions.append(
                col(Recipe.id).in_(
                    select(UserRecipeInteraction.recipe_id).where(
                        UserRecipeInteraction.user_id == user_id,
                        UserRecipeInteraction.is_favorite,
                    )
                )
            )

        return conditions

    def _apply_sorting(self, stmt: Any, sort_by: SortField, sort_order: SortOrder) -> Any:
        sort_column = {
            SortField.CREATED_AT: Recipe.created_at,
            SortField.UPDATED_AT: Recipe.updated_at,
            SortField.LIKE_COUNT: Recipe.like_count,
            SortField.FAVORITE_COUNT: Recipe.favorite_count,
        }.get(sort_by, Recipe.created_at)

        if sort_order == SortOrder.DESC:
            stmt = stmt.order_by(col(sort_column).desc())
        else:
            stmt = stmt.order_by(col(sort_column).asc())

        stmt = stmt.order_by(Recipe.id)
        return stmt

    def _build_pagination(
        self,
        results: list[RecipeRead],
        limit: int,
        sort_by: SortField,
        total: int,
        cursor_data: CursorData | None,
    ) -> PaginationMeta:
        current_offset = cursor_data.offset if cursor_data else 0
        has_next = current_offset + limit < total
        has_prev = current_offset > 0

        next_cursor = encode_cursor(
            offset=current_offset + limit,
            sort_field=sort_by.value,
            item_id=str(results[-1].id) if has_next and results else None,
        )
        prev_cursor = encode_cursor(
            offset=max(0, current_offset - limit),
            sort_field=sort_by.value,
            item_id=str(results[0].id) if has_prev and results else None,
        )

        return PaginationMeta(
            total=total,
            limit=limit,
            has_next=has_next,
            has_prev=has_prev,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
        )

    def _enrich_with_interactions(
        self, results: list[RecipeRead], user_id: str | None
    ) -> list[RecipeRead]:
        if not user_id or not results:
            return results

        recipe_ids = [r.id for r in results]
        interactions = self.session.exec(
            select(UserRecipeInteraction).where(
                UserRecipeInteraction.user_id == user_id,
                col(UserRecipeInteraction.recipe_id).in_(recipe_ids),
            )
        ).all()

        interaction_map = {i.recipe_id: i for i in interactions}
        for result in results:
            interaction = interaction_map.get(result.id)
            if interaction:
                result.is_liked = interaction.is_liked
                result.is_favorited = interaction.is_favorite

        return results

    def _summarize_filters(self, request: RecipeQueryRequest) -> dict[str, Any]:
        filters: dict[str, Any] = {}
        if request.food_types:
            filters["food_types"] = [ft.value for ft in request.food_types]
        if request.query:
            filters["text_search"] = True
        filters["sort_by"] = request.sort_by.value
        filters["only_mine"] = request.only_mine
        filters["only_favorites"] = request.only_favorites
        return filters
