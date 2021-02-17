from django.contrib.auth.models import User
from rest_framework import serializers;


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=6,write_only=True)
    first_name = serializers.CharField(min_length=2)
    last_name = serializers.CharField(min_length=2)
    username = serializers.EmailField()

    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name', 'password']

    def validate(self, attrs):
        email = attrs.get('username','')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email',('This email is already in use')})
        return super().validate(attrs);

    def create(self, validated_data): #inace je ugradjeno,
        # al ako validiramo sacuvacemo smao ako su validni podaci
        return User.objects.create_user(**validated_data)