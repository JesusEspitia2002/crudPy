from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = []

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    nuevo_usuario = request.get_json()
    nuevo_usuario["id"] = len(usuarios) + 1
    usuarios.append(nuevo_usuario)
    return jsonify({"mensaje": "Usuario creado", "usuario": nuevo_usuario}), 201

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({"usuarios": usuarios})

@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario:
        return jsonify({"usuario": usuario})
    return jsonify({"mensaje": "Usuario no encontrado"}), 404

@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario:
        datos = request.get_json()
        usuario.update(datos)
        return jsonify({"mensaje": "Usuario actualizado", "usuario": usuario})
    return jsonify({"mensaje": "Usuario no encontrado"}), 404

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario:
        usuarios.remove(usuario)
        return jsonify({"mensaje": "Usuario eliminado"})
    return jsonify({"mensaje": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    from threading import Thread
    import requests
    import time

    def iniciar_servidor():
        app.run(debug=False, use_reloader=False)

    servidor = Thread(target=iniciar_servidor)
    servidor.daemon = True
    servidor.start()

    time.sleep(1)

    def crear_usuario(nombre, edad):
        respuesta = requests.post("http://127.0.0.1:5000/usuarios", json={"nombre": nombre, "edad": edad})
        print("Crear Usuario:", respuesta.json())

    def obtener_usuarios():
        respuesta = requests.get("http://127.0.0.1:5000/usuarios")
        print("Obtener Usuarios:", respuesta.json())

    def obtener_usuario(id):
        respuesta = requests.get(f"http://127.0.0.1:5000/usuarios/{id}")
        print(f"Obtener Usuario {id}:", respuesta.json())

    def actualizar_usuario(id, nombre, edad):
        respuesta = requests.put(f"http://127.0.0.1:5000/usuarios/{id}", json={"nombre": nombre, "edad": edad})
        print(f"Actualizar Usuario {id}:", respuesta.json())

    def eliminar_usuario(id):
        respuesta = requests.delete(f"http://127.0.0.1:5000/usuarios/{id}")
        print(f"Eliminar Usuario {id}:", respuesta.json())

    print("Iniciando Pruebas de CRUD...\n")
    crear_usuario("Juan", 25)
    crear_usuario("Ana", 30)
    obtener_usuarios()
    obtener_usuario(1)
    actualizar_usuario(1, "Juan Perez", 26)
    obtener_usuario(1)
    eliminar_usuario(1)
    obtener_usuarios()

    print("\nPruebas Finalizadas.")
