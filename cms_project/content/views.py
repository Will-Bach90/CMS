# content/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostListView(ListView):
    model = Post
    template_name = 'content/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True) 

class PostDetailView(DetailView):
    model = Post
    template_name = 'content/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'is_published']
    template_name = 'content/post_form.html'
    success_url = reverse_lazy('post_list')

    # Automatically set the post author to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Limit access to users in the 'Editor' group or admins
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Editor").exists()

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('login'))  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def is_editor(user):
    return user.groups.filter(name="Editor").exists() or user.is_superuser

@login_required
@user_passes_test(is_editor)
def create_post(request):
    # Only editors and admins can access this view
    pass

