import http.server
import socketserver
import http.client
import json

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000
socketserver.TCPServer.allow_reuse_adress = True

# HTTPRequestHandler class
class OpenFDAClient():
# include the logic to communicate with the OpenFDA remote API

    def send_query(self, request_ending): # useful to obtain a jsonlist
        # send a query (implemented by request_ending) and returns the data obtained from the search
        request_default = "/drug/label.json"
        full_query = request_default + '?' + request_ending

        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", full_query, None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        repos = json.loads(repos_raw)
        return repos

    def list_drugs(self, limit = 10): # useful for drug_list, warning_list, company_list (just limit paremeter os requiered)
        # implements request by adding a limit parameter and call send_request to obtain the corresponding Json list
        request_ending = "limit=%s" % (limit)
        json_list = self.send_query(request_ending)
        print('_____json list has been returned: parameters: limit = %s______' % limit)
        return json_list

    def search_drugs(self, active, limit = 10): # useful for active_ingredient
        # implements request by adding an active_ingredient and a limit parameter to obtain the corresponding Json list
        request_ending = "search=active_ingredient:%s&limit=%s" % (active, limit)
        json_list = self.send_query(request_ending)
        print('_____json list has been returned: parameters: active = %s , limit = %s ______' % (active, limit))
        return json_list

    def search_companies(self, manufacturer, limit = 10):  # searches for manufacturer_name / returns brand_name
        # implements request by adding a manufacturer_name and limit parameter to obtain the corresponding Json list
        request_ending = "search=openfda.manufacturer_name:%s&limit=%s" % (manufacturer, limit)
        json_list = self.send_query(request_ending)
        print('_____json list has been returned: parameters: manufacturer = %s , limit = %s ______' % (manufacturer, limit))
        return json_list


class OpenFDAParser():
# includes the logic to extract the data from drugs items
    def parse_drugs(self, json_list): # useful in active_ingredients, manufacturer_list
        # called to return a list containing brand_names:
        brand_list = []
        for i in range(len(json_list['results'])):
            try:
                for n in range(len(json_list['results'][i]["openfda"]["brand_name"])):
                    try:
                        brand_list.append(json_list['results'][i]["openfda"]["brand_name"][0])
                    except KeyError:
                        brand_list.append("Unknown")
                        break
            except KeyError:
                brand_list.append("Unknown")
                continue
        return brand_list

    def parse_warnings(self, json_list): # useful for warning_list
    # called to return a list containing warnings
        warning_list = []
        for i in range(len(json_list['results'])):
            try:
                for n in range(len(json_list['results'][i]["openfda"]["brand_name"])):
                    try:
                        warning_list.append(json_list['results'][i]["warnings"][0])
                    except KeyError:
                        warning_list.append("Unknown")
                        break
            except KeyError:
                warning_list.append("Unknown")
                continue
        return warning_list

    def parse_companies(self, json_list): # useful for manufacturer_list
        # called to return a list containing manufacturers
        manufacturer_list = []
        for i in range(len(json_list['results'])):
            try:
                for n in range(len(json_list['results'][i]["openfda"]["manufacturer_name"])):
                    try:
                        manufacturer_list.append(json_list['results'][i]["openfda"]["manufacturer_name"][0])
                    except KeyError:
                        manufacturer_list.append("Unknown")
                        break
            except KeyError:
                manufacturer_list.append("Unknown")
                continue
        return manufacturer_list

class OpenFDAHTML():
    def create_html(self, json_list): # useful for all
        # takes in a jasonlist and writes element by element in an html file
        html_file = "<ul>"
        for elem in json_list:
            html_file += "<li>" + elem + "</li>"
        html_file += "</ul>"
        html_file += "<marquee>powered by Lasonata</marquee>"
        print("html file has been built")
        return html_file

    def send_file(self, file):
        with open(file, "r") as f:
            content = f.read()
        print(file, "is to be sent")
        return content

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        # let's create three instances
        client = OpenFDAClient()
        parser = OpenFDAParser
        html = OpenFDAHTML

        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        path = self.path
        if path != "/favicon.ico":
            print("_____path is: %s_____" % path)

        if path == "/":
        # default
            print("SEARCH: client entered default search web")
            send_content = html.send_file(self, "search.html")

        elif path.find('searchDrug') != -1:
        # input = active_ingredient // output = drugs with such active_ingredient
            try:
                print("SEARCHED: client has attemped to make a request")
                active = path.split("=")[1].split("&")[0]
                limit = path.split("=")[2]
                print("REQUEST: Client asked for drugs with %s and especified a limit of %s" % (active, limit))
                json_list = client.search_drugs(active, limit) # getting Json data
                drugs_list = parser.parse_drugs(self, json_list) # getting a list of drugs
                send_content = html.create_html(self, drugs_list) # writing down list in an html file
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                send_content = html.send_file(self, "error.html")
        elif path.find('searchCompany') != -1:
        # input = manufacturer and a limit // output = drugs produced by such company
            try:
                print("SEARCHED: client has attemped to make a request")
                manufacter = path.split("=")[1].split("&")[0]
                limit = path.split("=")[2]
                print("REQUEST: Client asked for drugs produced by %s and especified a limit of %s" % (manufacter, limit))
                json_list = client.search_companies(manufacter, limit)
                drugs_list = parser.parse_companies(self, json_list)
                print(drugs_list)
                send_content = html.create_html(self, drugs_list)
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                send_content = html.send_file(self, "error.html")
        elif path.find('listDrugs') != -1:
        # input = limit // output = list of drugs
            try:
                print("SEARCHED: client has attemped to make a request")
                limit = path.split("=")[1].split("&")[0]
                print("Client asked for a drug list and specified a limit of %s" % (limit))
                json_list = client.list_drugs(limit)
                drugs_list = parser.parse_drugs(self, json_list)
                send_content = html.create_html(self, drugs_list)
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                send_content = html.send_file(self, "error.html")
        elif path.find('listCompanies') != -1:
        # input = limit // output = list of companies
            try:
                print("SEARCHED: client has attemped to make a request")
                limit = path.split("=")[1].split("&")[0]
                print("Client asked for a manufacturer list and especified a limit of %s" % (limit))
                json_list = client.list_drugs(limit)
                drugs_list = parser.parse_companies(self, json_list)
                send_content = html.create_html(self, drugs_list)
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                send_content = html.send_file(self, "error.html")
        elif path.find('listWarnings') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("SEARCHED: client has attemped to make a request")
                limit = path.split("=")[1].split("&")[0]
                print("Client asked for a warning list and especified a limit of %s" % (limit))
                json_list = client.list_drugs(limit)
                drugs_list = parser.parse_companies(self, json_list)
                send_content = html.create_html(self, drugs_list)
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                send_content = html.send_file(self, "error.html")
        else:
            if path != "/favicon.ico":
                print("* * ERROR * * : standard error: wrong path")
                send_content = html.send_file(self, "error.html")
        # Send message back to client
        if path != "/favicon.ico":
            self.wfile.write(bytes(send_content, "utf8"))
            print("SERVED: File has been sent!")


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at %s:%s" % (IP, PORT))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print("")
print("Server stopped!")

