import profile

from django.contrib.auth import get_user_model, authenticate
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q
from account.schemas import *

from account.models import EmailAccount
from account.authorization import GlobalAuth, get_tokens_for_user

User = get_user_model()

account_controller = Router()


@account_controller.post('/signup',
                         response={200: AccountCreate, 403: MessageOut, 500: MessageOut, 201: AccountSignupOut})
def signup(request, account_in: AccountSignupIn):
    if account_in.password1 != account_in.password2:
        return MessageOut(message='Passwords do not match')
    try:
        EmailAccount.objects.get(email=account_in.email)
    except EmailAccount.DoesNotExist:
        user = EmailAccount.objects.create_user(email=account_in.email, password=account_in.password1,
                                                first_name=account_in.first_name, last_name=account_in.last_name,
                                                )

        token = get_tokens_for_user(user)

        return 201, {
            'token': token,
            'account': user
        }
    return 403, MessageOut(message='User already exists')

# @account_controller.post('signin', response={
#     200: AccountSignupOut,
#     404: MessageOut,
# })
# def signin(request, signin_in: AccountLoginData):
#     user = authenticate(email=signin_in.email, password=signin_in.password)
#     if user:
#         token = get_tokens_for_user(user)
#         return 200, {
#             'token': token,
#             'account': user
#         }
#     return 404, MessageOut(message='User not found')
