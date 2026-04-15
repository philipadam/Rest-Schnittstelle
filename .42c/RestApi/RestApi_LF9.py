import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_4_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Endpunkt: GET /todo-list/{list_id} - Liefert alle Einträge einer Todo-Liste zurück
@app.route('/todo-list/<list_id>', methods=['GET', 'POST'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list entries...')
        return jsonify([i for i in todos if i['list'] == list_id])
    
# Endpunkt: POST /todo-list/{list_id} - Fügt einen Eintrag zu einer bestehenden Todo-Liste hinzu
    elif request.method == 'POST':
        # add a new entry to the existing list
        new_entry = request.get_json(force=True)
        print('Got new entry to be added: {}'.format(new_entry))
        if 'name' not in new_entry:
            abort(406)  # Not Acceptable, missing required field
        # create id for new entry, save it and return the entry
        new_entry['id'] = str(uuid.uuid4())
        new_entry['list'] = list_id
        if 'description' not in new_entry:
            new_entry['description'] = ''
        todos.append(new_entry)
        return jsonify(new_entry), 201
# Endpunkt: DELETE /todo-list/{list_id} - Löscht eine bestehende Todo-Liste mit allen Einträgen
    elif request.method == 'DELETE':
        # delete the list and all its entries
        print('Deleting todo list and all its entries...')
        # remove all todos for this list
        global todos
        todos = [t for t in todos if t['list'] != list_id]
        # remove the list itself
        todo_lists.remove(list_item)
        return '', 204

# Endpunkt: POST /todo-list - Fügt eine neue Todo-Liste hinzu
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 201


if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)