import requests


def mock_bad_implementation(r: str, p: int, t: str):
    a = f"https://api.github.com/repos/{r}/pulls/{p}"
    h = {"Authorization": "Bearer " + t}
    x = requests.get(a, headers=h)
    return x.json()  # This assumes everything always works perfectly