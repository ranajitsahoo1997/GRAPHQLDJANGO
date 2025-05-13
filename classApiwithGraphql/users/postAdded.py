# yourapp/mutations.py

import graphene
from .models import Post,ExtendUser

from graphene_django.types import DjangoObjectType



class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "user")

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        user_id = graphene.ID(required=True)  # allow specifying a user

    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, title, content, user_id):
        try:
            user = ExtendUser.objects.get(pk=user_id)
        except ExtendUser.DoesNotExist:
            return CreatePost(success=False, message="User not found")

        post = Post.objects.create(user=user, title=title, content=content)
        return CreatePost(success=True, post=post, message="Post created23")
