from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.telegram_users.views import TelegramUsersDetailViewSet, TelegramUsersChatIdDetailViewSet, \
    TelegramUsersUpdateViewSet, TelegramUsersDeleteViewSet, TelegramUsersCreateViewSet, TelegramUsersListViewSet

router = DefaultRouter()

urlpatterns = [
                  path('', TelegramUsersListViewSet.as_view(),
                       name='telegram_user-list'),
                  path('create/', TelegramUsersCreateViewSet.as_view(),
                       name='telegram_users-create'),
                  path('chat_id/<str:chat_id>/', TelegramUsersChatIdDetailViewSet.as_view(),
                       name='telegram_users-chat_id'),
                  path('detail/<int:pk>/', TelegramUsersDetailViewSet.as_view(),
                       name='telegram_users-detail'),
                  path('update/<int:pk>/', TelegramUsersUpdateViewSet.as_view(),
                       name='telegram_users-update'),
                  path('delete/<int:pk>/', TelegramUsersDeleteViewSet.as_view(),
                       name='telegram_users-delete')
              ] + router.urls
