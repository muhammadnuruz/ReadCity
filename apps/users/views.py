from rest_framework.generics import RetrieveAPIView

from apps.users.models import User
from apps.users.permissions import UserPermission
from apps.users.serializers import UserRetrieveSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [UserPermission]

    def get_object(self):
        return self.queryset.get(phone_number=self.request.user.phone_number)
