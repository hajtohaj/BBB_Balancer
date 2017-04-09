from WebServiceClient import WebServiceClient

client = WebServiceClient()
client.establishConnection("TOMASZ", "GABRYS", "http://10.9.137.110:8001/")
print( "Client: {}".format(client.sendRequest("Pytam Cie")))
client.closeConnection()
