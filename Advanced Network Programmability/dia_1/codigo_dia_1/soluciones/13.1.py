import requests

def get_motd():
    URL = 'https://talaikis.com/api/quotes/random/'
    response = requests.get(URL, timeout=2).json()
    return response['quote']


if __name__ == '__main__':
    print(get_motd())