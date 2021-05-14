from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests

def getUrl(url: str, headers={}, retry=5, timeout=10):
    retry_strategy = Retry(
        total=retry,
        backoff_factor=0.1
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    response = http.get(url, headers=headers, timeout=timeout)

    return response

if __name__ == "__main__":
    print(getUrl("https://example.com").text)