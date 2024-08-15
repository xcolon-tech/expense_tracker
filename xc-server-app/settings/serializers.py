from rest_framework import serializers
from .models import Profile, Budget

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password', write_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'mobile', 'password']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.save()

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        if user_data.get('password'):
            user.set_password(user_data.get('password'))
        user.save()

        return instance

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'category', 'limit']