import requests

def get_motd():
    URL = 'https://talaikis.com/api/quotes/random/'
    response = # Hacer el llamado a la API
    return response['quote']

if __name__ == '__main__':
    print(get_motd())