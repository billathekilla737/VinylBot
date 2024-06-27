# Discord Vinyl Bot

## Description

This is a Discord bot created to help users find particular songs and artists that appear in the titles of posts on the popular r/vinyl subreddit. The bot uses various API keys to function, including Reddit, OpenAI, and Discord tokens. This bot was made for use in my Discord server with my friends, so it may not be maintained perfectly at all times.

## Features

- **Search Posts**: The bot searches for vinyl album releases on r/vinyl and identifies unique releases by comparing the titles. This can adequately discern between similar printings that might be for the same album but different publishers/vinyl color.
- **Artist Matching**: Compares your list of liked artists with the titles of recent posts to find matches. The bot by default runs this matching every 30 minutes to find new posts. The frequency can be edited to your preference.
- **User Commands**: Allows users to add, remove, and list their liked artists. The list will be unique to each person and currently the artists added via discord command will be ethereal (not shown to other's in the channel).

## Requirements

To run this bot, you will need the following API keys. Later we will save them to 'VinylBot\Assets\Keys':
- Reddit API key : https://www.reddit.com/wiki/api/ 
- OpenAI API key (version <=28) https://openai.com/api/pricing/#language-models
- Discord token https://openai.com/api/pricing/#language-models

Naming Conventions for the API key files are listed below in step 3 of installation

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/vinyl-bot.git
    cd vinyl-bot
    ```

2. Install the required Python packages:

    ```bash
    pip install discord.py tabulate openai==0.27.2
    ```

3. To set up your API keys and tokens, create 3 separate .txt files in the 'VinylBot\Assets\Keys' directory with the following structure:

    **Reddit API Key:**
    - File Named: `API_Private.txt`
    - File Layout:
        ```plaintext
        client_id = 'YourId'
        client_secret = 'YourAPIKey'
        user_agent = 'YourUserAgent'
        ```

    **Open AI API Key:**
    - File Named: `OpenAI_Private.txt`
    - File Layout:
        ```plaintext
        APIKEY = 'YourAPIKey'
        ```

    **Discord API Key:**
    - File Named: `Private.txt`
    - File Layout:
        ```plaintext
        Token = YourToken
        URL = 'YourDiscordUrl'
        ```


4. Run the bot:

    ```bash
    python bot.py
    ```

## Usage

The bot offers several commands to interact with:

- `/addartist <artist>`: Add an artist to your liked artists list.
- `/removeartist <artist>`: Remove an artist from your liked artists list.
- `/listartists`: List all the artists you like.
- `/help`: Display the available commands and their descriptions.

## Code Overview

The main components of the bot are as follows:

### `run_discord_bot()`

The main function that initializes and runs the Discord bot. It sets up the client, command tree, and event loop for periodic subreddit checks.

### Slash Commands

- `addartist`: Adds an artist to the user's liked artists list.
- `removeartist`: Removes an artist from the user's liked artists list.
- `listartists`: Lists all the artists the user likes.
- `help`: Provides information about available commands.

### Helper Functions

- `Parse_Private()`: Parses the `private.json` file for API keys.
- `get_recent_posts(postSearchAmount)`: Retrieves recent posts from r/vinyl.
- `RemoveDuplicates()`, `convert_to_list()`, `SearchArtist()`: Interact with the OpenAI API to process and search posts.

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License.

---

Feel free to explore the code and contribute to the project. If you encounter any issues or have suggestions, please open an issue on GitHub. Enjoy. This bot was created for use with my friends and I. I decided to make it public
