import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000

class OpenFDAClient():

    def send_query(self, query):

        site = "/drug/label.json"
        page = site + '?' + query

        print ('Requested page :', page)
        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", page, None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        res_raw = r1.read().decode("utf-8")
        conn.close()

        repos = json.loads(res_raw)
        return repos

    def search_drugs (self, active_ingredient, limit):

        query = "search=active_ingredient:%s&limit=%s" % (active_ingredient, limit)
        info = self.send_query(query)
        return info

    def search_companies(self,company, limit):

        query = "search=openfda.manufacturer_name:%s&limit=%s" % (company, limit)
        info = self.send_query(query)
        return info

    def list_drugs(self, limit):

        query = "limit=%s" % (limit)
        info = self.send_query(query)
        return info

class OpenFDAHTML():

    def create_html(self, json_list):

        html_file = "<ul>"
        for elem in json_list:
            html_file += "<li>" + elem + "</li>"
        html_file += "</ul>"

        return html_file

    def send_file(self, file):
        with open(file, "r") as f:
            message = f.read()

        return message

class OpenFDAParser():
    def parse_drugs(self, info):
        drug_list = []
        for element in info:
            try:


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        status_code = 200
        # Send headers


        # Send message back to client

        def send_file(file):
            with open(file) as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

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
                    try:
                        elementli = "<li>" + element["openfda"]["brand_name"][0] + "</li>" + "\n"
                    except KeyError:
                        elementli = "<li>" + "Unknown" + "</li>" + "\n"
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
                    try:
                        elementli = "<li>" + element["openfda"]["manufacturer_name"][0] + "</li>" + "\n"
                    except KeyError:
                        elementli = "<li>" + "Unknown" + "</li>" + "\n"
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
                    try:
                        elementli = "<li>" + element["warnings"][0] + "</li>" + "\n"
                    except KeyError:
                        elementli = "<li>" + "Unknown" + "</li>" + "\n"
                    self.wfile.write(bytes(elementli, "utf8"))


        path = self.path

        if path == "/":
            with open("search.html") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        elif 'searchDrug' in path:
            active_ingredient = path.split("=")[1].split("&")[0]
            limit = path.split("=")[2]
            search_drugs(active_ingredient,limit)
            file = 'info.html'
            send_file(file)

        elif 'searchCompany' in path:
            company = path.split("=")[1].split("&")[0]
            limit = path.split("=")[2]
            search_companies(company,limit)
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

        elif 'secret' in path:
            status_code = 401
        elif 'redirect' in path:
            status_code = 302

        else:
            status_code = 404
            with open("not_found.html") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        self.send_response(status_code)

        if 'secret' in path:
            self.send_header('WWW-Authenticate', 'Basic realm="OpenFDA Private Zone"')
        elif 'redirect' in path:
            self.send_header('Location', 'http://localhost:8000/')

        self.send_header('Content-type', 'text/html')
        self.end_headers()





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



