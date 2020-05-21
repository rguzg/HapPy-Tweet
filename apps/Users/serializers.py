from rest_framework.serializers import ModelSerializer
from apps.Users.models import Classifier

class read_classifier_serializer(ModelSerializer):
    class Meta:
        model = Classifier
        fields = ['name']

class write_classifier_serializer(ModelSerializer):
    class Meta:
        model = Classifier
        fields = ['name', 'location']
    