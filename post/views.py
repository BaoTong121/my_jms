from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest, JsonResponse, HttpResponseNotFound
import simplejson
import datetime
from .models import Post, Content
from user.models import User
from user.views import authenticate
import math

@authenticate
def put(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        post = Post()
        post.title = payload['title']
        post.author = User(request.user.id)
        post.putdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        content = Content()
        content.post = post
        content.content = payload['content']
        post.save()
        content.save()
        return HttpResponse('aaa')
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def get(request: HttpRequest, id):
    try:
        post = Post.objects.get(pk=int(id))
        return JsonResponse({
            "post": {
                "post_title": post.title,
                "post_putdate": post.putdate.timestamp(),
                "post_author": post.author.name,
                "post_author_id": post.author_id,
                "post_content": post.content.content
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()


def validata(d:dict, name:str, con_func, default, val_func):
    try:
        ret = con_func(d[name])
        ret = val_func(ret, default)
    except:
        ret = default
    return ret



def getall(request: HttpRequest):
    page = validata(request.GET, 'page', int, 1, lambda x,y: x if x>0 else y)
    size = validata(request.GET, 'size', int, 20, lambda x,y:x if x>0 and x<101 else y)
    start = (page-1) * size
    try:
        qs = Post.objects
        posts = qs.order_by("-id")[start:start+size]
        count = qs.count()
        return JsonResponse({
            "posts": [{
                "post_id": post.id,
                "post_title": post.title
            } for post in posts],
            "pagination": {
                "page": page,
                "size": size,
                "pages": math.ceil(count/size),
                "count": count

            }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()