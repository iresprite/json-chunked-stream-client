import requests
import bytestreamhandler
import argparse


def client(url=None, obj_count=float("inf")):
    if url is None:
        url = "http://localhost:8020"
    r = requests.get(url, stream=True)
    buffer = ''
    handler = bytestreamhandler.ByteStreamHandler(bytestreamhandler.EmptyState())
    json_objects_parsed = 0
    for line in r.iter_lines():
        for c, byte_char in enumerate(line):
            handler.next_byte(byte_char)
            buffer += chr(byte_char)
            if handler.complete_object():
                json_objects_parsed += 1
                print(buffer + '\n')
                buffer = ''
        if json_objects_parsed >= obj_count:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="The server and port to connect to, e.g. http://localhost:8020", type=str)
    parser.add_argument("--objcount", help="The number of objects to consume; default is infinity", type=int)
    args = parser.parse_args()
    client(args.server, args.objcount)