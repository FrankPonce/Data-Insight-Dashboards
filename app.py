from flask import Flask, render_template
import os
from backend import (
    generate_logs, stream_bottleneck_data, rollout_feature, get_node_status,
    get_kubernetes_metrics, get_feature_data, stream_kubernetes_data, stream_node_data
)

app = Flask(__name__)

# Root route for the main project page
@app.route('/')
def index():
    return render_template('index.html')

# Routes for serving each project page
@app.route('/project1')
def project1():
    return render_template('project1.html')

@app.route('/project2')
def project2():
    return render_template('project2.html')

@app.route('/project3')
def project3():
    return render_template('project3.html')

@app.route('/project4')
def project4():
    return render_template('project4.html')

@app.route('/project5')
def project5():
    return render_template('project5.html')

# API routes for streaming/logging
@app.route('/log-stream')
def log_stream():
    return generate_logs()

@app.route('/rollout-feature', methods=['POST'])
def rollout_feature_route():
    return rollout_feature()

# API route for getting feature data (Project 3)
@app.route('/get-feature-data', methods=['GET'])
def get_feature_data_route():
    return get_feature_data()

@app.route('/stream-bottleneck-data')
def stream_bottleneck_data_route():
    return stream_bottleneck_data()

@app.route('/node-status')
def node_status():
    return get_node_status()

@app.route('/kubernetes-metrics')
def kubernetes_metrics():
    return get_kubernetes_metrics()

# Stream real-time Node data (Project 4)
@app.route('/stream-node-data')
def stream_node_data_route():
    return stream_node_data()

# Stream real-time Kubernetes data (Project 5)
@app.route('/stream-kubernetes-data')
def stream_kubernetes_data_route():
    return stream_kubernetes_data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Fallback to 5000 if PORT not set
    app.run(debug=True, host='0.0.0.0', port=port)
