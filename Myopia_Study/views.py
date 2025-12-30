
from django.shortcuts import render
from django.views.generic import TemplateView
import os

# Create your views here.
class FrontendAppView(TemplateView):
    def get_template_names(self):
        return [self.kwargs["path"]]

