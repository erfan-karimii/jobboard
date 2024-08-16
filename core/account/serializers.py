from django.utils.translation import gettext_lazy as _
from .models import Role
from rest_framework import serializers
# from account.models import User 
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
    )
    
    
    def validate(self, attrs):
        email = attrs.get("email",None)

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
        

        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    

class CompanyAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
    )
    
    
    def validate(self, attrs):
        email = attrs.get("email")

        if email:
            try:
                company = Role.objects.get(role='company')
                user = User.objects.get(email=email,role=company)
            except User.DoesNotExist:
                msg = _('your company does not exists! call to our support for register')
                raise serializers.ValidationError(msg, code="authorization")      
            except Exception:
                msg = _('Something went wrong!\nPlease try again later.')
                raise serializers.ValidationError(msg, code="authorization")      
            
        else:
            msg = _('Must include "email".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs