from peewee import (
    MySQLDatabase,
    CharField,
    TextField,
    Model,
)

db = MySQLDatabase("ODOT_DB", user="root", passwd="OttersR0ck")

# Models


class BaseModel(Model):
    """A model/class to act as a base for other models.

    This is to keep my code DRY by setting common elements in one place
    e.g. the db
    """
    class Meta:
        database = db


class TodoList(BaseModel):
    """A model for Todo Lists which have a title and a description"""
    _title = CharField()
    _description = TextField()


# Functions


def setup_db():
    db.connect()
    db.create_tables([TodoList])


def create_todo_list(title, description):
    """A function to create a new TodoList

    It take 2 arguments - a title and a description -
    and creates a new entry in the TodoList table.
    An auto incrementing id is automatically created to
    act as a primary key
    """
    try:
        new_todolist = TodoList(_title=title, _description=description)
        new_todolist.save()
        return "Success"
    except:
        return "Failed"


def get_todo_lists():
    """A function to get all the todo lists from the db.

    It returns the todo lists in a list of dictionaries.
    The dictionaries contain an id, title and description.
    """
    todo_lists = []
    for todo_list in TodoList.select():
        todo_lists.append(
            {
                "id": todo_list.id,
                "title": todo_list._title,
                "description": todo_list._description
            }
        )
    return todo_lists


def get_todo_list(id):
    """A function to get a single todo list from its id

    It takes one argument: id which is used to return a
    dictionary of the corresponding todo list. The
    dictionary contains an id, a title, and a description
    """
    my_todo_list = TodoList.get(id=id)
    my_todo_list_dict = {
        "id": my_todo_list.id,
        "title": my_todo_list._title,
        "description": my_todo_list._description
    }
    return my_todo_list_dict


def update_todo_list(todo_list):
    """A function to update a given todo list.

    It takes one argument which is a dictionary
    containing an id, a title and a description.

    It then finds the corresponding todo list based
    on the id the updates the title and description
    with the values from the dictionary.

    It returns Success if the updates was successful
    and Error if not.
    """
    try:
        my_todo_list = TodoList.get(TodoList.id == todo_list["id"])
        my_todo_list._title = todo_list["title"]
        my_todo_list._description = todo_list["description"]
        my_todo_list.save()
        return "Success"

    except:
        return "Error"


def delete_todo_list(id):
    """A function to delete a todo list

    It takes one argument: an id of a todo
    list. It finds the matching todo list
    and deletes it.

    It returns Success if the updates was successful
    and Error if not.
    """
    try:
        my_todo_list = TodoList.get(TodoList.id == id)
        my_todo_list.delete_instance()
        return "Success"

    except:
        return "Error"
