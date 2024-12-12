from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulazione di un "database" di utenti vulnerabile
users = {
    "admin": "password123",
    "user": "userpass"
}

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # SQL injection vulnerabile: non utilizza query parametrizzate
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    # Controlla se l'utente e la password sono corretti (simulando un database)
    if username in users and users[username] == password:
        return jsonify({"status": "success", "message": "Login successful!"})
    
    # Finto errore SQL se la query non va a buon fine
    if " OR '1'='1" in query:
        return jsonify({"status": "error", "message": "SQL Injection successful!"}), 400
    
    return jsonify({"status": "error", "message": "Invalid credentials"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
