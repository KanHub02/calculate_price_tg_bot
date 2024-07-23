# from rest_framework import serializers

# class MarkdownField(serializers.Field):
#     def to_representation(self, value):
#         # Возвращаем данные в том же формате, в котором они хранятся
#         return value

#     def to_internal_value(self, data):
#         # Проверка входных данных, если необходимо
#         if not isinstance(data, str):
#             raise serializers.ValidationError('Invalid format')
#         return data
