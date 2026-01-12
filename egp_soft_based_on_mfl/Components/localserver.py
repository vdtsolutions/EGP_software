import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler


def start():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        return httpd.serve_forever() or "hi"
    pass





