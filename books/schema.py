import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = '__all__'


class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)

    def resolve_all_books(root, info):
        return Book.objects.all()


schema = graphene.Schema(query=Query)