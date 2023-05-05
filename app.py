from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), default="")
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'
    
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = [{'id': task.id, 'title': task.title, 'description': task.description, 'done': task.done} for task in tasks]
    return jsonify({'tasks': result})

# Define a route to return a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({'message': 'Task not found'})
    result = {'id': task.id, 'title': task.title, 'description': task.description, 'done': task.done}
    return jsonify({'task': result})

# Define a route to create a new task
@app.route('/create', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data.get('description', ""), done=data.get('done', False))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'})


# Define a route to update an existing task
@app.route('/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({'message': 'Task not found'})
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.done = data.get('done', task.done)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

# Define a route to delete an existing task
@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({'message': 'Task not found'})
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})
