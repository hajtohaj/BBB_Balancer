#author: tomasz.gabrys@nokia.com
import http.client
import re
import json

class WebServiceClient:
    URI_PATTERN = re.compile('(http|https)://(.*?)(:[0-9]*)*(/.*)')
    
    def __init__(self):
        pass
    
    def establishConnection (self, user, password, uri):
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


class BepfBuildRequestString:

    REQUEST_TEMPLATE = '{"request": {"name": "", "parameters": {}}}'

    def create_cursor(self, chunk_size=0, zero_offset=0):
        my_req = json.loads(self.REQUEST_TEMPLATE)
        my_req['request']['name'] = "create_cursor"
        my_req['request']['parameters']['chunk_size'] = chunk_size
        my_req['request']['parameters']['zero_offset'] = zero_offset
        return json.dumps(my_req)

    def close_cursor(self, cursor_id):
        my_req = json.loads(self.REQUEST_TEMPLATE)
        my_req['request']['name'] = "close_cursor"
        my_req['request']['parameters']['cursor_id'] = cursor_id
        return json.dumps(my_req)

    def read(self, cursor_id):
        my_req = json.loads(self.REQUEST_TEMPLATE)
        my_req['request']['name'] = "read"
        my_req['request']['parameters']['cursor_id'] = cursor_id
        return json.dumps(my_req)

    def count_all_records(self):
        my_req = json.loads(self.REQUEST_TEMPLATE)
        my_req['request']['name'] = "count_all_records"
        return json.dumps(my_req)

if __name__ == "__main__":

    # # uri = 'http://192.168.0.6:8001/bepf/data'
    # uri = 'http://127.0.0.1:8001/bepf/data'
    #
    # https_client = WebServiceClient()
    # https_client.establishConnection("", "", uri)
    # web_service_request = BepfBuildRequestString()
    #
    # request = web_service_request.create_cursor(0,1)
    # print("Request: {0}".format(request))
    # response = https_client.sendRequest(request)
    # print("Response: {0}".format(response))
    # response = json.loads(str(response, 'utf-8'))
    # status = response['response']['status']
    # cursor = response['response']['parameters']['cursor_id']
    #
    # request = web_service_request.read(cursor)
    # print("Request: {0}".format(request))
    #
    # response = https_client.sendRequest(request)
    # print("Response: {0}".format(response))
    #
    # request = web_service_request.close_cursor(cursor)
    # response = https_client.sendRequest(request)

    a = BepfBuildRequestString()
    print(a.close_cursor('AJFDJ567JHKKHF'))
