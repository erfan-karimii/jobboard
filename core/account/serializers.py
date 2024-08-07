
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from account.models import User 

class CustomAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
    )
    
    
    def validate(self, attrs):
        email = attrs.get("email")

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(email=email)
            except Exception:
                msg = _('Something went wrong!\nPlease try again later.')
                raise serializers.ValidationError(msg, code="authorization")      
            
        else:
            msg = _('Must include "email".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs