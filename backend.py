from flask import jsonify, Response, request
import random
import time
import json

# Project 1: Dummy data for logs (Log Aggregation Tool)
log_levels = ['INFO', 'ERROR', 'WARNING']
logs = [
    '2024-09-17 12:00:00 - INFO: Service started successfully.',
    '2024-09-17 12:05:30 - ERROR: Service failed to connect to database.',
    '2024-09-17 12:10:45 - WARNING: Service is experiencing high memory usage.'
]

def generate_logs():
    def generate():
        while True:
            log_line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {random.choice(log_levels)}: {random.choice(logs)}"
            yield f"data:{log_line}\n\n"
            time.sleep(2)
    return Response(generate(), mimetype='text/event-stream')

# Project 2: Dummy data for bottleneck detection
def generate_bottleneck_data():
    services = [
        {'name': 'nginx', 'cpu_usage': random.uniform(0, 100), 'memory_usage': random.uniform(100, 1000), 'network_latency': random.uniform(10, 500)},
        {'name': 'redis', 'cpu_usage': random.uniform(0, 100), 'memory_usage': random.uniform(100, 1000), 'network_latency': random.uniform(10, 500)},
        {'name': 'mysql', 'cpu_usage': random.uniform(0, 100), 'memory_usage': random.uniform(100, 1000), 'network_latency': random.uniform(10, 500)},
        {'name': 'elasticsearch', 'cpu_usage': random.uniform(0, 100), 'memory_usage': random.uniform(100, 1000), 'network_latency': random.uniform(10, 500)},
        {'name': 'nodejs-app', 'cpu_usage': random.uniform(0, 100), 'memory_usage': random.uniform(100, 1000), 'network_latency': random.uniform(10, 500)},
        {'name': 'postgresql', 'cpu_usage': random.uniform(0, 100), 'memory_usage': random.uniform(100, 1000), 'network_latency': random.uniform(10, 500)},
        {'name': 'apache', 'cpu_usage': random.uniform(0, 100), 'memory_usage': random.uniform(100, 1000), 'network_latency': random.uniform(10, 500)}
    ]
    return services

def stream_bottleneck_data():
    def generate():
        while True:
            data = generate_bottleneck_data()
            json_data = json.dumps(data)
            yield f"data:{json_data}\n\n"
            time.sleep(2)
    return Response(generate(), mimetype='text/event-stream')

# Project 3: Feature Rollout
feature_rollouts = {
    'new_ui': {
        'enabled_users': 0,
        'total_users': 1000,
        'user_privileges': {
            'admin': 0,
            'premium': 0,
            'regular': 0
        },
        'historical_data': []
    },
    'enhanced_security': {
        'enabled_users': 0,
        'total_users': 1000,
        'user_privileges': {
            'admin': 0,
            'premium': 0,
            'regular': 0
        },
        'historical_data': []
    },
    'dark_mode': {
        'enabled_users': 0,
        'total_users': 1000,
        'user_privileges': {
            'admin': 0,
            'premium': 0,
            'regular': 0
        },
        'historical_data': []
    }
}

def rollout_feature():
    data = request.get_json()
    feature = data.get('feature')
    user_privilege = data.get('user_privilege')
    user_count = int(data.get('user_count', 0))

    if feature not in feature_rollouts:
        return jsonify({'error': 'Feature not found'}), 400

    feature_data = feature_rollouts[feature]
    total_users = feature_data['total_users']
    enabled_users = feature_data['enabled_users']

    new_enabled_users = min(enabled_users + user_count, total_users)
    added_users = new_enabled_users - enabled_users

    feature_data['enabled_users'] = new_enabled_users
    feature_data['user_privileges'][user_privilege] += added_users

    timestamp = time.strftime('%H:%M:%S')
    percentage_enabled = (new_enabled_users / total_users) * 100
    feature_data['historical_data'].append({
        'timestamp': timestamp,
        'percentage': percentage_enabled
    })

    return jsonify({'message': 'Feature rollout updated successfully', 'feature_data': feature_data})

def get_feature_data():
    feature = request.args.get('feature')
    if feature not in feature_rollouts:
        return jsonify({'error': 'Feature not found'}), 400

    data = feature_rollouts[feature]
    return jsonify({
        'enabled_users': data['enabled_users'],
        'total_users': data['total_users'],
        'user_privileges': data['user_privileges'],
        'historical_data': data['historical_data']
    })

# Project 4: Distributed Monitoring System
node_data = {
    "Node 1": {"cpu": [], "latency": [], "status": "Healthy"},
    "Node 2": {"cpu": [], "latency": [], "status": "Healthy"},
    "Node 3": {"cpu": [], "latency": [], "status": "Healthy"}
}

time_series = []

def generate_node_data():
    # Capture the current time for the time series
    current_time = time.strftime('%H:%M:%S')
    time_series.append(current_time)
    
    if len(time_series) > 20:  # Limit the number of time points to the latest 20 (you can adjust this)
        time_series.pop(0)
    
    for node in node_data:
        node_data[node]['cpu'].append(random.uniform(0, 100))
        node_data[node]['latency'].append(random.uniform(10, 500))
        
        # Limit the history of data to match the time series length
        if len(node_data[node]['cpu']) > 20:
            node_data[node]['cpu'].pop(0)
        if len(node_data[node]['latency']) > 20:
            node_data[node]['latency'].pop(0)
        
        # Assign node health based on CPU and latency thresholds
        if node_data[node]['cpu'][-1] > 80 or node_data[node]['latency'][-1] > 400:
            node_data[node]['status'] = 'Unhealthy'
        elif node_data[node]['cpu'][-1] > 50 or node_data[node]['latency'][-1] > 300:
            node_data[node]['status'] = 'Warning'
        else:
            node_data[node]['status'] = 'Healthy'
    
    return {"time_series": time_series, "node_data": node_data}


def stream_node_data():
    def generate():
        while True:
            data = generate_node_data()  # Generate node data
            json_data = json.dumps(data)  # Convert Python dict to JSON string
            yield f"data:{json_data}\n\n"
            time.sleep(2)
    return Response(generate(), mimetype='text/event-stream')

def get_node_status():
    return jsonify(generate_node_data())

# Project 5: Kubernetes Metrics
kubernetes_data = {
    "Node 1": {"cpu": [], "memory": [], "status": "Healthy"},
    "Node 2": {"cpu": [], "memory": [], "status": "Healthy"},
    "Node 3": {"cpu": [], "memory": [], "status": "Healthy"}
}

# Time series data for the x-axis (limited to last 20 entries)
time_series = []

# Function to generate random Kubernetes data for each node
def generate_kubernetes_data():
    current_time = time.strftime('%H:%M:%S')
    time_series.append(current_time)
    
    if len(time_series) > 20:
        time_series.pop(0)

    for node in kubernetes_data:
        # Add random CPU and memory values to each node's data
        kubernetes_data[node]['cpu'].append(random.uniform(0, 100))
        kubernetes_data[node]['memory'].append(random.uniform(0, 100))

        # Keep data history to a maximum of 20 points
        if len(kubernetes_data[node]['cpu']) > 20:
            kubernetes_data[node]['cpu'].pop(0)
        if len(kubernetes_data[node]['memory']) > 20:
            kubernetes_data[node]['memory'].pop(0)

        # Set node health status based on the latest CPU usage
        if kubernetes_data[node]['cpu'][-1] > 80:
            kubernetes_data[node]['status'] = 'Critical'
        elif kubernetes_data[node]['cpu'][-1] > 50:
            kubernetes_data[node]['status'] = 'Warning'
        else:
            kubernetes_data[node]['status'] = 'Healthy'

    return {"time_series": time_series, "node_data": kubernetes_data}

# Streaming endpoint for real-time Kubernetes data
def stream_kubernetes_data():
    def generate():
        while True:
            data = generate_kubernetes_data()
            json_data = json.dumps(data)
            yield f"data:{json_data}\n\n"
            time.sleep(2)
    return Response(generate(), mimetype='text/event-stream')
def get_kubernetes_metrics():
    return jsonify(generate_kubernetes_data())

