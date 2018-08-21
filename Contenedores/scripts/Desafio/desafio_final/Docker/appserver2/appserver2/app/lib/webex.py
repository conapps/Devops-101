import requests
import json

api_url = 'https://api.ciscospark.com/v1/'

def get_room_id_by_name(name, api_key):
    endpoint = 'rooms'
    url = api_url + endpoint

    headers = {
        'Authorization': "Bearer " + api_key,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
    }

    response = requests.get(url, headers=headers).json()

    for room in response['items']:
        if room['title'] == name:
            return room['id']

    return None

def post_message(message, room_id, api_key):
    endpoint = 'messages'
    url = api_url + endpoint

    headers = {
        'Authorization': "Bearer " + api_key,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
    }

    payload = {
        "roomId": room_id,
        "text": message
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        return False


if __name__ == "__main__":
    response = post_message('probando', get_room_id_by_name('prueba123'))
    print(response)
