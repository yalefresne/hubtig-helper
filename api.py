import requests


def get(url: str, header: dict):
    response = requests.get(url=url, headers=header)

    if response.ok:
        return response.json()

    return response


def delete(url: str, header: dict):
    response = requests.delete(url=url, headers=header)

    return response
