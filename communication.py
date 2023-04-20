# pip install zmq pynacl
import zmq
import threading
from nacl.public import PrivateKey, Box

class DroneCommunication:
    def __init__(self, drone, key, drone_keys, bind_address, message_handler):
        self.drone = drone
        self.key = key
        self.drone_keys = drone_keys
        self.bind_address = bind_address
        self.message_handler = message_handler
        self.context = zmq.Context()
        self._running = True

        self.listener_thread = threading.Thread(target=self._listen)
        self.listener_thread.start()

    def _listen(self):
        socket = self.context.socket(zmq.PULL)
        socket.bind(self.bind_address)

        while self._running:
            try:
                message = socket.recv()
                sender_id, encrypted_message = message.split(b':', 1)
                sender_key = self.drone_keys[sender_id.decode()]
                box = Box(self.key, sender_key)
                decrypted_message = box.decrypt(encrypted_message)
                self.message_handler(self.drone, sender_id, decrypted_message)
            except Exception as e:
                print(f"Error receiving message: {e}")

        socket.close()

    def send_message(self, drone_id, message):
        if drone_id not in self.drone_keys:
            raise ValueError(f"Unknown drone ID: {drone_id}")

        recipient_key = self.drone_keys[drone_id]
        box = Box(self.key, recipient_key)
        encrypted_message = box.encrypt(message)
        payload = self.drone.id.encode() + b':' + encrypted_message

        socket = self.context.socket(zmq.PUSH)
        socket.connect(recipient_key.address)
        socket.send(payload)
        socket.close()

    def stop(self):
        self._running = False
        self.listener_thread.join()
