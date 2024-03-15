from django.urls import include, path

from users.views import SubscribeListView, SubscribeView

app_name = 'users'

urlpatterns = [
    path('users/subscriptions/', SubscribeListView.as_view(),
         name='subscription'),
    path('users/<int:id>/subscribe/', SubscribeView.as_view(),
         name='subscribe'),
    path('', include('djoser.urls')),
]
