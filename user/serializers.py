from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        label=_("Confirm Password"),
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "is_staff",
            "favorite_cities",
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def validate(self, attrs):
        password1 = attrs.get("password")
        password2 = attrs.get("password2")

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                _("Passwords do not match."), code="password_mismatch"
            )

        return attrs

    def create(self, validated_data):
        """Create user with encrypted password"""
        validated_data.pop("password2", None)
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update user with correctly encrypted password"""
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True,
    )
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

        else:
            msg = _("Must include 'email' and 'password'.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        return attrs

    def create(self, validated_data):
        return Token.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get("user", instance.user)
        instance.created = validated_data.get("created", instance.created)
        instance.save()
        return instance
