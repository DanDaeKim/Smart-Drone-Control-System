# pip install pandas plotly

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class DataAnalytics:
    def __init__(self, drone_data):
        self.drone_data = pd.DataFrame(drone_data)

    def analyze_flight_duration(self):
        flight_durations = self.drone_data.groupby('drone_id')['flight_duration'].sum()
        return flight_durations

    def analyze_collision_data(self):
        collisions = self.drone_data[self.drone_data['collision'] == True]
        collision_count = collisions.groupby('drone_id')['collision'].count()
        return collision_count

    def analyze_altitude_data(self):
        avg_altitude = self.drone_data.groupby('drone_id')['altitude'].mean()
        return avg_altitude

class DataVisualization:
    def __init__(self, data_analytics):
        self.data_analytics = data_analytics

    def plot_flight_duration(self):
        flight_durations = self.data_analytics.analyze_flight_duration()
        fig = px.bar(flight_durations, x=flight_durations.index, y=flight_durations.values,
                     labels={'x': 'Drone ID', 'y': 'Flight Duration (minutes)'}, title='Flight Duration per Drone')
        fig.show()

    def plot_collision_data(self):
        collision_count = self.data_analytics.analyze_collision_data()
        fig = px.pie(collision_count, names=collision_count.index, values=collision_count.values,
                     title='Collision Count per Drone')
        fig.show()

    def plot_altitude_data(self):
        avg_altitude = self.data_analytics.analyze_altitude_data()
        fig = px.line(avg_altitude, x=avg_altitude.index, y=avg_altitude.values,
                      labels={'x': 'Drone ID', 'y': 'Average Altitude (m)'}, title='Average Altitude per Drone')
        fig.show()

    def plot_flight_paths(self, drone_paths):
        fig = go.Figure()

        for drone_id, path in drone_paths.items():
            path_data = pd.DataFrame(path, columns=['x', 'y', 'z'])
            fig.add_trace(go.Scatter3d(x=path_data['x'], y=path_data['y'], z=path_data['z'],
                                       mode='lines+markers', name=drone_id))

        fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
                          title='Flight Paths of Drones')
        fig.show()
        
    drone_data = [
{'drone_id': 'drone1', 'flight_duration': 20, 'collision': False, 'altitude': 150},
{'drone_id': 'drone1', 'flight_duration': 30, 'collision': True, 'altitude': 120},
{'drone_id': 'drone2', 'flight_duration': 25, 'collision': False, 'altitude': 200},
{'drone_id': 'drone2', 'flight_duration': 15, 'collision': False, 'altitude': 180},
{'drone_id': 'drone3', 'flight_duration': 40, 'collision': True, 'altitude': 100},
{'drone_id': 'drone3', 'flight_duration': 35, 'collision': False, 'altitude': 90},
]

