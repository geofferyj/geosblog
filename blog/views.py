from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Post, Comment
from .forms import  CommentForm


class PostList(ListView):
    queryset = Post.objects.filter(status='published').order_by('-updated_on')
    template_name = 'blog/index.html'
    paginate_by = 1


def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            com_id = request.POST.get('comment_id')
            if com_id:
                new_comment.tn_parent = Comment.objects.get(id=com_id)
            # Save the comment to the database 
            new_comment.save()
    #         comment_form = CommentForm()
            return redirect(request.path_info)
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'comment_form': comment_form})

class TagIndexView(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'post_list'
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug')).order_by('-updated_on')

