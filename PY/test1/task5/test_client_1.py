import requests
import json


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "foobar",
        "params": {'foo':'nishi','bar':'shabi','hew':'aaa'},
        "jsonrpc": "2.0",
        "id": 3,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["result"]
    assert response["jsonrpc"]
    assert response["id"]
    d = {
        "method": "test_add",
        "params": [1,2,3,4,5],
        "jsonrpc": "2.0",
        "id": 0,
    }
    r = requests.post(url,data=json.dumps(d),headers=headers).json()
    return r

if __name__ == "__main__":
    response=main()
    print(response)