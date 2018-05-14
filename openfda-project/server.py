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

    def build_html(self, info):

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

        brand_list = []
        for i in range(len(info['results'])):
            try:
                for n in range(len(info['results'][i]["openfda"]["brand_name"])):
                    try:
                        brand_list.append(info['results'][i]["openfda"]["brand_name"][0])
                    except KeyError:
                        brand_list.append("Unknown")
                        break
            except KeyError:
                brand_list.append("Unknown")
                continue
        return brand_list
    
    def parse_warnings(self, info):

        warning_list = []

        for i in range(len(info['results'])):
            try:
                if "warnings" in info["results"][i]:
                    warning_list.append(info['results'][i]['warnings'][0])
                else:
                    warning_list.append("Unknown")
            except KeyError:
                warning_list.append("Unknown")
                continue

        return warning_list

    def parse_companies(self, info):
        manufacturer_list = []
        for i in range(len(info['results'])):
            try:
                for n in range(len(info['results'][i]["openfda"]["manufacturer_name"])):
                    try:
                        manufacturer_list.append(info['results'][i]["openfda"]["manufacturer_name"][0])
                    except KeyError:
                        manufacturer_list.append("Unknown")
                        break
            except KeyError:
                manufacturer_list.append("Unknown")
                continue
        return manufacturer_list

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        client = OpenFDAClient()
        parser = OpenFDAParser
        html = OpenFDAHTML

        path = self.path

        if path == "/" or 'searchDrug' in path or 'searchCompany' in path or 'listDrugs' in path or 'listCompanies' in path or 'listWarnings' in path:
            status_code = 200
        elif 'secret' in path:
            status_code = 401
        elif 'redirect' in path:
            status_code = 302
        else:
            status_code = 404

        # Send response status code

        self.send_response(status_code)

        if path == "/" or 'searchDrug' in path or 'searchCompany' in path or 'listDrugs' in path or 'listCompanies' in path or 'listWarnings' in path:
            self.send_header('Content-type', 'text/html')
        elif 'secret' in path:
            self.send_header('WWW-Authenticate', 'Basic realm="OpenFDA Private Zone"')
        elif 'redirect' in path:
            self.send_header('Location', 'http://localhost:8000/')

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()



        if path == "/":
            print('"search.html" oppened')
            contents = html.send_file(self, "search.html")
            self.wfile.write(bytes(contents, "utf8"))

        elif 'searchDrug'in path:
            print ('Client request: searchDrug')
            active_ingredient = path.split("=")[1].split("&")[0]
            if 'limit' in path:
                limit = path.split("=")[2]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            info = client.search_drugs(active_ingredient, limit)
            drugs_list = parser.parse_drugs(self, info)
            contents = html.build_html(self, drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'searchCompany' in path:
            print('Client request: searchCompany')
            company = path.split("=")[1].split("&")[0]
            if 'limit' in path:
                limit = path.split("=")[2]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            info = client.search_companies(company, limit)
            company_list = parser.parse_companies(self, info)
            contents = html.build_html(self, company_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listDrugs' in path:
            print('Client request: listDrugs')
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            info = client.list_drugs(limit)
            drugs_list = parser.parse_drugs(self, info)
            contents = html.build_html(self, drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listCompanies' in path:
            print('Client request: listCompanies')
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            info = client.list_drugs(limit)
            drugs_list = parser.parse_companies(self, info)
            contents = html.build_html(self, drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listWarnings' in path:
            print('Client request: listWarnings')
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            info = client.list_drugs(limit)
            warning_list = parser.parse_warnings(self, info)
            contents = html.build_html(self, warning_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'secret' in path:
            status_code = 401
            print('Status code:' + str(status_code))
        elif 'redirect' in path:
            status_code = 302
            print('Status code:' + str(status_code))
        else:
            status_code = 404
            print('Status code:' + str(status_code))
            with open("not_found.html") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

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

