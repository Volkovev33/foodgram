from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from api.filters import RecipeFilter, IngredientFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeReadSerializer, RecipeSerializer,
                             TagSerializer, ShoppingListSerializer)

from recipes.models import (Favorite, Ingredient, Recipe, IngredientInRecipe,
                            ShoppingCart, Tag)


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    Сборная солянка для ингридиентов и тегов
    """
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Получение списка рецептов, избранного и
    списка покупок.
    """
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_action(request, pk, serializers):
        """
        Общий метод для добавления в Избранное/Корзину.
        """
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        """
        Добавление рецепта в избранное
        """
        return self.post_method_for_action(request=request, pk=pk,
                                           serializers=FavoriteSerializer)

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        """
        Добавление рецепта в список покупок
        """
        return self.post_method_for_action(request=request, pk=pk,
                                           serializers=ShoppingListSerializer)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        """
        Общий метод для удаления избранного/списка покупок.
        """
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_object = model.objects.filter(user=user, recipe=recipe)
        if model_object.exists():
            model_object.delete()
            return Response(
                f'Рецепт удалён из {model._meta.verbose_name.title()}',
                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                f'Рецепт уже удалён из {model._meta.verbose_name.title()}',
                status=status.HTTP_400_BAD_REQUEST)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """
        Удаление рецепта из избранного
        """
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """
        Удаление рецепта из списка покупок
        """
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """
        Скачивание списка покупок
        """
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        today = datetime.today()
        shopping_list = (
            f'Покупки: {user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_list += '\n\nFoodgram project'
        filename = f'{user.username}_shopping.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class IngredientViewSet(ListRetrieveViewSet):
    """
    Получение игредиентов (фильрация по полю name)
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ['^name', ]
    permission_classes = (permissions.AllowAny,)


class TagViewSet(ListRetrieveViewSet):
    """
    Получение тегов
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
