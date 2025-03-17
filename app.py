import dash
from dash import html, dcc, Output, Input
import dash_table
import plotly.express as px
import cv2
import numpy as np
import base64
import pandas as pd
import socket
import json
import threading
import time

def draw_overlay(current_room, current_action, previous_action_overlay):
    overlay_width, overlay_height = 600, 400  
    overlay = np.ones((overlay_height, overlay_width, 3), dtype=np.uint8) * 255  
    cv2.rectangle(overlay, (0, 0), (overlay_width, overlay_height), (0, 0, 0), 4)
    
    rooms = {
        "Kitchen": (100, 200, 100, 160),
        "Bathroom": (100, 100, 100, 100),
        "Bedroom": (200, 100, 200, 100),
        "Living Room": (400, 100, 100, 260),
    }
    
    actions = {
        "Fridge": (101, 270, 25, 25),
        "Laying on Bed": (270, 101, 60, 60),
        "Sink": (169, 130, 30, 40),
        "Sitting on Couch": (469, 200, 30, 80),
    }
    
    for room_name, (x, y, w, h) in rooms.items():
        color = (154, 205, 50)  
        if room_name == current_room:
            color = (0, 165, 255)  
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), 1)
        cv2.putText(overlay, room_name, (x + 5, y + h - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (120, 120, 120), 1)
    
    for action_name, (x, y, w, h) in actions.items():
        color = (128, 128, 128)
        if action_name == current_action:
            color = (0, 255, 255)
        if action_name == previous_action_overlay:
            color = (0, 120, 120)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 0, 0), 1, lineType=cv2.LINE_AA)
    
    return overlay

def convert_image_to_base64(img):
    ret, buf = cv2.imencode('.png', img)
    if ret:
        b64 = base64.b64encode(buf).decode('utf-8')
        return f"data:image/png;base64,{b64}"
    return None

# Global variable to store the latest TCP data
latest_data = {
    "room": "Kitchen",
    "action": "Fridge",
    "previous_action": "Sink"
}

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

def tcp_listener():
    global latest_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to TCP server at {SERVER_IP}:{SERVER_PORT}")
    except Exception as e:
        print("Error connecting to TCP server:", e)
        return

    while True:
        try:
            response = sock.recv(BUFFER_SIZE)
            if response:
                data = json.loads(response.decode('utf-8'))
                print("Received TCP data:", data)
                latest_data = {
                    "room": data.get("room", "Kitchen"),
                    "action": data.get("action", "Fridge"),
                    "previous_action": data.get("previous_action", "Sink")
                }
        except Exception as e:
            print("Error receiving/parsing data:", e)
            time.sleep(1)

listener_thread = threading.Thread(target=tcp_listener, daemon=True)
listener_thread.start()

def get_garbage_graph_data():
    df_graph = pd.DataFrame({
        "Category": ["Kitchen", "Bathroom", "Bedroom", "Living", "Outside"],
        "Activities": [6, 15, 4, 3, 15]
    })
    return px.bar(df_graph, x="Category", y="Activities", title="Activites in Location")

def get_garbage_table_data():
    return [
        {"Action #": 1, "Activity": "Entered Living", "Time": "03:38:05"},
        {"Action #": 2, "Activity": "Left Living", "Time": "03:38:15"},
        {"Action #": 3, "Activity": "Entered Kitchen", "Time": "03:38:15"},
        {"Action #": 4, "Activity": "Started Fridge", "Time": "03:38:17"},
        {"Action #": 5, "Activity": "Stopped Fridge", "Time": "03:38:20"},
        {"Action #": 6, "Activity": "Left Kitchen", "Time": "03:39:33"},
        {"Action #": 7, "Activity": "Entered Bathroom", "Time": "03:39:33"},
        {"Action #": 8, "Activity": "Started Sink", "Time": "03:39:34"},
        {"Action #": 9, "Activity": "Stopped Sink", "Time": "03:39:38"},
        {"Action #": 10, "Activity": "Entered Kitchen", "Time": "03:43:15"}
    ]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Healthcare Dashboard Patient #1045"),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # update every 1000 ms
        n_intervals=0
    ),
    html.Div([
        html.Div([
            html.H2("Overlay"),
            html.Img(id='overlay-image', style={'width': '600px', 'height': '400px'})
        ], style={'padding': '20px', 'flex': '1'}),
        html.Div([
            html.H2("Graph"),
            dcc.Graph(id='graph')
        ], style={'padding': '20px', 'flex': '1'}),
        html.Div([
            html.H2("Spreadsheet"),
            dash_table.DataTable(
                id='table',
                columns=[{"name": col, "id": col} for col in ["Action #", "Activity", "Time"]],
                data=[],
                editable=True,
                row_deletable=True,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'}
            )
        ], style={'padding': '20px', 'flex': '1'})
    ], style={'display': 'flex', 'flexDirection': 'row'})
])

# Separate callback for updating the overlay
@app.callback(
    Output('overlay-image', 'src'),
    Input('interval-component', 'n_intervals')
)
def update_overlay(n):
    try:
        room = latest_data.get("room", "Kitchen")
        action = latest_data.get("action", "Fridge")
        previous = latest_data.get("previous_action", "Sink")
        overlay_img = draw_overlay(room, action, previous)
        encoded_img = convert_image_to_base64(overlay_img)
        print(f"Overlay updated at interval {n}: {latest_data}")
        return encoded_img
    except Exception as e:
        print("Error in update_overlay:", e)
        return dash.no_update

# Separate callback for updating the graph
@app.callback(
    Output('graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    try:
        fig = get_garbage_graph_data()
        return fig
    except Exception as e:
        print("Error in update_graph:", e)
        return dash.no_update

# Separate callback for updating the table
@app.callback(
    Output('table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_table(n):
    try:
        table_data = get_garbage_table_data()
        return table_data
    except Exception as e:
        print("Error in update_table:", e)
        return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
