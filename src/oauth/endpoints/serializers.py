from rest_framework import serializers


class GoogleAuth(serializers.Serializer):
    """
    Сериализация данных от гугл
    """
    email = serializers.EmailField()
    token = serializers.CharField()


EMAIL_ALLOWED_LETTERS = (
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o',
    'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k',
    'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '1',
    '2', '3', '4', '5', '6', '7', '8', '9', '0', '.'
)


class LoginOrRegister(serializers.Serializer):
    """
    Сериализация данных от пользователя
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def is_valid(self, raise_exception=False):

        for i in str(self.initial_data['email']).lower().split('@')[0]:
            if not any(i in ch for ch in EMAIL_ALLOWED_LETTERS):
                raise ValueError(f'Allowed Eng. letters, numbers 0-9, and (.)')

        return super().is_valid(raise_exception=raise_exception)
