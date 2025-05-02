from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'User registration successful'})


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else: return JsonResponse({'error': 'Invalid username or password'}, status=401)


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    data = [{'username': u.username} for u in users]
    return JsonResponse(data, safe=False)


from .models import Message
@login_required
def get_messages(request, username):
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    data = [{
        'sender': msg.sender.username,
        'receiver': msg.receiver.username,
        'message': msg.message,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages]

    return JsonResponse(data, safe=False)
