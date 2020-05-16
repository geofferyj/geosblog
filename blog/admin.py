from django.contrib import admin
from .models import  Post, Comment
from markdownx.admin import MarkdownxModelAdmin
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm

@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'tag_list')
    list_filter = ("status",)
    list_editable = ["status"]
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(Comment)
class CommentAdmin(TreeNodeModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on')
    list_filter = ('post', 'created_on')
    search_fields = ('name', 'email', 'body')
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    form = TreeNodeForm
    