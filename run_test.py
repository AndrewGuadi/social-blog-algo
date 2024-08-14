



import requests
import markdown



def publish_blog(title, categories)
    # Step 1: Read your Markdown file
    with open('post.md', 'r') as file:
        markdown_content = file.read()

    # Step 2: Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Step 3: Define the WordPress API endpoint and credentials
    url = "https://njvowsnow.com/wp-json/wp/v2/posts"
    username = "Andrew Guasch"
    with open('wordpress_key.txt', 'r', encoding='utf-8') as file:
        password = file.read()

    # Step 4: Create the post data payload
    post_data = {
        "title": title,
        "content": html_content,
        "status": "publish"  # Use 'draft' if you want to save it as a draft
    }

    # Step 5: Send the post request
    response = requests.post(url, json=post_data, auth=(username, password))

    # Step 6: Check the response
    if response.status_code == 201:
        print("Post successfully created on njvowsnow.com.")
    else:
        print(f"Failed to create post. Status code: {response.status_code}")
        print(response.json())



#first we want to create the daily list of titles and categories for the blog post content

# second we want to take the daily data and have the blog post written in an SEO optimized manner, pulling from a longer range of keywords as well

# third we want to have the body content written, the title and other text based information,and format it

#forth we want select an appropriate image for the article.

#we want to make sure this is all prepared for the wordpress template and create a new blog post with said data.

#we then want to make sure that this data is then shared with facebook and instagram, as well as added to google search console
