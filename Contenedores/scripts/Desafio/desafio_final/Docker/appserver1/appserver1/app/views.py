from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import requests
import json

# Create your views here.


def home(request, template_name):
    context = {}
    return render(request, template_name, context)

@csrf_exempt
def data(request, template_name, fail_template_name):
    context = {}
    token = request.POST.get('token')
    sala = request.POST.get('sala')
    mensaje = request.POST.get('mensaje')
    url = 'http://172.18.1.5:8080/message'
    payload = {
        'name': sala,
        'message': mensaje,
        'api_key': token
    }

    result = requests.post(url, data=json.dumps(payload))

    if result.status_code == 200:
        return render(request, template_name, context)
    else:
        return render(request, fail_template_name, context)