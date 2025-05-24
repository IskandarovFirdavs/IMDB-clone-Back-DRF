from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Person, TitlePerson
from titles.serializers import TitleSerializer  # Assuming you have a TitleSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'birth_date', 'location', 'website', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Login yoki parol noto‘g‘ri")
        data['user'] = user
        return data


class TitlePersonSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()


    class Meta:
        model = TitlePerson
        fields = ['id', 'title', 'role', 'characters', 'order']


class PersonSerializer(serializers.ModelSerializer):
    person_titles = TitlePersonSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'birth_year', 'death_year', 'bio', 'photo', 'person_titles']