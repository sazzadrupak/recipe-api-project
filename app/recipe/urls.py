"""
URL mappings for the recipe app
"""
from django.urls import ( # type: ignore # noqa
  path,
  include
)
from rest_framework.routers import DefaultRouter # type: ignore # noqa
from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'
urlpatterns = [
    path('', include(router.urls)),
]
