from http import HTTPStatus
from django.contrib.auth import get_user_model, authenticate
from ninja import Router
from django.shortcuts import get_object_or_404
from Handmade.utils.permissions import *
from Handmade.utils.utils import response
from account.schemas import *
from account.models import EmailAccount

User = get_user_model()

account_controller = Router()


@account_controller.post('/signup',
                         response={200: AccountCreate, 403: MessageOut, 500: MessageOut, 201: AccountSignupOut})
def signup(request, account_in: AccountSignupIn):
    if account_in.password1 != account_in.password2:
        return MessageOut(message='Passwords do not match')
    try:
        EmailAccount.objects.get(email=account_in.email)
        return response(403,
                        {'message': 'Forbidden, email is already registered'})
    except EmailAccount.DoesNotExist:
        user = EmailAccount.objects.create_user(email=account_in.email, password=account_in.password1,
                                                first_name=account_in.first_name, last_name=account_in.last_name,
                                                phone_number=account_in.phone_number)

        if user:
            token = create_token(user.id)
            return response(HTTPStatus.OK, {
                'profile': user,
                'token': token
            })
        else:
            return response(HTTPStatus.INTERNAL_SERVER_ERROR, {'message': 'An error occurred, please try again.'})


@account_controller.post('signin', response={
    200: AccountSignupOut,
    404: MessageOut,
})
def signin(request, signin_in: AccountLoginData):
    user = authenticate(email=signin_in.email, password=signin_in.password)
    if user is not None:
        return response(HTTPStatus.OK, {
            'profile': user,
            'token': create_token(user)
        })

    return 404, MessageOut(message='User not found')

# @account_controller.post('/change-password',
#                          auth=AuthBearer(),
#                          response={200: MessageOut, 400: MessageOut})
# def change_password(request, change_password_in: ChangePassword):
#     if change_password_in.new_password != change_password_in.confirm_password:
#         return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords do not match'})
#     try:
#         user = get_object_or_404(EmailAccount, id=request.auth.user_id)
#     except:
#         return response(HTTPStatus.BAD_REQUEST, {'message': 'User not found'})
#
#     user_updated = user.update_password(change_password_in.old_password, change_password_in.new_password)
#
#     if user_updated:
#         return response(HTTPStatus.OK, {'message': 'Password changed successfully'})
#     else:
#         return response(HTTPStatus.BAD_REQUEST, {'message': 'Password change failed'})
