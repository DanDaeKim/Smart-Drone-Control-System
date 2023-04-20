import heapq
import math

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def in_bounds(self, point):
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, point):
        x, y = point
        neighbors = [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1),
        ]
        return filter(self.in_bounds, neighbors)

class FlightPathOptimizer:
    def __init__(self, grid, airspace_manager, altitude_range=(100, 500)):
        self.grid = grid
        self.airspace_manager = airspace_manager
        self.altitude_range = altitude_range

    def heuristic(self, point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def a_star_search(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for next in self.grid.get_neighbors(current):
                new_cost = cost_so_far[current] + self.heuristic(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        return came_from, cost_so_far

    def reconstruct_path(self, came_from, start, goal):
        path = [goal]
        node = goal
        while node != start:
            node = came_from[node]
            path.append(node)
        path.reverse()
        return path

    def find_optimal_path(self, start, goal):
        came_from, _ = self.a_star_search(start, goal)
        path = self.reconstruct_path(came_from, start, goal)
        return path

    def optimize_path(self, start, goal):
        optimal_path = self.find_optimal_path(start, goal)
        for point in optimal_path:
            _, airspace = self.airspace_manager.get_airspace_by_location(point)
            if airspace is not None:
                optimal_altitude = self.find_optimal_altitude(airspace)
                point = (point[0], point[1], optimal_altitude)
        return optimal_path

    def find_optimal_altitude(self, airspace):
        return max(self.altitude_range[0], min(airspace.radius, self.altitude_range[1]))
