from django.views import View
from django.shortcuts import render, redirect

from .models import Products, Category


class CategorysView(View):
    def get(self, request):
        pass


class CategoryDetails(View):
    def get(self, request):
        pass
