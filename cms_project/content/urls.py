# content/urls.py
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CategoryViewSet, signup

router = DefaultRouter()
router.register(r'posts', PostViewSet)       # API endpoint for posts
router.register(r'categories', CategoryViewSet)  # API endpoint for categories

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),       # List all posts
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Detail view of a single post
    path('post/new/', PostCreateView.as_view(), name='post_create'),       # Create a new post
    path('signup/', signup, name='signup'),
] + router.urls  # Add API routes from the router
