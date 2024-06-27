from Assets.Utilities import *
import openai
import asyncpraw


openai.api_key = get_api_key_from_file()
ViewedPostsFile = 'Assets/ViewedPosts.txt'
ViewedPosts = set()

try:
    with open(ViewedPostsFile, 'r') as f:
        ViewedPosts = set(f.read().splitlines())
except FileNotFoundError:
    print('File not found. Creating A New One.')

async def get_recent_posts(amount):
    # Variable Initialization
    #####################################################################
    client_id, client_secret, user_agent = Parse_Reddit_Secrets()
    
    reddit = asyncpraw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    subreddit = await reddit.subreddit('vinylreleases')
    postList = []

    async for post in subreddit.new(limit=amount):  # 'limit' specifies how many posts to fetch
        # Check each line to see if the postID is unique
        if post.id not in ViewedPosts:
            # If the postID is unique, add it to the list of posts
            postList.append({'title': post.title, 'url': post.url})
            # Add the postID to the list of viewed posts
            ViewedPosts.add(post.id)
            # Write the postID to the file
            with open(ViewedPostsFile, 'a') as f:
                f.write(post.id + '\n')

    return postList


def RemoveDuplicates(posts, GPT_Prompt, model):
    # Preprocess the list into a string of titles
    #print('Posts:\n' + str(posts))
    preprocessed_titles = preprocess_input(posts)
    
    
    # Combine your task description with the preprocessed titles
    full_prompt = f"{GPT_Prompt}\n\nSubreddit Posts:\n{preprocessed_titles}\n\n Only Return Processed list as 'Processed List:'"
    # Call GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
        
    )
    return response.choices[0].message['content'].strip()


def SearchArtist(list1, list2, model, prompt):
    #Remove 'Processed List:' from the beginning of the string
    if str(list2).startswith('Processed List:'):
        list2 = str(list2)[15:]

    #print('Liked List:' + str(list1))
    #print('Reddit List:' + str(list2))
    # print('End of Lists')
    

    preprocessed_list1 = list1
    preprocessed_list2 = list2
    
    # Combine your task description with the preprocessed titles
    full_prompt = f"{prompt}\n\nList 1:\n{preprocessed_list1}\n\nList 2:\n{preprocessed_list2}\n\nMatches:"
    # Call GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
        
    )
    return response.choices[0].message['content'].strip()
