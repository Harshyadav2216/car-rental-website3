# server.py
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os

PORT = 8000

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/register':
            self.save_data('data/users.json', post_data)
        elif self.path == '/login':
            self.check_login('data/users.json', post_data)
        elif self.path == '/book':
            self.save_data('data/bookings.json', post_data)
        else:
            self.send_error(404, 'Endpoint Not Found')

    def save_data(self, file_path, post_data):
        try:
            data = json.loads(post_data)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)

            with open(file_path, 'r') as f:
                existing = json.load(f)

            existing.append(data)
            with open(file_path, 'w') as f:
                json.dump(existing, f, indent=4)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Success")
        except Exception as e:
            self.send_error(500, str(e))

    def check_login(self, file_path, post_data):
        try:
            data = json.loads(post_data)
            with open(file_path, 'r') as f:
                users = json.load(f)

            for user in users:
                if user['email'] == data['email'] and user['password'] == data['password']:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Login Successful")
                    return

            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Invalid credentials")
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == '__main__':
    #os.chdir('group15 [car rental website ]car.com')  # Set root folder to serve frontend files
    server = HTTPServer(('', PORT), MyHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()
