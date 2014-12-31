# Import statements
from db_functions import (
    create_todo_list,
    get_todo_list,
    get_todo_lists,
    update_todo_list,
    delete_todo_list
)

from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    request
)

# Flask App Setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"

# Routes


@app.route("/")
@app.route("/show")
def show():
    """Main page of app

    Features:
    Listing of all todo lists
    Links to viewing, editing and deleting todo lists
    Link to add todo list
    """
    todo_lists = get_todo_lists()
    context = {
        "todo_lists": todo_lists
    }
    return render_template("show.html", **context)


@app.route("/a_list/<id>")
def a_list(id):
    """Page for individual todo list

    It takes an id parameter which is
    uses to search for a todo list.
    It displays the title and the
    description for the todo list
    """
    my_todo_list = get_todo_list(id)
    context = {
        "title": my_todo_list["title"],
        "description": my_todo_list["description"]
    }
    return render_template("a_list.html", **context)


@app.route("/delete/<id>")
def delete(id):
    delete_list_result = delete_todo_list(id)
    flash(delete_list_result)
    return redirect(url_for("show"))


@app.route("/edit/<id>", methods=["POST", "GET"])
def edit(id):
    """Function to display a form to/and edit a given todo list.

    If the request method is POST it creates an a dictionary with
    the id parameter, the title and description from the POST data.
    Using this dictionary it creates a new entry in the db.

    If the request method is GET it displays the form to edit the
    todo list. Which POSTs the updated info back here.
    """
    if request.method == "POST":
        my_todo_list = {
            "id": id,
            "title": request.form["title"].rstrip(),
            "description": request.form["description"].rstrip()
        }
        result = update_todo_list(my_todo_list)
        flash(result)
        return redirect(url_for("show"))
    else:
        my_todo_list = get_todo_list(id)
        return render_template("edit.html", **my_todo_list)


@app.route("/add", methods=["POST", "GET"])
def add():
    """Function to display a form to add a todo list.

    If the request method is POST it creates a todo list
    using the POST data/

    If the request method is GET it displays the form to add a
    todo list. Which POSTs the info back here.
    """
    if request.method == "POST":
        result = create_todo_list(
            request.form["title"].rstrip(),
            request.form["description"].rstrip()
        )
        flash(result)
        return redirect("/show")
    else:
        return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
