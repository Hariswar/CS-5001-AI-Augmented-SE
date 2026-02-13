from flask import Flask, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest

app = Flask(__name__)

todos = []

class ToDo:
    def __init__(self, id, task, completed=False):
        self.id = id
        self.task = task
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "task": self.task,
            "completed": self.completed
        }

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo.id == todo_id), None)
    if todo is None:
        raise NotFound("Todo not found")
    return jsonify(todo.to_dict())

@app.route('/todos', methods=['POST'])
def create_todo():
    if not request.is_json:
        raise BadRequest("Request must be JSON")
    data = request.get_json()
    if not data or 'task' not in data:
        raise BadRequest("Missing task field")
    new_todo = ToDo(id=len(todos) + 1, task=data['task'], completed=data.get('completed', False))
    todos.append(new_todo)
    return jsonify(new_todo.to_dict()), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((todo for todo in todos if todo.id == todo_id), None)
    if todo is None:
        raise NotFound("Todo not found")
    if not request.is_json:
        raise BadRequest("Request must be JSON")
    data = request.get_json()
    if 'task' in data:
        todo.task = data['task']
    if 'completed' in data:
        todo.completed = data['completed']
    return jsonify(todo.to_dict())

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todo = next((todo for todo in todos if todo.id == todo_id), None)
    if todo is None:
        raise NotFound("Todo not found")
    todos = [t for t in todos if t.id != todo_id]
    return jsonify({"message": "Todo deleted"}), 200

@app.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({"error": str(e)}), 404

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
