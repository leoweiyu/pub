from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import subprocess

app = Flask(__name__)
#CORS(app)  # Enables CORS for all routes
CORS(app, origins=["http://localhost:5173"])
#CORS(app, resources={r"/submit": {"origins": "http://localhost:5173"}})

@app.route('/submit', methods=['POST'])
@cross_origin(origin='http://localhost:5173')
def submit():
  data = request.get_json()

  hostname = data.get('hostname')
  namespace = data.get('namespace')
  live_pod_name = data.get('livePodName')

  gateway = "dummy_gateway"
  operation_mode = "tcp"
  tcp_istio_cluster = "outbound|8083||twistlock-console.anz-sec-twst.svc.cluster.local"

  dummy_certificate = "dummy_cert"
  dummy_certificate_status = "active"
  dummy_certificate_begin = "2023-11-03"
  dummy_certificate_end = "2025-11-07"
  required_client_certificate = "true"
  route_name = "https.443.https.testgateway.csp-eng-general-dev"
  virtualservice_name = "dummy_virtualservice_name"
  tcp_normal_cluster = {
    "cluster_name": "dummy_tcp_cluster1",
    "normal_cluster_endpoints": [
      {"endpoint": "10.34.123.1:8009", "status": "healthy", "outlier_check": "OK"},
      {"endpoint": "10.34.123.2:8009", "status": "healthy", "outlier_check": "OK"}
    ]
  }
  tcp_weighted_clusters = [
    {
      "cluster_name": "dummy_tcp_cluster1",
      "cluster_weight": "80",
      "weighted_cluster_endpoints": [
        {"endpoint": "10.34.123.1:8009", "status": "healthy", "outlier_check": "OK"},
        {"endpoint": "10.34.123.2:8009", "status": "healthy", "outlier_check": "OK"}
      ]
    },
    {
      "cluster_name": "dummy_tcp_cluster2",
      "cluster_weight": "20",
      "weighted_cluster_endpoints": [
        {"endpoint": "10.34.123.4:8009", "status": "healthy", "outlier_check": "OK"},
        {"endpoint": "10.34.123.5:8009", "status": "healthy", "outlier_check": "OK"}
      ]
    }
  ]

  http_normal_clusters = [
    {
      "dummy_cluster_name": "dummy_normal_cluster1",
      "match": {
        "prefix": "/",
        "case_sensitive": "true",
      },
      "normal_cluster_endpoint": [
        {"endpoint": "10.34.123.1:8009", "status": "healthy", "outlier_check": "OK"}
      ]
    }
  ]

  http_weighted_clusters = [
    {
      "match": {
	"prefix": "/api",
	"case_sensitive": "true"
      },
      "weighted_clusters": [
        {
	  "cluster_name": "dummy_weighted_cluster1",
	  "cluster_weight": "20",
	  "weighted_cluster_endpoints": [
	    {"endpoint": "10.34.123.1:8009", "status": "healthy", "outlier_check": "OK"}
	  ]
	}
      ]
    }
  ]



  backends = [
    {"endpoint": "192.168.1.1:8083", "status":"HEALTHY", "outlier_check": "OK", "cluster": "outbound|8083||twistlock-console.anz-sec-twst.svc.cluster.local"},
    {"endpoint": "192.168.1.2:8083", "status":"HEALTHY", "outlier_check": "OK", "cluster": "outbound|8083||twistlock-console.anz-sec-twst.svc.cluster.local"},
    {"endpoint": "192.168.1.3:8083", "status":"HEALTHY", "outlier_check": "OK", "cluster": "outbound|8083||twistlock-console.anz-sec-twst.svc.cluster.local"}
  ]

  response = {
    "operation_mode": operation_mode,
    "cluster": tcp_istio_cluster,
    "certificate": dummy_certificate,
    "certificate_status": dummy_certificate_status,
    #"tcp_normal_cluster": tcp_normal_cluster
    "tcp_weighted_clusters": tcp_weighted_clusters
  }

  return jsonify(response)

if __name__ == '__main__':
  app.run(debug=True)

