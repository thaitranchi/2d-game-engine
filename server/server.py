from flask import Flask, request, jsonify
import json
import os
import socket
import threading

# Scoreboard server
app = Flask(__name__)
HIGH_SCORE_FILE = "highscores.json"

def load_scores():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return json.load(f)
    return []

def save_scores(scores):
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")
    if name is None or score is None:
        return jsonify({"status": "error", "message": "Missing name or score"}), 400

    scores = load_scores()
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # Keep top 10 scores
    save_scores(scores)
    return jsonify({"status": "success", "scores": scores}), 200

@app.route("/get_scores", methods=["GET"])
def get_scores():
    scores = load_scores()
    return jsonify({"scores": scores}), 200

# Multiplayer server
HOST = '0.0.0.0'
PORT = 5001

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break  # Connection closed
            # Relay data to all other clients
            for client in clients:
                if client != conn:
                    client.sendall(data)
        except Exception as e:
            print(f"[ERROR] {e}")
            break
    print(f"[DISCONNECT] {addr} disconnected.")
    clients.remove(conn)
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    start_server()
