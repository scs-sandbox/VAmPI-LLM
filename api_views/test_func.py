import requests
import logging
from urllib.parse import urlparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def mock_bad_implementation(r: str, p: int, g: str):
    a = f"https://api123.github.com/repos/{r}/pulls/{p}"
    h = {"Authorization": "Bearer " + g}
    x = requests.get(a, headers=h)


def is_valid_url(url, max_length=2048):
    try:
        # Check the length of the URL
        if len(url) > max_length:
            return False

        # Parse the URL
        result = urlparse(url)

        # Validate scheme and netloc
        if not all([result.scheme, result.netloc]):
            return False

        return True
    except ValueError:
        logging.error(f"Invalid URL: {url}")
        return False


def fetch_data(api_url: str, timeout: int = 30):
    """
    Fetches data from the specified API URL.

    Parameters:
    api_url (str): The URL of the API endpoint to fetch data from.

    Returns:
    dict: A dictionary containing 'status' and 'data' keys:
          - 'status': 'success' if the request is successful, otherwise 'error'.
          - 'data': The response text if successful, or an error message if an error occurs.
    """

    if not api_url or not is_valid_url(api_url):
        return {'status': 'error', 'data': 'API URL is required'}

    try:
        response = requests.get(api_url, timeout=timeout)
        # Check for HTTP errors
        if response.status_code == 200:
            return {'status': 'success', 'data': response.text}
        else:
            # Log the HTTP error with status code
            logging.error(f"HTTP error occurred: {response.status_code} {response.reason}")
            return {'status': 'error', 'data': f"HTTP error {response.status_code}: {response.reason}"}
    except requests.exceptions.RequestException as err:
        # Log the general request exception
        logging.error(f"Error occurred: {err}")
        return {'status': 'error', 'data': str(err)}
