import requests


def main():
    response = requests.get("http://127.0.0.1:8000/items")
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    main()
