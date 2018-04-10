import http.server
import socketserver

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 9007


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path =="/":
        # Send message back to client
            with open("index.html","r") as f:
                index=f.read()       
                message =index
        # Write content as utf-8 data
        elif self.path =="/new":
            with open("new.html","r") as f:
                new =f.read()
                message = new
        else:
            with open("error.html","r") as f:
                error= f.read()
                message= error
            
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")

