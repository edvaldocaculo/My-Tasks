from flask import Flask, request,jsonify
from models.task import Task


app = Flask(__name__)

increment_task_id =1
tasks =[]


@app.route('/')
def index():
    return 'Conectado com o flask'

@app.route('/tasks', methods=['POST',])
def create_task():
    global increment_task_id
    data = request.get_json()
    new_task = Task(id=increment_task_id, title=data.get('title'), description=data.get('description'))
    increment_task_id +=1
    tasks.append(new_task)
    print(tasks)
    return jsonify({'message':'Nova tarefa criada teste', 'id':new_task.id})

@app.route('/tasks/list', methods=['GET',])
def get_tasks():
    list_tasks =[]
    for task in tasks:
        list_tasks.append(task.to_dict())
    
    output = {
        'tasks': list_tasks,
        'total_tasks': len(tasks)
    }
    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict()), 200
    
    return jsonify({'message':'Nenhuma tarefa encontrada'}), 404

@app.route('/tasks/update/<int:id>', methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
    
    if task == None:
        return jsonify({'message':'task não foi encontrada'})
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    return jsonify({'message':'Tarefa atualizada com sucesso!!'})

@app.route('/tasks/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    
    if not task:
        return jsonify({'message':'nenhuma tarefa encontrada'})
    
    tasks.remove(task)
    return jsonify({'message':f'a tarefa {task.title} foi removida com sucesso'})


app.run(debug=True)