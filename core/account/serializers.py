from django.utils.translation import gettext_lazy as _
from .models import Role,UserProfile
from rest_framework import serializers
# from account.models import User 
from rest_framework_simplejwt.tokens import RefreshToken
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
                user = User.objects.get(email=email,role__role= 'user')
            except User.DoesNotExist:
                user = User.objects.create_user(email=email) # FIXME: this throw 500 error when compant email is there 
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
    
class CustomerProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # exclude  = ['user','updated_at','created_at','id']
        fields = ['fullname','resume_file']
    

class CompanyAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
    )
    
    def validate(self, attrs):
        email = attrs.get("email",None)

        if email:
            try:
                company = User.objects.get(email=email,role__role='company')
            except User.DoesNotExist:
                msg = _('Your Company Email Doesn\'t exist.\nFor more informations , please contact supports.')
                raise serializers.ValidationError(msg, code="authentication")
            except Exception:
                msg = _('Something went wrong!\nPlease try again later.')
                raise serializers.ValidationError(msg, code="authorization")      
            
        else:
            msg = _('Must include "email".')
            raise serializers.ValidationError(msg, code="authorization")
        

        refresh = RefreshToken.for_user(company)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    