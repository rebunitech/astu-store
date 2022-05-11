from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponse



def items(requests):
    return HttpResponse("hello")
