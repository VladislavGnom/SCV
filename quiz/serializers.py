from rest_framework import serializers
from .models import Test

class TestTypeSerializer(serializers.Serializer):
    '''Сериализатор для отображения типов тестов'''
    value = serializers.CharField()
    display = serializers.CharField()

class TestSerializer(serializers.ModelSerializer):
    test_type = serializers.ChoiceField(choices=Test.TestType.choices)
    type_display = serializers.CharField(
        source='get_test_type_display',
        read_only=True
    )

    class Meta:
        model = Test
        fields = ('id', 'title', 'test_type', 'type_display', 'time_limit')