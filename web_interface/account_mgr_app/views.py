from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.


def signup(request):
    return HttpResponse("<p>This is a raw response page</p>"+
                        '<a href="/acct/">Return home</a>'+
                        "<p>end</p>")