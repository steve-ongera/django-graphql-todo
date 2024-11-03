import graphene
from graphene_django import DjangoObjectType, GraphQLError
from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'completed')


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType, completed=graphene.Boolean(), search=graphene.String())

    def resolve_todos(self, info, completed=None, search=None):
        queryset = Todo.objects.all()
        if completed is not None:
            queryset = queryset.filter(completed=completed)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class CreateTodoMutation(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        title = graphene.String(required=True)
        completed = graphene.Boolean(default_value=False)

    def mutate(self, info, title, completed):
        if Todo.objects.filter(title=title).exists():
            raise GraphQLError('A todo with this title already exists.')

        todo = Todo.objects.create(title=title, completed=completed)
        return CreateTodoMutation(todo=todo)


class UpdateTodoMutation(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        completed = graphene.Boolean()

    def mutate(self, info, id, title=None, completed=None):
        try:
            todo = Todo.objects.get(id=id)
            if title is not None:
                todo.title = title
            if completed is not None:
                todo.completed = completed
                todo.save()
            return UpdateTodoMutation(todo=todo)
        except Todo.DoesNotExist:
            raise GraphQLError('Todo not found.')


class DeleteTodoMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        try:
            todo = Todo.objects.get(id=id)
            todo.delete()
            return DeleteTodoMutation(success=True)
        except Todo.DoesNotExist:
            raise GraphQLError('Todo not found.')


class Mutation(graphene.ObjectType):
    create_todo = CreateTodoMutation.Field()
    update_todo = UpdateTodoMutation.Field()
    delete_todo = DeleteTodoMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
