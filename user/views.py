from django.http import HttpResponseBadRequest, HttpResponse, HttpRequest, JsonResponse
from .models import User
import jwt, simplejson, bcrypt, datetime
from django.conf import settings
AUTH_EXPIRE = 60*60*8


def authenticate(view):
    def wrapper(request: HttpRequest):
        token = request.META.get('HTTP_JWT')
        if not token:
            return HttpResponse(status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            return HttpResponse(status=401)
        try:
            user_id = payload.get('uid', -1)
            user = User.objects.get(pk=user_id)
            request.user = user
        except Exception as e:
            print(e)
            return HttpResponse(status=401)
        return view(request)
    return wrapper


def get_token(user_id):
    ret = jwt.encode({
        "uid": user_id,
        "exp": int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE
    }, settings.SECRET_KEY, "HS256")
    return ret.decode()


def check_email(email):

    qs = User.objects.filter(email=email).first()
    if qs:
        return qs
    else:

        return False


def reg(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        name = payload["name"]
        email = payload["email"]
        password = payload["password"]

        if not check_email(email):
            user = User()
            user.name = name
            user.email = email
            user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user.save()
            return JsonResponse({"token": get_token(user.id).decode()})
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def login(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password']
        user = check_email(email)
        if not user:
            return HttpResponseBadRequest()
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return HttpResponseBadRequest()
        return JsonResponse({
            "user": {
                "user_id": user.id,
                "user_name": user.name,
                "user_email": user.email,
                },
            "token": get_token(user.id)
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


@authenticate
def test(request):
    return HttpResponse('1111')