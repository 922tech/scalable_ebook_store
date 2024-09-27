from rest_framework import serializers
from rest_framework import serializers

from apps.common.serializers import BaseSerializer
from apps.common.utils import validate_iran_mobile_number
from .models import Profile


class OTPLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15, validators=[
                                         validate_iran_mobile_number])  # Adjust max_length as needed


class ProfileSerializer(BaseSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileWalletChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['wallet_charge']
