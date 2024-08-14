

from helpers.wordpress_helpers import get_categories
from helpers.general_helpers import write_to_json
import time


#get tags from wordpress so we can associate the correct data for the blog

if __name__=="__main__":
    categories = get_categories()

    category_data = []
    for category in categories:

        new_data = {
            'id': category['id'],
            'name': category['name']
        }
        category_data.append(new_data)


    write_to_json(category_data)
#store this as a piece of data



