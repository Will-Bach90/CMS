# content/management/commands/setup_groups.py
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'content/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'content/post_detail.html'

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'is_published']
    template_name = 'content/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Command(BaseCommand):
    help = 'Sets up initial user groups and permissions'

    def handle(self, *args, **kwargs):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        editor_group, _ = Group.objects.get_or_create(name='Editor')
        reader_group, _ = Group.objects.get_or_create(name='Reader')

        # Add permissions to groups
        admin_permissions = Permission.objects.all()
        editor_permissions = Permission.objects.filter(codename__in=[
            'add_post', 'change_post', 'delete_post', 'add_category', 'change_category'
        ])

        admin_group.permissions.set(admin_permissions)
        editor_group.permissions.set(editor_permissions)

        self.stdout.write(self.style.SUCCESS('User groups and permissions created!'))
