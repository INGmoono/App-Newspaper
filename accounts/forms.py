# accounts/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Modify your forms here
class CustomUserCreationForm (UserCreationForm ):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = (   # ampliamos la informacion de UserCreationForm
            'username',
            'email',
            'age',
        )

class CustomUserChangeForm (UserChangeForm ):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'age',
        )