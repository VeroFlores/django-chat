# chat/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django. views. decorators. csrf import csrf_exempt

def index(request):
    return render(request, 'chat/index.html',{})

def room(request, room_name):

    # return JsonResponse(room_name)
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

@csrf_exempt
def veroJSON(request):
    
    if request.method == "POST":
        data = {
            "Nombre": "Javier",
            "Apellido": "Arias",
        }
        return JsonResponse(data)
    
    data = {
        "Nombre": "Vero",
        "Apellido": "Flores",
    }
    return JsonResponse(data)