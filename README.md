# Whatsapp_clone

A basic clone of chat engine like whatsapp. You can register, login, see your chat messages and get userlist via http apis.
There's real-time communication between 2 users using websockets. Messages are saved in sqlite db.

Backend used is Django and Django channels. Start the server using the command : uvicorn watsapp.asgi:application --reload
