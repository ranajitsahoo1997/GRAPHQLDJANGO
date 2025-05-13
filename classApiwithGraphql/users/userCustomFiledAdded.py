# myapp/graphql/mutations.py

import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from .models import ExtendUser


class UserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        fields = ("id", "username", "email", "link", "posts")
        
User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "username", "link")

class CustomUpdateAccount(graphene.Mutation):
    class Arguments:
        link = graphene.String(required=True)

    success = graphene.Boolean()
    user = graphene.Field(UserType)
    message = graphene.String()
    errors = graphene.List(graphene.String)  # 👈 add this line

    def mutate(self, info, link):
        user = info.context.user

        if not user.is_authenticated:
            return CustomUpdateAccount(
                success=False,
                message="Authentication required.",
                errors=["User is not logged in."]
            )

        user.link = link
        user.save()

        return CustomUpdateAccount(
            success=True,
            message="Link updated successfully.",
            user=user,
            errors=[]
        )

