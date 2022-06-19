from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *
from . import views


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('filter/', AdsAction.as_view(), name='filter'),
    path('ads/<slug:ads_slug>', ShowAds.as_view(), name='ads'),
    path('category/<slug:cat_slug>', AdsCategory.as_view(), name='category'),
    path('addads/', views.add_ads, name='add_ads'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile_add/', ProfileAddUser.as_view(), name='profile_add'),
    path('user_profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='ads/logout.html'), name='logout'),
    path('edit-page', views.edit_page, name='edit_page'),
    path('update-page/<int:pk>', views.update_page, name='update_page'),
    path('delete-image/<int:id>', views.delete_image, name="delete_image"),
    path('delete-page/<int:pk>', ProductDeleteView.as_view(), name="delete_page"),
    path('favourite_post/<int:id>', views.favourite_post, name="favourite_post"),
    path('favourites', views.favourite_post_list, name="favourite_post_list"),
    path('search/', SearchResultsView.as_view(), name='search_results'),

    #ajax
    path('update_comment_status/<int:pk>/<slug:type>', views.update_comment_status, name='update_comment_status')
]
