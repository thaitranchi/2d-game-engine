import socket
import threading
import json
import time

SERVER = 'localhost'  # Đổi thành IP của server nếu cần
PORT = 5001

class NetworkClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)  # Timeout 5 giây
        self.last_heartbeat = time.time()
        self.received_data = []
        self.running = True

        # Bắt đầu kết nối
        self.connect()
        self.start_receiving()
        self.start_heartbeat()

    def connect(self):
        """Thử kết nối lại khi mất tín hiệu"""
        while True:
            try:
                print(f"[CONNECTING] Connecting to {SERVER}:{PORT}...")
                self.client_socket.connect((SERVER, PORT))
                print("[CONNECTED] Connected to the server.")
                self.last_heartbeat = time.time()
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                print("[RETRYING] Reconnecting in 5 seconds...")
                time.sleep(5)

    def send_data(self, message):
        """Gửi dữ liệu đến server"""
        try:
            self.client_socket.sendall(json.dumps(message).encode())
        except Exception as e:
            print(f"[SEND ERROR] {e}")

    def send_heartbeat(self):
        """Gửi heartbeat mỗi 5 giây"""
        heartbeat_msg = {"type": "heartbeat"}
        self.send_data(heartbeat_msg)

    def start_receiving(self):
        """Chạy luồng nhận dữ liệu"""
        thread = threading.Thread(target=self.receive_data, daemon=True)
        thread.start()

    def receive_data(self):
        """Luồng lắng nghe dữ liệu"""
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    message = json.loads(data.decode())
                    # Xử lý heartbeat response
                    if message.get("type") == "heartbeat_response":
                        self.last_heartbeat = time.time()
                    else:
                        self.received_data.append(message)
                        print(f"[RECEIVED] {message}")
            except socket.timeout:
                # Timeout - kiểm tra heartbeat
                if time.time() - self.last_heartbeat > 10:
                    print("[NETWORK ERROR] No heartbeat, reconnecting...")
                    self.running = False
                    self.reconnect()
            except Exception as e:
                print(f"[ERROR] {e}")
                self.running = False
                self.reconnect()

    def start_heartbeat(self):
        """Bắt đầu gửi heartbeat liên tục"""
        def heartbeat_loop():
            while self.running:
                self.send_heartbeat()
                time.sleep(5)
        thread = threading.Thread(target=heartbeat_loop, daemon=True)
        thread.start()

    def reconnect(self):
        """Thử kết nối lại"""
        self.client_socket.close()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.start_receiving()
        self.start_heartbeat()


if __name__ == "__main__":
    client = NetworkClient()
