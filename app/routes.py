from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime

main = Blueprint('main', __name__)

# Dados em memória
tasks = []
CATEGORIES = ['Pessoal', 'Trabalho', 'Estudos', 'Compras', 'Outros']
PRIORITIES = ['Baixa', 'Média', 'Alta', 'Urgente']

class Task:
    def __init__(self, id, title, category='Outros', priority='Média'):
        self.id = id
        self.title = title
        self.category = category
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now()
        self.description = ""

def get_next_id():
    return len(tasks) + 1 if tasks else 1

@main.route('/')
def index():
    filtered_tasks = tasks.copy()
    
    # Aplicar filtros de forma mais eficiente
    filters = {
        'search': request.args.get('search', '').lower(),
        'category': request.args.get('category', ''),
        'priority': request.args.get('priority', ''),
        'status': request.args.get('status', '')
    }

    if filters['search']:
        filtered_tasks = [
            task for task in filtered_tasks 
            if filters['search'] in task.title.lower() 
            or (task.description and filters['search'] in task.description.lower())
        ]
    
    if filters['category']:
        filtered_tasks = [
            task for task in filtered_tasks 
            if task.category == filters['category']
        ]
    
    if filters['priority']:
        filtered_tasks = [
            task for task in filtered_tasks 
            if task.priority == filters['priority']
        ]
    
    if filters['status']:
        is_completed = filters['status'] == 'completed'
        filtered_tasks = [
            task for task in filtered_tasks 
            if task.completed == is_completed
        ]

    # Ordenar tarefas: primeiro as não completadas, depois por prioridade
    priority_order = {
        'Urgente': 0,
        'Alta': 1,
        'Média': 2,
        'Baixa': 3
    }
    
    filtered_tasks.sort(key=lambda x: (x.completed, priority_order.get(x.priority, 4)))

    # Estatísticas para o dashboard
    stats = {
        'total': len(tasks),
        'completed': len([t for t in tasks if t.completed]),
        'pending': len([t for t in tasks if not t.completed]),
        'urgent': len([t for t in tasks if t.priority == 'Urgente'])
    }

    return render_template('index.html', 
                         tasks=filtered_tasks,
                         categories=CATEGORIES,
                         priorities=PRIORITIES,
                         stats=stats)

@main.route('/add_task', methods=['POST'])
def add_task():
    if not request.form.get('title'):
        return redirect(url_for('main.index'))
        
    task = Task(
        id=get_next_id(),
        title=request.form.get('title'),
        category=request.form.get('category', 'Outros'),
        priority=request.form.get('priority', 'Média')
    )
    task.description = request.form.get('description', '')
    tasks.append(task)
    
    return redirect(url_for('main.index'))

@main.route('/task/<int:id>')
def get_task(id):
    task = next((task for task in tasks if task.id == id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    return jsonify({
        'id': task.id,
        'title': task.title,
        'category': task.category,
        'priority': task.priority,
        'description': task.description,
        'completed': task.completed
    })

@main.route('/edit_task/<int:id>', methods=['POST'])
def edit_task(id):
    task = next((task for task in tasks if task.id == id), None)
    if task:
        task.title = request.form.get('title', task.title)
        task.category = request.form.get('category', task.category)
        task.priority = request.form.get('priority', task.priority)
        task.description = request.form.get('description', task.description)
    return redirect(url_for('main.index'))

@main.route('/complete_task/<int:id>')
def complete_task(id):
    task = next((task for task in tasks if task.id == id), None)
    if task:
        task.completed = not task.completed
    return redirect(url_for('main.index'))

@main.route('/delete_task/<int:id>', methods=['GET', 'POST', 'DELETE'])
def delete_task(id):
    global tasks
    task = next((task for task in tasks if task.id == id), None)
    
    if not task:
        if request.method == 'DELETE':
            return jsonify({'error': 'Task not found'}), 404
        return redirect(url_for('main.index'))
    
    tasks = [t for t in tasks if t.id != id]
    
    if request.method == 'DELETE':
        return jsonify({'success': True})
    return redirect(url_for('main.index'))