#!/usr/bin/env python3
"""
CTT Mesh HTTP Bridge
Provides HTTP API for browser extension to access mesh network
"""
import http.server
import socketserver
import json
import os
import hashlib

PORT = 8765
CACHE_DIR = os.path.expanduser("~/.ctt-mesh/content")

class CTTHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            # Count cache files
            cache_size = 0
            if os.path.exists(CACHE_DIR):
                for f in os.listdir(CACHE_DIR):
                    cache_size += os.path.getsize(os.path.join(CACHE_DIR, f))
            
            response = {
                "status": "online",
                "nodes": 1,
                "cache_size": cache_size
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path.startswith("/retrieve/"):
            content_hash = self.path.split("/retrieve/")[1]
            cache_file = os.path.join(CACHE_DIR, content_hash)
            
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                response = {
                    "success": True,
                    "content": content.decode('utf-8', errors='ignore'),
                    "mime_type": "text/html",
                    "source": "cache",
                    "hash": content_hash
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = {"success": False, "error": "Content not found"}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress log output
        pass

if __name__ == "__main__":
    with socketserver.TCPServer(("127.0.0.1", PORT), CTTHandler) as httpd:
        print(f"✓ CTT Mesh HTTP Bridge running on port {PORT}")
        print(f"✓ Extension can now communicate with mesh network")
        httpd.serve_forever()
