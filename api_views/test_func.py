import requests


def mock_bad_implementation(r: str, p: int, g: str):
    a = f"https://api123.github.com/repos/{r}/pulls/{p}"
    h = {"Authorization": "Bearer " + g}
    x = requests.get(a, headers=h)


def fetch_data_test_v1(api_url1):
    response = requests.get(api_url1)
    return response.text