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

    def search_drugs(self, active_ingredient, limit):

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

    def create_html(self, info):

        html_file = "<ul>"
        for element in info:
            html_file += "<li>" + element + "</li>"
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
                drug_list.append(info["openfda"]["brand_name"][0])
            except KeyError:
                drug_list.append('Unknown')
        return drug_list

    def parse_companies(self,info):
        company_list = []
        for element in info:
            try:
                company_list.append(info['results'][element]["openfda"]["manufacturer_name"][0])
            except KeyError:
                company_list.append('Unknown')
        return company_list

    def parse_warnings (self,info):
        warning_list = []
        for element in info:
            try:
                warning_list.append(info['results'][element]["warnings"][0])
            except KeyError:
                warning_list.append('Unknown')
        return warning_list

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        client = OpenFDAClient()
        html_gen = OpenFDAHTML()
        parser = OpenFDAParser()

        # Define response status code
        status_code = 200

        path = self.path

        if path == "/":
            file = 'search.html'
            contents = html_gen.send_file(self,file)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'searchDrug' in path:
            active_ingredient = path.split("=")[1].split("&")[0]
            limit = path.split("=")[2]
            info = client.search_drugs(active_ingredient, limit)
            drug_list = parser.parse_drugs(self, info)
            contents = html_gen.create_html(self, drug_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'searchCompany' in path:
            company = path.split("=")[1].split("&")[0]
            limit = path.split("=")[2]
            info = client.search_companies(company, limit)
            company_list = parser.parse_companies(self, info)
            contents = html_gen.create_html(self, company_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listDrugs' in path:
            limit = path.split("=")[1].split("&")[0]
            info = client.list_drugs(limit)
            drugs_list = parser.parse_drugs(self, info)
            contents = html_gen.create_html(self, drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listCompanies' in path:
            limit = path.split("=")[1].split("&")[0]
            info = client.list_drugs(limit)
            drugs_list = parser.parse_companies(self, info)
            contents = html_gen.create_html(self, drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listWarnings' in path:
            limit = path.split("=")[1].split("&")[0]
            info = client.list_drugs(limit)
            warning_list = parser.parse_companies(self, info)
            contents = html_gen.create_html(self, warning_list)
            self.wfile.write(bytes(contents, "utf8"))

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



