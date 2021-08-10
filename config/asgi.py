# import os

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter

# from django.core.asgi import get_asgi_application

# import myapp.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'verifynews.config.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             myapp.routing.websocket_urlpatterns
#         )
#     )
# })






"""
ASGI config for test project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application
# import chat.routing


# This allows easy placement of apps within the interior
# test directory.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "verifynews"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
os.environ.setdefault('SERVER_GATEWAY_INTERFACE', 'Asynchronous') # use this variable in other parts of the code to verify that the app is using ASGI 


# This application object is used by any ASGI server configured to use this file.
# django_application = get_asgi_application()
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# # Import websocket application here, so apps from django_application are loaded first
# from config.websocket import websocket_application  # noqa isort:skip


# async def application(scope, receive, send):
#     if scope["type"] == "http":
#         await django_application(scope, receive, send)
#     elif scope["type"] == "websocket":
#         await websocket_application(scope, receive, send)
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    
    "websocket": AuthMiddlewareStack(
        URLRouter(
            verifynews.myapp.routing.websocket_urlpatterns
        )
    )
})






