from ninja import Router, File
from http import HTTPStatus
from django.contrib.auth import authenticate
from Handmade.utils.permissions import create_token, AuthBearer
from Handmade.utils.schemas import MessageOut
from Handmade.utils.utils import response
from ninja.files import UploadedFile
from .models import EmailAccount
from .schemas import AccountSignupOut, AccountSignupIn, AccountSigninOut, \
    AccountSigninIn, AccountOut, AccountUpdateIn, PasswordChangeIn, Profile
from django.shortcuts import get_object_or_404

auth_controller = Router(tags=['Auth'])


@auth_controller.post('/signup', response={200: AccountSignupOut, 403: MessageOut, 500: MessageOut})
def register(request, payload: AccountSignupIn):
    if payload.password1 != payload.password2:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords does not match!'})

    try:
        EmailAccount.objects.get(email=payload.email)
        return response(403,
                        {'message': 'Forbidden, email is already registered'})
    except EmailAccount.DoesNotExist:
        user = EmailAccount.objects.create_user(first_name=payload.first_name, last_name=payload.last_name,
                                                email=payload.email, password=payload.password1,

                                                )
        if user:
            user.phone_number = payload.phone_number
            user.address = payload.address
            user.save()
            token = create_token(user.id)
            return response(HTTPStatus.OK, {
                'profile': user,
                'token': token
            })
        else:
            return response(HTTPStatus.INTERNAL_SERVER_ERROR, {'message': 'An error occurred, please try again.'})


@auth_controller.post('/signin', response={200: AccountSigninOut, 404: MessageOut})
def login(request, payload: AccountSigninIn):
    user = authenticate(email=payload.email, password=payload.password)
    if user is not None:
        return response(HTTPStatus.OK, {
            'profile': user,
            'token': create_token(user.id)
        })
    return response(HTTPStatus.NOT_FOUND, {'message': 'User not found'})


@auth_controller.post('/change-password',
                      auth=AuthBearer(),
                      response={200: MessageOut, 400: MessageOut})
def change_password(request, payload: PasswordChangeIn):
    if payload.new_password1 != payload.new_password2:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords do not match!'})

    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})

    user_update = authenticate(email=user.email, password=payload.old_password)

    if user_update is not None:
        user_update.set_password(payload.new_password1)
        user_update.save()
        return response(HTTPStatus.OK, {'message': 'password updated'})

    return response(HTTPStatus.BAD_REQUEST, {'message': 'something went wrong, please try again later'})


@auth_controller.get('/profile',
                     auth=AuthBearer(),
                     response={200: AccountOut, 400: MessageOut})
def profile(request):
    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})
    return response(HTTPStatus.OK, user)


@auth_controller.put('/profile',
                     auth=AuthBearer(),
                     response={200: AccountOut, 400: MessageOut})
def update_profile(request, user_in: AccountUpdateIn):
    try:
        user = EmailAccount.objects.filter(id=request.auth.id)

    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})

    if user_in.first_name:
        user.first_name = user_in.first_name
    if user_in.last_name:
        user.last_name = user_in.last_name
    if user_in.email:
        user.email = user_in.email
    if user_in.phone_number:
        user.phone_number = user_in.phone_number
    if user_in.address:
        user.address = user_in.address

    user.save()
    return response(HTTPStatus.OK, user)



