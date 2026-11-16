import urllib.request
import json
import time

def test_api(cmd):
    t0 = time.perf_counter()
    req = urllib.request.Request(
        'http://127.0.0.1:8765/api/command',
        data=json.dumps({'command': cmd}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    t1 = time.perf_counter()
    print(f'API "{cmd}" took: {(t1 - t0)*1000:.2f} ms | Reply: {data["reply"]}')

if __name__ == "__main__":
    for c in ["open Spotify", "close Spotify", "open it again", "what is 500 times 8", "akar dari 144"]:
        test_api(c)

