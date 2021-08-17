from django.http import HttpResponse
import datetime
from django.http import JsonResponse
import random

def index(request):
    if (random.randrange(0,2) > 0):
        return JsonResponse({'leftHand': 'Rock', 
            'rightHand': 'Paper',
            'win': 'Right',
            'time': 'BLANK'})
    else:
        return JsonResponse({'leftHand': 'Scissors', 
            'rightHand': 'Scissors',
            'win': 'Tie',
            'time': 'BLANK'})
         # return HttpResponse(datetime.today().strftime())
