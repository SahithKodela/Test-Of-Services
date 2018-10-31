from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Register
import re

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class RegSerializer(serializers.ModelSerializer):

    class Meta:
        model = Register
        fields = ('user', 'address', 'dob')

    def validate_user(self, value):
        """
        Check that value is a valid name.
        """
        if not '@gst.com' in value:  # check name has more than 1 word
            raise serializers.ValidationError("Please enter valid email")  # raise ValidationError
        return value

    def validate_dob(self, value):
        """
        Check that value is a valid name.
        """
        if not re.match(r'\d+/\d+/\d+',value):  # check name has more than 1 word
            raise serializers.ValidationError("Please enter valid dob")  # raise ValidationError
        return value
