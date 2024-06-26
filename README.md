# Discord Vinyl Bot

## Description

This is a Discord bot created to help users find particular songs and artists that appear in the titles of posts on the popular r/vinyl subreddit. The bot uses various API keys to function, including Reddit, OpenAI, and Discord tokens. This bot was made for use in my Discord server with my friends, so it may not be maintained perfectly at all times.

## Features

- **Search Posts**: The bot searches for vinyl album releases on r/vinyl and identifies unique releases.
- **Artist Matching**: Compares the list of liked artists with the titles of recent posts to find matches.
- **User Commands**: Allows users to add, remove, and list their liked artists.

## Requirements

To run this bot, you will need the following API keys:
- Reddit API key
- OpenAI API key (version <=28)
- Discord token

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

3. Set up your API keys and tokens. Create a file named `private.json` in the `Assets` directory with the following structure:

    ```json
    {
      "reddit_api_key": "your_reddit_api_key",
      "openai_api_key": "your_openai_api_key",
      "discord_token": "your_discord_token"
    }
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
