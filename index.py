#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"message": "AgenticSeek Voice API", "status": "running", "version": "1.0"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        if self.path == '/api/voice':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                data = json.loads(post_data.decode())
                response = {"response": f"Got: {data.get('message', '')}", "status": "ok"}
            except:
                response = {"response": "Voice endpoint working", "status": "ok"}
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Server running on port {port}")
    server.serve_forever()