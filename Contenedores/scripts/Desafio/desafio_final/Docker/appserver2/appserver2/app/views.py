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

    if request.method == 'POST':
        received_data = json.loads(request.body.decode('utf-8'))
        room_id = get_room_id_by_name(received_data['name'], received_data['api_key'])
        result = post_message(received_data['message'], room_id, received_data['api_key'])
        return JsonResponse(result, status=200)
    else:
        return JsonResponse({'error': 'invalid method'}, status=400)