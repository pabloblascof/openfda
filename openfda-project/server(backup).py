import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000


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

        elif "searchDrug" in self.path:

            path = str(self.path)
            print(path)

            params = self.path.split("?")[1]
            drug = params.split("&")[0].split("=")[1]
            limit = params.split("&")[1].split("=")[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=generic_name:%s&limit=%s" %(drug,limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            repos = json.loads(repos_raw)
            conn.close()

            with open("info.html","w"):
                self.wfile.write(bytes("<ol>"+"\n","utf8"))
                for element in repos["results"]:
                    elementli="<li>"+element["openfda"]["brand_name"][0]+"</li>"+"\n"
                    self.wfile.write(bytes(elementli, "utf8"))

        elif "searchCompany" in self.path:

            path = str(self.path)
            print(path)

            params = self.path.split("?")[1]
            company = params.split("&")[0].split("=")[1]
            limit = params.split("&")[1].split("=")[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=openfda.manufacturer_name:%s&limit=%s" %(company,limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            repos = json.loads(repos_raw)
            conn.close()

            with open("info.html","w"):
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

