from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models import QuerySet

from ..models import User
from ..serializers import UserSerializer


@api_view(["GET"])
def user_api_list(request: Request) -> Response:
    users: QuerySet[User] = User.objects.all().order_by("id")
    serializer: UserSerializer = UserSerializer(users, many=True)
    return Response({
            "status": "success",
            "message": "Users retrieved successfully.",
            "count": len(serializer.data),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    
@api_view(["POST"])
def user_api_create(request: Request) -> Response:
    serializer: UserSerializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user: User = serializer.save()
        return Response({
                "status": "success",
                "message": "User created successfully.",
                "data": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
    return Response({
        "status": "error",
        "message": "User creation failed.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)