import uuid 

from flask import Flask, request, jsonify, abort


# initialisiere Flask Server
app = Flask(__name__)

# erstelle einige Beispiel-IDs für Todo-Listen und Einträge, damit die API direkt mit Beispieldaten getestet werden kann
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# definiere interne Datenstrukturen mit Beispieldaten
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list_id': todo_list_1_id, 'user_id': str(uuid.uuid4())},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list_id': todo_list_2_id, 'user_id': str(uuid.uuid4())},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list_id': todo_list_3_id, 'user_id': str(uuid.uuid4())},
    {'id': todo_4_id, 'name': 'Eier', 'description': '', 'list_id': todo_list_1_id, 'user_id': str(uuid.uuid4())},
]

# füge Header hinzu, um Zugriff auf die API auf diesem Server zu ermöglichen, notwendig für die Verwendung der Vorschau im Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Endpunkt: GET /todo-list/{list_id} - Liefert alle Einträge einer Todo-Liste zurück
# Endpunkt: POST /todo-list/{list_id} - Fügt einen Eintrag zu einer bestehenden Todo-Liste hinzu
# Endpunkt: DELETE /todo-list/{list_id} - Löscht eine komplette Todo-Liste mit allen Einträgen
@app.route('/todo-list/<list_id>', methods=['GET', 'POST', 'DELETE'])
def handle_list(list_id):
    # finde die Todo-Liste anhand der übergebenen list_id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # wenn die übergeben list_id ungültig ist, gebe Statuscode 404 zurück
    if not list_item:
        return jsonify({'message': 'not found'}), 404
    if request.method == 'GET':
        print('Returning todo list entries...')
        return jsonify([i for i in todos if i['list_id'] == list_id])
    
# Endpunkt: POST /todo-list/{list_id} - Fügt einen Eintrag zu einer bestehenden Todo-Liste hinzu
    elif request.method == 'POST':
        new_entry = request.get_json(force=True)
        print('Got new entry to be added: {}'.format(new_entry))
        if 'name' not in new_entry:
            return jsonify({'message': 'invalid data'}), 406
        new_entry['id'] = str(uuid.uuid4())
        new_entry['list_id'] = list_id
        if 'description' not in new_entry:
            new_entry['description'] = ''
        new_entry['user_id'] = str(uuid.uuid4())
        todos.append(new_entry)
        return jsonify(new_entry), 201
# Endpunkt: DELETE /todo-list/{list_id} - Löscht eine bestehende Todo-Liste mit allen Einträgen
    elif request.method == 'DELETE':
        print('Deleting todo list and all its entries...')
        global todos
        todos = [t for t in todos if t['list_id'] != list_id]
        todo_lists.remove(list_item)
        return '', 204

# Endpunkt: PATCH /entry/{entry_id} - Aktualisiert einen bestehenden Eintrag
# Endpunkt: DELETE /entry/{entry_id} - Löscht einen einzelnen Eintrag einer Todo-Liste
@app.route('/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def handle_entry(entry_id):
    # finde den Eintrag anhand der übergebenen entry_id
    entry = None
    for t in todos:
        if str(t['id']) == entry_id:
            entry = t
            break
    if not entry:
        return jsonify({'message': 'not found'}), 404
    if request.method == 'PATCH':
        update_data = request.get_json(force=True)
        print('Got update data: {}'.format(update_data))
        if not update_data or not any(key in update_data for key in ['name', 'description']):
            return jsonify({'message': 'invalid data'}), 406
        if 'name' in update_data:
            entry['name'] = update_data['name']
        if 'description' in update_data:
            entry['description'] = update_data['description']
        return jsonify(entry), 200
    elif request.method == 'DELETE':
        print('Deleting todo entry...')
        todos.remove(entry)
        return '', 204

# Endpunkt: POST /todo-list - Fügt eine neue Todo-Liste hinzu
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    if 'name' not in new_list:
        return jsonify({'message': 'invalid data'}), 406
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 201


if __name__ == '__main__':
    # starte Flask Server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)