import http.server
import socketserver
import http.client
import json

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

        def send_file(file_name): # call to enter a filename to be opened
            with open(file_name) as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        def drug_warning(limit):
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("fda_info_tobesent.html", "w"):
                self.wfile.write(bytes('<html><head><h1>Search OpenFDA Application</h1><body style="background-color: yellow" >\n<marquee><h3>listWarnings: You searched for %s warnings</h3></marquee><ol>' % (limit), "utf8"))

            for i in range(len(repos['results'])):
                    try:
                        for n in range(len(repos['results'][i]["openfda"]["brand_name"])):
                            try:
                                warning = "<li>" + "warning of "+ repos['results'][i]["openfda"]["brand_name"][0] + ":     " + repos['results'][i]["warnings"][0] + "</li>"
                                self.wfile.write(bytes(warning, "utf8"))
                            except KeyError:
                                warning = "<li>" + "NOT FOUND" + "</li>"
                                self.wfile.write(bytes(warning, "utf8"))
                                break
                    except KeyError:
                        warning = "<li>" + "warning : " + "NOT FOUND" + "</li>"
                        self.wfile.write(bytes(warning, "utf8"))
                        continue
            self.wfile.write(bytes('</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Sad"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' % (IP, PORT), "utf8"))

        def active_fda(active, limit): # called to search for a drug and a limit

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=active_ingredient:%s&limit=%s" % (active, limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("fda_info_tobesent.html", "w"):
                self.wfile.write(bytes('<html><head><h1>Search OpenFDA Application</h1><marquee><h3>Active Ingredient: You searched for %s. Here you have %s matches:</h3></marquee><body style="background-color: yellow" >\n<ol>' % (active, limit), "utf8"))

                for i in range(len(repos['results'])):
                    try:
                        for n in range(len(repos['results'][i]["openfda"]["brand_name"])):
                            try:
                                drug = "<li>"+ "brand name is: " + repos['results'][i]["openfda"]["brand_name"][0] + "</li>"
                                self.wfile.write(bytes(drug, "utf8"))
                            except KeyError:
                                break
                    except KeyError:
                        drug = "<li>" + "brand name is: " + "NOT FOUND" + "</li>"
                        self.wfile.write(bytes(drug, "utf8"))
                        continue
                self.wfile.write(bytes('</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Sad"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' % (IP, PORT), "utf8"))

        def manufacturer_fda(manufacturer, limit):  # searches for manufacturer_name / returns brand_name

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=openfda.manufacturer_name:%s&limit=%s" % (manufacturer, limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("fda_info_tobesent.html", "w"):
                self.wfile.write(bytes('<html><head><h1>Search OpenFDA Application</h1><marquee><h3>Company: You searched for %s drugs produced by %s</h3></marquee><body style="background-color: yellow" >\n<ol>' % (limit, manufacturer), "utf8"))

                for i in range(len(repos['results'])):
                    try:
                        for n in range(len(repos['results'][i]["openfda"]["brand_name"])):
                            try:
                                manufacturer = "<li>"+ "brand name is: " + repos['results'][i]["openfda"]["brand_name"][0] + "</li>"
                                self.wfile.write(bytes(manufacturer, "utf8"))
                            except KeyError:
                                break
                    except KeyError:
                        manufacturer = "<li>" + "brand name is: " + "NOT FOUND" + "</li>"
                        self.wfile.write(bytes(manufacturer, "utf8"))
                        continue
                self.wfile.write(bytes('</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Sad"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' % (IP, PORT), "utf8"))

        def drugs_fda(limit):  # returns a drug list

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("fda_info_tobesent.html", "w"):
                self.wfile.write(bytes('<html><head><h1>Search OpenFDA Application</h1><marquee><h3>listDrug: You searched for %s drugs</h3></marquee><body style="background-color: yellow" >\n<ol>' % (limit), "utf8"))

                for i in range(len(repos['results'])):
                    try:
                        for n in range(len(repos['results'][i]["openfda"]["brand_name"])):
                            try:
                                drug = "<li>"+ "brand name is: " + repos['results'][i]["openfda"]["brand_name"][0] + "</li>"
                                self.wfile.write(bytes(drug, "utf8"))
                            except KeyError:
                                break
                    except KeyError:
                        drug = "<li>" + "brand name is: " + 'NOT FOUND' + "</li>"
                        self.wfile.write(bytes(drug, "utf8"))
                        continue
                self.wfile.write(bytes('</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Sad"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' % (IP, PORT), "utf8"))


        def manufacturers_fda(limit):  # returns a company list

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("fda_info_tobesent.html", "w"):
                self.wfile.write(bytes('<html><head><h1>Search OpenFDA Application</h1><marquee><h3>listCompanies: You searched %s companies</h3></marquee><body style="background-color: yellow" >\n<ol>' % (limit), "utf8"))

                for i in range(len(repos['results'])):
                    try:
                        for n in range(len(repos['results'][i]["openfda"]["manufacturer_name"])):
                            try:
                                manufacturer = "<li>"+ "brand name is: " + repos['results'][i]["openfda"]["brand_name"][0] + "</li>"
                                self.wfile.write(bytes(manufacturer, "utf8"))
                            except KeyError:
                                break
                    except KeyError:
                        manufacturer = "<li>" + "brand name is: " + "NOT FOUND" + "</li>"
                        self.wfile.write(bytes(manufacturer, "utf8"))
                        continue
                self.wfile.write(bytes('</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Sad"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' % (IP, PORT), "utf8"))

        path = self.path

        if path != "/favicon.ico":
            print("PATH: path introduced by client:", path)

        if path == "/":
            print("SEARCH: client entered default search web")
            filename = "search.html"

        elif path.find('searchDrug') != -1:  # let´s try to find a drug and a limit entered by user
            try:
                print("SEARCHED: client has attemped to make a request")
                active = path.split("=")[1].split("&")[0]  # drug entered by client
                limit = path.split("=")[2]  # limit entered by client
                print("REQUEST: Client asked for drugs with %s and especified a limit of %s" % (active, limit))
                active_fda(active, limit)
                print("SUCCESS: Client has succesfully made a request")
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                filename = "error.html"
        elif path.find('searchCompany') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("SEARCHED: Client searched for a manufacturer")  # this a check point
                manufacter = path.split("=")[1].split("&")[0] # drug entered by client
                limit = path.split("=")[2]  # limit entered by client
                print("REQUEST: Client asked for drugs produced by %s and especified a limit of %s" % (manufacter, limit))
                manufacturer_fda(manufacter, limit)
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                filename = "error.html"
        elif path.find('listDrugs') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("Client searched for a list of drugs")  # this a check point
                limit = path.split("=")[1].split("&")[0]  # limit entered by client
                print("Client asked for a drug list and especified a limit of %s" % (limit))
                drugs_fda(limit)
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("***** some ERROR occurred")
                filename = "error.html"
        elif path.find('listCompanies') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("Client searched for a list of manufacturers")  # this a check point
                limit = path.split("=")[1].split("&")[0]  # limit entered by client
                print("Client asked for a manufacturer list and especified a limit of %s" % (limit))
                manufacturers_fda(limit)
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("***** some ERROR occurred")
                filename = "error.html"
        elif path.find('listWarnings') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("Client searched for a list of warnings")  # this a check point
                limit = path.split("=")[1].split("&")[0]  # limit entered by client
                print("Client asked for a warning list and especified a limit of %s" % (limit))
                drug_warning(limit)
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("***** some ERROR occurred")
                filename = "error.html"

        else:
            if path != "/favicon.ico":
                print("***** ERROR: standard error")
            filename = "error.html"
            # Send message back to client

        if path != "/favicon.ico":
            send_file(filename)
            print("SERVED: File <<%s>> has been sent!" % filename)
            return


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

