import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from users.postAdded import PostType



from .models import ExtendUser,Post

from users.userCustomFiledAdded import UserType,CustomUpdateAccount
from users.postAdded import CreatePost



class CustomObtainJSONWebToken(mutations.ObtainJSONWebToken):
    @classmethod
    def mutate(cls, root, info, **kwargs):
        # call the default mutation
        result = super().mutate(root, info, **kwargs)

        # decode token if it's returned as bytes
        if hasattr(result, 'token') and isinstance(result.token, bytes):
            result.token = result.token.decode('utf-8')

        if hasattr(result, 'refresh_token') and isinstance(result.refresh_token, bytes):
            result.refresh_token = result.refresh_token.decode('utf-8')

        return result
    
    


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    # token_auth = CustomObtainJSONWebToken.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_account = mutations.VerifyAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_paasword_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    update_account = CustomUpdateAccount.Field()
   
    
    
    
    # refresh_token = CustomObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    
class PostMutation(graphene.ObjectType):
    create_post = CreatePost.Field()    



class Query(UserQuery, MeQuery, graphene.ObjectType):
    all_posts = graphene.List(PostType)
    user_posts = graphene.List(PostType, user_id=graphene.Int())
    all_users = graphene.List(UserType)
    
    def resolve_all_users(root,info):
        return ExtendUser.objects.all()

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_user_posts(root, info, user_id):
        return Post.objects.filter(user_id=user_id)
    


class Mutation(PostMutation,AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
