import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Quiz, Question, Category, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")

class QuizzType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields = ("id", "title")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "title", "quiz")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("id", "question", "answer_text", "is_right")


# read data with query


class Query(graphene.ObjectType):
    # reading data

    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_questions(root, info, id):
        return Question.objects.filter(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)


class CategoryAddMutation(graphene.Mutation):
    # creating Category

    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return  CategoryAddMutation(category=category)


class CategoryUpdateMutation(graphene.Mutation):
    # updating Category

    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        # category = Category.objects.get(pk=id).update(name=name)
        category.save()
        return CategoryUpdateMutation(category=category)


class CategoryDeleteMutation(graphene.Mutation):
    # updating Category

    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        Category.objects.get(id=id).delete()


# add / update / delete with mutation

class Mutation(graphene.ObjectType):
    add_category = CategoryAddMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)