from rest_framework import serializers

from app.models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author_detail = AuthorSerializer(source='author', read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_detail']
        extra_kwargs = {
            'author': {'write_only': False}
        }

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Kitob nomi 2 ta xarfan koproq bolishi kerak')
        return value

    def validate(self, data):
        if Book.objects.filter(
                title=data['title'],
                author=data['author'],

        ).exists():
            raise serializers.ValidationError(
                'Bu maullif bu kitobni alloqachon yozgan!'
            )
        return data