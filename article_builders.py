


from helpers.gpt_helpers import OpenAIHelper
from helpers.general_helpers import write_to_json, read_json, write_markdown_file
import json
import markdown
import requests



intent_message = "You are going to create blog posts, that are first and foremost informative for the user. Secondarily you will write them from the aspect of a quirky, but majorly honest or real wedding professional, who is well versed in all things wedding. You will write in a non-standard format to avoid being every other blog. We are writing blog posts to help those looking to get married or are already planning out their wedding."



def new_post_data(blog_title):

    with open('keys/openai.txt', 'r', encoding='utf-8') as file:
        api_key = file.read()

    bot = OpenAIHelper(api_key, intent_message)
    example = "{'common_questions':[an array of commonly asked questions], 'other_necessary_info:[array of strings as necessary data points.], 'creative_anecdotal_info':['array of strings that help illustrate the given points], 'topics':[array of topics]}" 
    prompt = 'Create the data necessary to complete this beginning outline'

    try:
        response = bot.gpt_json(prompt, blog_title, example)
        if response:
            write_to_json(response, filename='data/outputs/new_post_data.json')

    except:
        response = None
    

    return response


def create_post_outline(title):

    #this function assumes there is a new_post_data file and if not, it should immediately return nothing.
    data = read_json('data/outputs/new_post_data.json')
    #We want to then create the outline with gpt for this article with the article title

    if data:

        with open('keys/openai.txt', 'r', encoding='utf-8') as file:
            api_key = file.read()

        bot = OpenAIHelper(api_key, intent_message)
        prompt = 'Please create the blog post outline for the given data' 
        example = '{"article_outline": "a notably complete article outline as string"}'

        try:
            response = bot.gpt_json(prompt=prompt, example=example, data=str(data))
            write_to_json(response, filename='data/outputs/new_post_outline.json')
            if response:
                return response

            else:
                response = []
                return response

        except Exception as e:
            print(f'Failed to create an outline for this article data: {e}')



    else:
        return None
    ##take this post data and title and create the outline for our new blog post
    



def write_markdown(title):

    #requires new_post_data and new_post_outline, check this first

    try:
        data_load = read_json('data/outputs/new_post_data.json')
        data = json.dumps(data_load)
        outline_load = read_json('data/outputs/new_post_outline.json')
        outline = json.dumps(outline_load)


        with open('keys/openai.txt', 'r', encoding='utf-8') as file:
            api_key = file.read()
        bot = OpenAIHelper(api_key, intent_message)

        prompt = 'Write this entire blog post article, authored by Celia Milton (who has 25 years in the industry) as a markdown( .md ) file, considering the following data:[data as denoted]'
        example = '{"markdown": "markdown file as string text"}'
        composite_data = (data + outline)
        
        response = bot.gpt_json(prompt=prompt,example=example, data=composite_data)
        print('Markdown File: ' + str(response))

        if response:
            print(response['markdown'])
            markdown_data = response['markdown']
            with open('data/outputs/new_post_markdown.md', 'w', encoding='utf-8') as file:
                file.write(markdown_data)

            print(f"Content successfully written to new_post_markdown.md")
            return True
        
        else:
            return False

    except Exception as e:
        print(f'There was an error creating the Markdown file: {e}') 
        return False



def add_categories():

    #read in the article
    with open('data/outputs/new_post_markdown.md', 'r', encoding='utf-8') as file:
        content = file.read()

    with open('keys/openai.txt', 'r', encoding='utf-8') as file:
        api_key = file.read()
    bot = OpenAIHelper(api_key, intent_message)
    #feed gpt model to read and output necessary categories for our new blog_post

    categories_json = read_json('data/categories.json')
    categories = json.dumps(categories_json)

    prompt = "You will read the following article and attach the proper categories to label this blog post with. [You will be given the categories to choose from]" 
    example = {'categories: [array of categories ids as strings]'}
    data = f"[Blog Post]:{content}\n\n[categories]:{categories}"

    response = bot.gpt_json(prompt=prompt, example=example, data=data)

    if response:
        return response['categories']

    return None




def publish_blog(title, categories):
    # Step 1: Read your Markdown file
    with open('data/outputs/new_post_markdown.md', 'r') as file:
        markdown_content = file.read()

    # Step 2: Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Step 3: Define the image caption and HTML snippet
    image_caption = """
    [caption id="attachment_514" align="alignnone" width="1024"]
    <img src="https://images.unsplash.com/photo-1500900173725-e0978c945e23?crop=entropy&cs=srgb&fm=jpg&ixid=M3w2NDMwODN8MHwxfHNlYXJjaHwxfHx3ZWRkaW5nJTIwJTJCJTIwbG92ZXxlbnwwfDB8fHwxNzIzNjUyMjM1fDA&ixlib=rb-4.0.3&q=85" 
    alt="" width="1024" height="290" class="size-large wp-image-514" /> 
    A beautiful I love you sign represents love on the door
    [/caption]
    """

    # Step 4: Combine the image caption with the rest of the HTML content
    final_html_content = f"{image_caption}\n{html_content}"

    # Step 5: Define the WordPress API endpoint and credentials
    url = "https://njvowsnow.com/wp-json/wp/v2/posts"
    username = "Andrew Guasch"
    with open('keys/wordpress_key.txt', 'r', encoding='utf-8') as file:
        password = file.read()

     # Step 6: Create the post data payload
    post_data = {
        "title": title,
        "content": final_html_content,
        "status": "publish",  # Use 'draft' if you want to save it as a draft
        "categories": categories,  # Assuming categories is a list of category IDs
        "author": 3
    }

    # Step 7: Send the post request
    response = requests.post(url, json=post_data, auth=(username, password))

    # Step 8: Check the response
    if response.status_code == 201:
        print("Post successfully created on njvowsnow.com.")
    else:
        print(f"Failed to create post. Status code: {response.status_code}")
        print(response.json())




if __name__== "__main__":
    title = "How to Prioritize Your Wedding Budget: Where to Spend and Where to Save"


    try:
        data = new_post_data(title)  
        
        outline = create_post_outline(title)
        
        markdown_content = write_markdown(title)
        print(markdown_content)
        categories = add_categories()
        print(categories)

        publish_blog(title, categories)

        
    except Exception as e:
        print(f"There was no data to print: {e}")
    #