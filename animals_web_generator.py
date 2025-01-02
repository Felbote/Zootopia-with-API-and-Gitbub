import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")

def fetch_data(animal_name):
    """
    Fetches the animal data for the given animal name.
    Returns a list of animals or an error message if no animals are found.
    """
    url = f"https://api.api-ninjas.com/v1/animals?name={animal_name}"
    headers = {"X-Api-Key": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        data = response.json()

        # If data is empty, return an empty list
        return data if data else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    except ValueError:
        print("Error decoding the API response.")
        return None


def generate_html(animal_name, animals_data):
    """
    Generates an HTML page for the provided animal data.
    """
    if not animals_data:
        return f"<h2>The animal \"{animal_name}\" doesn't exist.</h2>"

    html_content = f"<h1>Animals related to {animal_name}</h1>"
    for animal in animals_data:
        html_content += f"<h2>{animal.get('name', 'Unknown')}</h2>"
        html_content += f"<p>Location(s): {', '.join(animal.get('locations', []))}</p>"
        
        characteristics = animal.get('characteristics', {})
        characteristics_list = "".join(
            f"<li>{key}: {value}</li>" for key, value in characteristics.items()
        )
        html_content += f"<ul>{characteristics_list}</ul>"

    return html_content


def main():
    animal_name = input("Enter an animal name: ").strip()
    animals_data = fetch_data(animal_name)

    if animals_data is not None:
        html = generate_html(animal_name, animals_data)
        with open("animals.html", "w") as f:
            f.write(html)
        print("Website was successfully generated to the file animals.html.")
    else:
        print("Error fetching animal data.")


if __name__ == "__main__":
    main()