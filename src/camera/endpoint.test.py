import requests, time

while True:
    res = requests.get("http://127.0.0.1:5001/get_color")
    color = res.json()["color"]
    print(color)
    time.sleep(1)
