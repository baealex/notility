import requests
import settings

def verify(token):
    data = {
        'response': token,
        'secret': settings.HCAPTCHA_SECRET_KEY
    }
    response = requests.post('https://hcaptcha.com/siteverify', data=data)
    if response.json().get('success'):
        return True
    return False