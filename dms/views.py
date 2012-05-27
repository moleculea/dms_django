# HTTP
from django.http import HttpResponse, HttpResponseRedirect

# login_required decorator
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return HttpResponseRedirect('/user/')