from rest_framework import serializers
from books.models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=1, required=True)
    page_size = serializers.IntegerField(min_value=1, required=True)