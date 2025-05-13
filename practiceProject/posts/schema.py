import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from .models import Post
from authuser.models import AuthUser

# User type
class AuthUserType(DjangoObjectType):
    class Meta:
        model = AuthUser
        fields = ("id", "username", "email")

# Post type
class PostType(DjangoObjectType):
    author = graphene.Field(AuthUserType)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "author", "created_at")


# Queries
class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.Int())

    def resolve_all_posts(self, info):
        user = info.context.user
        print(user.username)
        if user.is_anonymous:
            raise GraphQLError("Authentication required")
        return Post.objects.filter(author=user)
    def resolve_post_by_id(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")
        try:
            return Post.objects.get(id=id, author=user)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
    
        

# Mutations
class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, title, content):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")
        post = Post(title=title, content=content, author=user)
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, id, title=None, content=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")

        if post.author != user:
            raise GraphQLError("You do not have permission to edit this post")

        if title:
            post.title = title
        if content:
            post.content = content
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
        if post.author != user:
            raise GraphQLError("You do not have permission to delete this post")

        post.delete()
        return DeletePost(success=True)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
