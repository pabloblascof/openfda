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

        def send_file(file):
            with open(file) as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        def search_ingredient (active_ingredient, limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=active_ingredient:%s&limit=%s" % (active_ingredient, limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("info.html","w"):
                self.wfile.write(bytes("<ol>"+"\n","utf8"))
                for element in repos["results"]:
                    elementli="<li>"+element["openfda"]["brand_name"][0]+"</li>"+"\n"
                    self.wfile.write(bytes(elementli, "utf8"))

        def search_company (company, limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=openfda.manufacturer_name:%s&limit=%s" % (company, limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for element in repos["results"]:
                    elementli = "<li>" + element["openfda"]["brand_name"][0] + "</li>" + "\n"
                    self.wfile.write(bytes(elementli, "utf8"))

        def list_drugs (limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for element in repos["results"]:
                    elementli = "<li>" + element["openfda"]["brand_name"][0] + "</li>" + "\n"
                    self.wfile.write(bytes(elementli, "utf8"))

        def list_companies (limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for element in repos["results"]:
                    elementli = "<li>" + element["openfda"]["manufacturer_name"][0] + "</li>" + "\n"
                    self.wfile.write(bytes(elementli, "utf8"))

        def list_warnings (limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for element in repos["results"]:
                    elementli = "<li>" + element["warnings"][0] + "</li>" + "\n"
                    self.wfile.write(bytes(elementli, "utf8"))


        path = self.path

        if path == "/":
            with open("search.html") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        elif 'searchDrug' in path:
            active_ingredient = path.split("=")[1].split("&")[0]
            limit = path.split("=")[2]
            search_ingredient(active_ingredient,limit)
            file = 'info.html'
            send_file(file)

        elif 'searchCompany' in path:
            company = path.split("=")[1].split("&")[0]
            limit = path.split("=")[2]
            search_company(company,limit)
            file = 'info.html'
            send_file(file)

        elif 'listDrugs' in path:
            limit = path.split("=")[1].split("&")[0]
            list_drugs(limit)
            file = 'info.html'
            send_file(file)

        elif 'listCompanies' in path:
            limit = path.split("=")[1].split("&")[0]
            list_companies(limit)
            file = 'info.html'
            send_file(file)

        elif 'listWarnings' in path:
            limit = path.split("=")[1].split("&")[0]
            list_warnings(limit)
            file = 'info.html'
            send_file(file)
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

