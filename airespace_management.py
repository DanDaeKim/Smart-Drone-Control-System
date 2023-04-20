import geopy.distance
import uuid

class Airspace:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.drones = {}

    def add_drone(self, drone):
        self.drones[drone.id] = drone

    def remove_drone(self, drone_id):
        del self.drones[drone_id]

    def is_point_inside(self, point):
        return geopy.distance.distance(self.center, point).m <= self.radius

    def get_drones_in_airspace(self):
        return list(self.drones.values())

    def is_drone_inside(self, drone):
        return self.is_point_inside(drone.location)

class Drone:
    def __init__(self, id, location):
        self.id = id
        self.location = location

class AirspaceManager:
    def __init__(self):
        self.airspaces = {}

    def create_airspace(self, center, radius):
        airspace_id = uuid.uuid4()
        self.airspaces[airspace_id] = Airspace(center, radius)
        return airspace_id

    def remove_airspace(self, airspace_id):
        del self.airspaces[airspace_id]

    def get_airspace_by_location(self, location):
        for airspace_id, airspace in self.airspaces.items():
            if airspace.is_point_inside(location):
                return airspace_id, airspace
        return None, None

    def register_drone(self, drone, airspace_id):
        if airspace_id in self.airspaces:
            self.airspaces[airspace_id].add_drone(drone)
        else:
            raise ValueError(f"Invalid airspace ID: {airspace_id}")

    def update_drone_location(self, drone_id, new_location):
        for airspace in self.airspaces.values():
            if drone_id in airspace.drones:
                if airspace.is_point_inside(new_location):
                    airspace.drones[drone_id].location = new_location
                else:
                    airspace.remove_drone(drone_id)
                    new_airspace_id, new_airspace = self.get_airspace_by_location(new_location)
                    if new_airspace is not None:
                        new_airspace.add_drone(airspace.drones[drone_id])
                break
