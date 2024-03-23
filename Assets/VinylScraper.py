import praw
from Utilities import Parse_Reddit_Secrets
ViewedPostsFile = 'Assets/ViewedPosts.txt'
ViewedPosts = set()

try:
    with open(ViewedPostsFile, 'r') as f:
        ViewedPosts = set(f.read().splitlines())
except FileNotFoundError:
    print('Error: File not found.')

def get_recent_posts(amount):
    # Variable Initialization
    #####################################################################
    client_id, client_secret, user_agent = Parse_Reddit_Secrets()
    print(client_id, client_secret, user_agent)
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subreddit = reddit.subreddit('vinylreleases')
    posts = []

    for post in subreddit.new(limit=amount):  # 'limit' specifies how many posts to fetch
        #Check each line of to see if the postID is unique
        if post.id not in ViewedPosts:
            #If the postID is unique, add it to the list of posts
            posts.append({'title': post.title, 'url': post.url})
            #Add the postID to the list of viewed posts
            ViewedPosts.add(post.id)
            #Write the postID to the file
            with open(ViewedPostsFile, 'a') as f:
                f.write(post.id + '\n')

    return posts
