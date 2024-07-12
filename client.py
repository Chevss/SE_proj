# client.py
import requests

server_url = 'http://192.168.86.8:5000/query'
# server_url = 'http://127.0.0.1:5000/query'

def send_query(query, params):
    try:
        response = requests.post(server_url, json={'query': query, 'params': params})
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return None