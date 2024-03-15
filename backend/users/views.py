from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPagination
from api.serializers import (
    SubscribeListSerializer, SubscribeSerializer,
    )

from users.models import Subscribe, User


class SubscribeView(APIView):
    '''
    Вью для подписок на автора.
    '''
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        serializer = SubscribeSerializer(
            data={'user': request.user.id, 'author': id},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        try:
            subscription = Subscribe.objects.get(user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subscribe.DoesNotExist:
            return Response(
                'Вы уже отписались от этого автора',
                status=status.HTTP_400_BAD_REQUEST,
            )


class SubscribeListView(ListAPIView):
    '''
    Отображение подписок с пагинацией.
    '''
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        serializer = SubscribeListSerializer(
            self.paginate_queryset(
                User.objects.filter(subscribing__user=request.user)),
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)
