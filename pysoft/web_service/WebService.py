#author: tomasz.gabrys@nokia.com
import json
import sys
import random
import string
import bottle


class BepfFileHandler:

    DEFAULT_FILE = 'data.txt'

    def __init__(self, file_name=None):
        self.file_name = self.DEFAULT_FILE
        if file_name is not None:
            self.file_name = file_name

    def read(self, first_line, chunk_size=0):
        data = []
        with open(self.file_name, 'r') as f:
            for i, line in enumerate(f):
                a = i
                if i < first_line:
                    continue
                if chunk_size and i >= first_line + chunk_size:
                    a -= 1
                    break
                data.append(line)
        a += 1
        return ''.join(data), a - first_line

    def count_all_records(self):
        with open(self.file_name) as f:
            for i, l in enumerate(f):
                pass
        return i + 1


class BepfBuildResponseString:

    RESPONSE_TEMPLATE = '{"response": {"status": "", "parameters": {}}}'
    STATUS_SUCCESS = 'OK'
    STATUS_FAILURE = 'FAILED'

    def create_cursor(self, cursor_id):
        my_resp = json.loads(self.RESPONSE_TEMPLATE)
        my_resp['response']['parameters']['cursor_id'] = cursor_id
        my_resp['response']['status'] = self.STATUS_SUCCESS
        return json.dumps(my_resp)

    def close_cursor(self):
        my_resp = json.loads(self.RESPONSE_TEMPLATE)
        my_resp['response']['status'] = self.STATUS_SUCCESS
        return json.dumps(my_resp)

    def read(self, records, records_count):
        my_resp = json.loads(self.RESPONSE_TEMPLATE)
        my_resp['response']['parameters']['records'] = records
        my_resp['response']['parameters']['records_count'] = records_count
        my_resp['response']['status'] = self.STATUS_SUCCESS
        return json.dumps(my_resp)

    def count_all_records(self, records_count):
        my_resp = json.loads(self.RESPONSE_TEMPLATE)
        my_resp['response']['parameters']['count_all_records'] = records_count
        my_resp['response']['status'] = self.STATUS_SUCCESS
        return json.dumps(my_resp)

    def operation_failed(self, reason):
        my_resp = json.loads(self.RESPONSE_TEMPLATE)
        my_resp['response']['status'] = self.STATUS_FAILURE
        my_resp['response']['parameters']['reason'] = reason
        return json.dumps(my_resp)


class BepfServeRequest:

    CURSOR_ID_SIZE = 10

    def __init__(self):
        self.cursors = {}
        self.response_builder = BepfBuildResponseString()
        self.file_handler = BepfFileHandler()

    def create_cursor(self, chunk_size, zero_offset):
        cursor_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(self.CURSOR_ID_SIZE))
        position = 0
        if not zero_offset:
            position = self.file_handler.count_all_records()
        self.cursors[cursor_id] = {'chunk_size': chunk_size, 'position': position}
        return self.response_builder.create_cursor(cursor_id)

    def close_cursor(self, cursor_id):
        if cursor_id in self.cursors:
            self.cursors.pop(cursor_id)
            return self.response_builder.close_cursor()
        return self.response_builder.operation_failed("Cursor {0} not found".format(cursor_id))

    def read(self, cursor_id):
        if cursor_id in self.cursors:
            chunk_size = self.cursors[cursor_id]['chunk_size']
            start_position = self.cursors[cursor_id]['position']
            data, number_of_records = self.file_handler.read(start_position, chunk_size)
            self.cursors[cursor_id]['position'] += number_of_records
            return self.response_builder.read(data, number_of_records)
        return self.response_builder.operation_failed("Cursor {0} not found".format(cursor_id))

    def count_all_records(self):
        number_of_records = self.file_handler.count_all_records()
        return self.response_builder.count_all_records(number_of_records)

    def read_all(self):
        chunk_size = 0
        start_position = 0
        data, number_of_records = self.file_handler.read(start_position, chunk_size)
        return data

    def request_processor(self, request):
        my_req = json.loads(request)
        req_name = my_req['request']['name']
        if req_name == 'create_cursor':
            return self.create_cursor(my_req['request']['parameters']['chunk_size'],
                                      my_req['request']['parameters']['zero_offset'])
        elif req_name == 'close_cursor':
            return self.close_cursor(my_req['request']['parameters']['cursor_id'])
        elif req_name == 'read':
            return self.read(my_req['request']['parameters']['cursor_id'])
        elif req_name == 'count_all_records':
            return self.count_all_records()
        else:
            return self.response_builder.operation_failed("Request not implemented".format(req_name))

app = BepfServeRequest()


@bottle.post('/bepf/data')
def index():
    request = str(bottle.request.body.getvalue(), 'utf-8')
    response = app.request_processor(request)
    return response


@bottle.get('/bepf/data')
def index2():
    response = app.read_all()
    return response

if __name__ == "__main__":

    if len(sys.argv) == 1:
        host = "127.0.0.1"
        port = 8001
    elif len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        print("Usage: WebService.py")
        print("Usage: WebService.py 192.168.0.6 8001")
        sys.exit(1)

    bottle.run(host=host, port=port)
