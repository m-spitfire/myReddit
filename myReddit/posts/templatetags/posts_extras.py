from django import template

register = template.Library()


@register.filter(name="get_comment_set", is_safe=True)
def get_comment_set(post):
    return post.comment_set.order_by('-upvotes')


@register.filter(name='has_upvoted_post', is_safe=True)
def has_upvoted_post(user, post):
    return user in post.upvoters_total.all()


@register.filter(name='has_downvoted_post', is_safe=True)
def has_downvoted_post(user, post):
    return user in post.downvoters_total.all()


@register.filter(name='has_upvoted_comment', is_safe=True)
def has_upvoted_comment(user, comment):
    return user in comment.upvoters.all()


@register.filter(name='has_downvoted_comment', is_safe=True)
def has_downvoted_comment(user, comment):
    return user in comment.downvoters.all()


@register.filter(name='net_upvotes', is_safe=True)
def net_upvotes(post):
    return len(post.upvoters_total.all())-len(post.downvoters_total.all())
