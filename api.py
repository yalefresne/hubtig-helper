import requests


def get(url: str, header: dict):
    response = requests.get(url=url, headers=header)

    return response


def delete(url: str, header: dict):
    response = requests.delete(url=url, headers=header)

    return response
