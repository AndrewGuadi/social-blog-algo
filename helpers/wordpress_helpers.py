
# home/helpers/wordpress_helpers.py

import requests

def get_categories():

    username = "Andrew Guasch"
    with open('/workspaces/social-blog-algo/keys/wordpress_key.txt', 'r', encoding='utf-8') as file:
        password = file.read().strip()

        url = "https://njvowsnow.com/wp-json/wp/v2/categories"
        categories = []
        page = 1

        while True:
            params = {
                "per_page": 10,  # Adjust per_page as needed
                "page": page
            }
            response = requests.get(url, params=params, auth=(username, password))

            if response.status_code == 200:
                data = response.json()
                if not data:  # If no data is returned, break the loop
                    break
                categories.extend(data)
                page += 1
            else:
                print(f"Failed to retrieve categories on page {page}. Status code: {response.status_code}")
                break

    return categories

