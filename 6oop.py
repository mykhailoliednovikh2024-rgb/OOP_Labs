


import requests

class Restclient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, params=None):
        if params is None:
            params = {}
        
        params["appid"] = self.api_key
        
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        return response.json() if response.ok else f"Error: {response.status_code}"

    def post(self, endpoint, data):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        return response.json() if response.ok else f"Error: {response.status_code}"

    def put(self, endpoint, data):
        response = requests.put(f"{self.base_url}/{endpoint}", json=data)
        return response.json() if response.ok else f"Error: {response.status_code}"

    def delete(self, endpoint):
        response = requests.delete(f"{self.base_url}/{endpoint}")
        return response.status_code

if __name__ == "__main__":
    url = "https://api.openweathermap.org/data/2.5"
    key = "5f9732a1f38fcdf6eb68671a1a8688ad"
    
    client = Restclient(url, key)
    
    weather_params = {
        "q": "Lviv",
        "units": "metric",
        "lang": "ua"
    }
    
    print(client.get("weather", params=weather_params)) 