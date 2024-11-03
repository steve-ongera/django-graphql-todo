# Django Graphql Todo App
A minimal django todo application which uses Graphql


## Requirements
- Python 3.7+


## Installation
- Clone the repo and navigate to project root.
  ```
  git clone https://github.com/madhvi-n/django-graphql-todo.git
  cd django-graphql-todo
  ```

- Create a virtual environment and activate it
```
virtualenv venv --python=python3
source venv/bin/activate
```

- Install the python dependencies
```
pip install -r requirements.txt
```

- Run the database migrations and start the development server
```
python manage.py migrate
python manage.py runserver
```

## GraphQL API:
- You can access the GraphQL API's user interface by navigating to `localhost:8000/graphql`.

#### Code Snippets

- To retrieve all todo
  ```
  query {
    todos {
      id
      title
      completed
    }
  }
  ```

- To create a todo
  ```
  mutation {
    createTodo(
      title: "Create a read list for goodreads."
    ) {
      todo {
        id
        title
        completed
      }
    }
  }
  ```

- To update a todo
  ```
  mutation {
    updateTodo(id: "1", title: "New Title", completed: true) {
      todo {
        id
        title
        completed
      }
    }
  }
  ```

- To delete a todo
  ```
  mutation {
    deleteTodo(id: "1") {
      success
    }
  }
  ```

- Search and filter for todos
  ```
  query {
    todos(completed: true, search: "example") {
      id
      title
      completed
    }
  }
  ```
