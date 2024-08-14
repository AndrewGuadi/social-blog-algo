import requests




# Function to fetch the first horizontally oriented image from Unsplash
def fetch_unsplash(keyword):

    with open('../keys/unsplash_key.txt', 'r', encoding='utf-8') as file:
        api_key = file.read()
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": keyword,
        "orientation": "landscape",  # Filter for horizontal (landscape) images
        "per_page": 1,  # Only return the first result
        "client_id": api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            # Get the first image from the results
            image_url = data["results"][0]["urls"]["full"]
            image_id = data["results"][0]["id"]
            return image_url, image_id
        else:
            print("No images found for the keyword.")
            return None, None
    else:
        print(f"Failed to fetch images: {response.status_code}")
        return None, None




if __name__=="__main__":

    url, image_id = fetch_unsplash('wedding + love')

    print(url, image_id)