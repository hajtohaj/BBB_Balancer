#author: tomasz.gabrys@nokia.com
import base64, http.client
import re
import json

#example URI: https://clab299lbwas.netact.nsn-rdnet.net:443/netact/cm/oes/CMAdvanceResolver


class WebServiceClient:
    URI_PATTERN = re.compile('(http|https)://(.*?)(:[0-9]*)*(/.*)')
    
    def __init__(self):
        pass
    
    def establishConnection (self,user,password,uri):
        self.user = user
        self.password = password
        self.protocol = self.__extractProtocol(uri)
        self.address = self.__extractAddress(uri)
        self.port = self.__extractPort(uri)
        self.endpoint = self.__extractEndpoint(uri)
        return self.__connect()

    def sendRequest (self, request=''):
        base64string ='{0}:{1}'.format(self.user, self.password).replace('\n', '')
        headers={'Authorization': 'Basic '+ base64string}
        self.connection.request('POST', self.endpoint, request, headers)
        responseObject = self.connection.getresponse()
        self.connectionstate = vars(responseObject)
        return (responseObject.read())

    def closeConnection(self):
        return self.connection.close()

    def getConnectionState(self):
        return self.connectionstate

    def __extractProtocol(self,uri):
        return re.search(self.URI_PATTERN,uri).group(1)
        
    def __extractAddress(self,uri):
        return re.search(self.URI_PATTERN,uri).group(2)

    def __extractPort(self,uri):
        if not re.search(self.URI_PATTERN,uri).group(3):
            if self.protocol.upper() == 'HTTP' :
                return str(http.client.HTTP_PORT)
            elif self.protocol.upper() == 'HTTPS':
                return str(http.client.HTTPS_PORT)
            else: print('WebService Port can\'t be determined')
        return re.search(self.URI_PATTERN,uri).group(3)[1:]

    def __extractEndpoint(self,uri):
        return re.search(self.URI_PATTERN,uri).group(4)
    
    def __connect(self):
        if self.protocol.upper() == 'HTTP':
                self.connection = (http.client.HTTPConnection(self.address+':'+self.port))
                return self.connection
        elif self.protocol.upper() == 'HTTPS':
                self.connection = (http.client.HTTPSConnection(self.address+':'+self.port))
                return self.connection
        else: 
            assert False, 'Unknown protocol: %s' % self.protocol

if __name__ == "__main__":

    uri = 'http://127.0.0.1:8001/aaa'
    username = 'Tomasz'
    password = 'Pass'

    https_client = WebServiceClient()
    https_client.establishConnection(username, password, uri)
    request = {"request": "get_data"}
    request_s = json.dumps(request)
    print("Request: {0}".format(request_s))
    response = https_client.sendRequest(request_s)
    print("Response: {0}".format(response))