from django.http import HttpResponse
from django.shortcuts import render
from eq_web.model.eq_info import EqInfo

test_list = [{"name": 'good', 'password': 'python'}, {'name': 'learning', 'password': 'django'}]


def hello(request):
    return HttpResponse("Hello world ! ")


# 跳转入index页面
def index(request):
    is_had_eq = EqInfo.objects.order_by('-O_time')[0:100].filter()
    return render(request, "index.html", {'eqInfo': is_had_eq})

