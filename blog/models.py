from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Model, CharField, EmailField, IntegerField, ForeignKey, TextField, DateTimeField, CASCADE, SlugField
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from treenode.models import TreeNodeModel

STATUS = (
    ('draft',"Draft"),
    ('published',"Publish")
)


class Post(Model):
    title = CharField(max_length=100)
    slug = SlugField(max_length=200, unique=True)
    author = ForeignKey(User, on_delete=CASCADE, related_name='blog_posts')
    created_on = DateTimeField(default=timezone.now)
    updated_on = DateTimeField(auto_now_add=True)
    description = TextField()
    content = MarkdownxField()
    status = CharField(max_length=100, choices=STATUS, default='draft')
    tags = TaggableManager(blank=True)


    def __str__(self):
        return self.title

class Comment(TreeNodeModel):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    name = CharField(max_length=100)
    email = EmailField()
    body = TextField()
    created_on = DateTimeField(auto_now_add=True)
    treenode_display_field = 'name'


    class Meta(TreeNodeModel.Meta):
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_on']
    
    def __str__(self):
        return f'comment {self.body} by {self.name}'