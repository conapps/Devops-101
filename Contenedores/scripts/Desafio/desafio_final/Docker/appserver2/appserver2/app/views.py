import os
from django.shortcuts import render
from app.lib.webex import get_room_id_by_name, post_message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.


def home(request, template_name):
    context = {}
    room_id = get_room_id_by_name('prueba123')
    post_message('prueba desde view', room_id)
    return render(request, template_name, context)


@csrf_exempt
def send_message(request):
    teams_key = os.environ.get('TEAMS_KEY', None)
    group = os.environ['GRUPO']
    room_name = 'Docker-101'
    message = '## Mensaje de ' + group + '\n'
    if request.method == 'POST':
        received_data = json.loads(request.body.decode('utf-8'))
        message += received_data['message']
        room_id = get_room_id_by_name(room_name, teams_key)
        result = post_message(message, room_id, teams_key)
        return JsonResponse(result, status=200)
    else:
        return JsonResponse({'error': 'invalid method'}, status=400)
