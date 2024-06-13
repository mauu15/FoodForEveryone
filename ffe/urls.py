from django.urls import path

from . import views
from .views import add_recipe, recipe_detail, add_comment, toggle_favorite, user_detail

urlpatterns = [

    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="my-login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path('explore/', views.explore, name='explore'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/add_comment/', add_comment, name='add_comment'),
    path('toggle_favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<int:recipe_id>/remove/', views.remove_favorite, name='remove_favorite'),
    path('search/', views.search, name='search'),
    path('category/<str:category>/', views.category_recipes, name='category_recipes'),
    path('follow_user/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow_user/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('user/<str:username>/', user_detail, name='user_detail'),
    path('profile/', views.profile, name='profile'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),

]








