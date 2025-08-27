import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/':
            response = {"message": "API is working!", "status": "ok"}
        elif self.path == '/health':
            response = {"status": "healthy"}
        else:
            response = {"error": "Not found"}
            
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"message": "POST received", "status": "ok"}
        self.wfile.write(json.dumps(response).encode())

port = int(os.environ.get('PORT', 8000))
server = HTTPServer(('0.0.0.0', port), SimpleHandler)
print(f"Starting server on port {port}")
server.serve_forever()