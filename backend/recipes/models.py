from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=200
        )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, измеряем в {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField('Название', unique=True, max_length=200)
    color = models.CharField(
        'Цветовой код (HEX)',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не в формате HEX!'
            )
        ]
    )
    slug = models.SlugField('Уникальный слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        blank=False,
        null=False
    )
    name = models.CharField('Название', max_length=200)

    text = models.TextField('Описание')
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=False,
        null=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[MinValueValidator(
            1,
            message='Нельзя готовить меньше минуты!'
            )]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты',
        blank=False,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        blank=False,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(
            1,
            message='Нельзя добавить меньше единицы!'
            )]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return (
            f'''
{self.ingredient.name} {self.ingredient.measurement_unit}: {self.amount}
'''
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
                )
        ]

    def __str__(self):
        return f'Пользователь {self.user} добавил {self.recipe} в избранные.'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
                )
        ]

    def __str__(self):
        return f'Пользователь {self.user} добавил {self.recipe} в покупки.'
