# content/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import viewsets
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def is_editor(user):
    return user.groups.filter(name="Editor").exists() or user.is_superuser

@login_required
@user_passes_test(is_editor)
def create_post(request):
    # Only editors and admins can access this view
    pass

