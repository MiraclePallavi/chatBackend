from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Message
import json


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"message": "Login successful", "username": user.username}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "POST method required"}, status=405)


@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)

    return JsonResponse({"error": "POST method required"}, status=405)


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Create the user
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({"message": "User registered successfully", "username": user.username}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    return JsonResponse({"error": "POST method required"}, status=405)


def get_users(request):
   
    if request.method == "GET":
        current_user = request.user
        users = User.objects.exclude(id=current_user.id)  # Exclude the logged-in user
        user_list = [{"username": user.username} for user in users]
        return JsonResponse({"users": user_list}, status=200)

    return JsonResponse({"error": "GET method required"}, status=405)


@login_required
def get_chat_history(request):
    """
    Fetch the chat history for group chat or personalized chat.
    """
    if request.method == "GET":
        recipient_username = request.GET.get("recipient")  # Recipient username for personal chat
        is_group = request.GET.get("is_group", "false").lower() == "true"  # Determine if it's group chat

        if is_group:
            # Fetch group chat messages
            messages = Message.objects.filter(is_group_message=True).order_by("timestamp")
        else:
            # Fetch private messages between the sender and recipient
            recipient = User.objects.filter(username=recipient_username).first()
            if not recipient:
                return JsonResponse({"error": "Recipient not found"}, status=404)

            messages = Message.objects.filter(
                sender=request.user, recipient=recipient
            ) | Message.objects.filter(
                sender=recipient, recipient=request.user
            )
            messages = messages.order_by("timestamp")

        # Format messages
        message_list = [
            {
                "sender": msg.sender.username,
                "recipient": msg.recipient.username if msg.recipient else "Group",
                "content": msg.content,
                "timestamp": msg.timestamp,
            }
            for msg in messages
        ]
        return JsonResponse({"messages": message_list}, status=200)

    return JsonResponse({"error": "GET method required"}, status=405)
