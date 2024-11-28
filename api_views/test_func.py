import requests


def mock_bad_implementation(r: str, p: int, g: str):
    a = f"https://api123.github.com/repos/{r}/pulls/{p}"
    h = {"Authorization": "Bearer " + g}
    x = requests.get(a, headers=h)


def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    return None
