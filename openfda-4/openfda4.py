import http.server
import socketserver
import http.client
import json

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

        # Send message back to client
        if self.path == "/":
            with open("search.html") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))
        else:

            path = str(self.path)
            print(path)
            if "=" in path:
                
                drug = path[path.find("drug") + 5: path.find("&")]
                limit =path[path.find("limit") + 6:]

                headers = {'User-Agent': 'http-client'}

                conn = http.client.HTTPSConnection("api.fda.gov")
                conn.request("GET", "/drug/label.json?search=generic_name:%s&limit=%s" %(drug,limit), None, headers)
                r1 = conn.getresponse()
                print(r1.status, r1.reason)
                repos_raw = r1.read().decode("utf-8")
                repos = json.loads(repos_raw)
                conn.close()

                with open("brand_name.html","w"):
                    self.wfile.write(bytes("<ol>"+"\n","utf8"))
                    for element in repos["results"]:
                        elementli="<li>"+element["openfda"]["brand_name"][0]+"</li>"+"\n"
                        self.wfile.write(bytes(elementli, "utf8"))

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




# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open("htmlopenfda3.html", "r") as f:
             message= f.read()
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

