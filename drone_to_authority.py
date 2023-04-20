# pip install zmq pynacl

import zmq
import threading
from nacl.public import PrivateKey, Box

class Authority:
    def __init__(self, key, bind_address, update_handler):
        self.key = key
        self.bind_address = bind_address
        self.update_handler = update_handler
        self.context = zmq.Context()
        self._running = True

        self.listener_thread = threading.Thread(target=self._listen)
        self.listener_thread.start()

    def _listen(self):
        socket = self.context.socket(zmq.REP)
        socket.bind(self.bind_address)

        while self._running:
            try:
                message = socket.recv()
                drone_id, encrypted_update = message.split(b':', 1)
                drone_key = self.drone_keys[drone_id.decode()]
                box = Box(self.key, drone_key)
                decrypted_update = box.decrypt(encrypted_update)
                self.update_handler(drone_id, decrypted_update)
                socket.send(b'ACK')
            except Exception as e:
                print(f"Error receiving update: {e}")

        socket.close()

    def stop(self):
        self._running = False
        self.listener_thread.join()

class DroneToAuthorityCommunicator:
    def __init__(self, drone, key, authority_key, authority_address, update_interval=10):
        self.drone = drone
        self.key = key
        self.authority_key = authority_key
        self.authority_address = authority_address
        self.update_interval = update_interval
        self.context = zmq.Context()
        self._running = True

        self.updater_thread = threading.Thread(target=self._send_updates)
        self.updater_thread.start()

    def _send_updates(self):
        while self._running:
            update = self.drone.get_status_update()
            box = Box(self.key, self.authority_key)
            encrypted_update = box.encrypt(update)
            payload = self.drone.id.encode() + b':' + encrypted_update

            socket = self.context.socket(zmq.REQ)
            socket.connect(self.authority_address)
            socket.send(payload)
            response = socket.recv()
            if response == b'ACK':
                print(f"Drone {self.drone.id}: update sent successfully.")
            else:
                print(f"Drone {self.drone.id}: update failed.")
            socket.close()

            time.sleep(self.update_interval)

    def stop(self):
        self._running = False
        self.updater_thread.join()
