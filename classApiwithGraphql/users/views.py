from django.shortcuts import render

# Create your views here.
# from django.http import JsonResponse
# from graphql_jwt.utils import jwt_decode
# from graphql_auth.models import UserStatus

# def activate_account(request, token):
#     try:
#         # Decode the token to get the payload
#         payload = jwt_decode(token)
#         username = payload.get("username")

#         # Activate the user
#         user_status = UserStatus.objects.get(user__username=username)
#         user_status.activate()
#         return JsonResponse({'success': True, 'message': 'Account activated!'})
    
#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)}, status=400)