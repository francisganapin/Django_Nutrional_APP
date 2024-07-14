from django.urls import path
from  . import views


urlpatterns = [
    path('food/',views.food_view,name='food_view'),
    path('success/', views.success_page, name='success_page'),
    path('food/add/',views.food_add_view,name='food_add_view'),
    path('food/remove/', views.food_remove_view, name='food_remove'),
    path('',views.food_view,name='food_view')
]