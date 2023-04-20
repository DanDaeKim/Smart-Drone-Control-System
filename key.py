from nacl.public import PrivateKey

def message_handler(drone, sender_id, message):
    print(f"Drone {drone.id} received message from {sender_id}: {message}")

drone1_key = PrivateKey.generate()
drone2_key = PrivateKey.generate()

drone_keys = {
    "drone1": drone1_key.public_key,
    "drone2": drone2_key.public_key,
}

drone1 = Drone("drone1", (0, 0))
drone2 = Drone("drone2", (0, 0))

drone1_comm = DroneCommunication(drone1, drone1_key, drone_keys, "tcp://*:5555", message_handler)
drone2
