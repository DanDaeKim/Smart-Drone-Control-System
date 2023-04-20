from nacl.public import PrivateKey

# Define a message handler function
def message_handler(drone_id, message):
    print(f"Message from {drone_id}: {message}")

drone1_key = PrivateKey.generate()
drone2_key = PrivateKey.generate()
drone3_key = PrivateKey.generate()

drone_keys = {
    "drone1": drone1_key.public_key,
    "drone2": drone2_key.public_key,
    "drone3": drone3_key.public_key,
}

drone1 = Drone("drone1", (0, 0))
drone2 = Drone("drone2", (0, 0))
drone3 = Drone("drone3", (0, 0))

# Create DroneCommunication instances for each drone
drone1_comm = DroneCommunication(drone1, drone1_key, drone_keys, "tcp://*:5555", message_handler)
drone2_comm = DroneCommunication(drone2, drone2_key, drone_keys, "tcp://*:5556", message_handler)
drone3_comm = DroneCommunication(drone3, drone3_key, drone_keys, "tcp://*:5557", message_handler)



