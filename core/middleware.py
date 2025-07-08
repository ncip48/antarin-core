from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

@database_sync_to_async
def get_user_from_token(token):
    try:
        print("[JWT Middleware] Raw Token:", token)
        validated_token = UntypedToken(token)
        user, _ = JWTAuthentication().get_user(validated_token), validated_token
        print(f"[JWT Middleware] Authenticated user: {user} (ID: {user.id})")
        return user
    except (InvalidToken, TokenError) as e:
        print("[JWT Middleware] Invalid Token:", str(e))
        return AnonymousUser()
    except Exception as e:
        print("[JWT Middleware] Unexpected error:", str(e))
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        print("[JWT Middleware] Raw query string:", query_string)

        token = parse_qs(query_string).get("token", [None])[0]
        print("[JWT Middleware] Extracted token:", token)

        if token:
            scope["user"] = await get_user_from_token(token)
        else:
            print("[JWT Middleware] No token found")
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
