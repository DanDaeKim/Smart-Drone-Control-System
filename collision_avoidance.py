import numpy as np

class CollisionAvoidance:
    def __init__(self, min_distance=50, time_horizon=5, max_speed=20):
        self.min_distance = min_distance
        self.time_horizon = time_horizon
        self.max_speed = max_speed

    def get_velocity_obstacle(self, drone1, drone2):
        relative_position = np.array(drone2.location) - np.array(drone1.location)
        relative_velocity = np.array(drone2.velocity) - np.array(drone1.velocity)
        distance = np.linalg.norm(relative_position)

        if distance < self.min_distance:
            return None

        theta = np.arccos(self.min_distance / distance)
        cone_angle = np.arctan2(relative_position[1], relative_position[0])

        min_angle = cone_angle - theta
        max_angle = cone_angle + theta

        return (min_angle, max_angle)

    def get_velocity_obstacle_intersection(self, drone, other_drones):
        angles = []

        for other_drone in other_drones:
            obstacle = self.get_velocity_obstacle(drone, other_drone)
            if obstacle is not None:
                angles.append(obstacle)

        return angles

    def find_evasive_velocity(self, drone, other_drones):
        obstacles = self.get_velocity_obstacle_intersection(drone, other_drones)
        candidate_velocities = []

        for angle in np.linspace(0, 2 * np.pi, num=360):
            velocity = self.max_speed * np.array([np.cos(angle), np.sin(angle)])

            if not any(min_angle <= angle <= max_angle for min_angle, max_angle in obstacles):
                candidate_velocities.append(velocity)

        if candidate_velocities:
            return min(candidate_velocities, key=lambda v: np.linalg.norm(v - np.array(drone.velocity)))
        else:
            return drone.velocity

    def apply_evasive_maneuver(self, drones):
        for drone in drones:
            other_drones = [d for d in drones if d.id != drone.id]
            evasive_velocity = self.find_evasive_velocity(drone, other_drones)
            drone.velocity = tuple(evasive_velocity)
