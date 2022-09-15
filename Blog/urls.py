from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('article-<str:pk>/',views.Post_view,name='view_post'),
    path('profile/<str:pk>',views.user_profile, name='profile'),
    path('category/<str:pk>',views.categories, name='category'),
    path('new-post/',views.new_post, name='new_post'),
    path('update/<str:pk>/',views.update_post,name='update_post'),
    path('delete/<str:pk>/',views.delete,name='delete_post'),
    path('post-like', views.post_like, name='post-like'),
    path('post-unlike',views.post_unlike,name='unLike-post'),
    path('serch_result/',views.search, name='search'),
    path('delete_comment/',views.delete_comment, name='delete_comment'),
    path('follow-user', views.follow_user, name='follow-user'),
    path('unfollow-user', views.unfollow_user, name='unfollow-user'),
]