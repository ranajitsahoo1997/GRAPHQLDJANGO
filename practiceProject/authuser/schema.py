import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import posts.schema

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
    verify_account = mutations.VerifyAccount.Field()
    password_reset = mutations.PasswordReset.Field()
    update_account = mutations.UpdateAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    password_change = mutations.PasswordChange.Field()
    password_set = mutations.PasswordSet.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
  

class Query(posts.schema.Query,UserQuery, MeQuery, graphene.ObjectType):
    # Add any custom queries here
    pass
class Mutation(posts.schema.Mutation,AuthMutation, graphene.ObjectType):
    # Add any custom mutations here
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)