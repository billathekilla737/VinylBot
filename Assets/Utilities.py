import regex as re
def Parse_Private():
    try:
        with open(r"Assets/Keys/Private.txt", "r") as tokenFile:
            lines = tokenFile.readlines()
        
        # Initialize a dictionary to hold the values
        values = {}
        for line in lines:
            # Skip lines that do not contain ' = '
            if ' = ' not in line:
                continue
            key, value = line.strip().split(' = ')
            values[key] = value.strip("'")
        
        # Extract token and URL from the dictionary
        token = values.get('Token')
        URL = values.get('URL')
        
        if token is None or URL is None:
            raise ValueError("Token or URL not found in file")
        
        return token, URL
    except Exception as e:
        print(f"Error reading file or parsing content: {e}")
        return None, None
    
def Parse_Reddit_Secrets():
        """
        Parse the API credentials from a given file.
    
        Args:
        - filepath (str): The path to the file containing the API credentials.
    
        Returns:
        - tuple: A tuple containing the client_id, client_secret, and user_agent.
        """
        credentials = {'client_id': None, 'client_secret': None, 'user_agent': None}
        with open(r'Assets/Keys/API_Private.txt', 'r') as file:
            for line in file:
                if line.startswith('client_id'):
                    credentials['client_id'] = line.split('=')[1].strip().strip("'")
                elif line.startswith('client_secret'):
                    credentials['client_secret'] = line.split('=')[1].strip().strip("'")
                elif line.startswith('user_agent'):
                    credentials['user_agent'] = line.split('=')[1].strip().strip("'")
        
        return credentials['client_id'], credentials['client_secret'], credentials['user_agent']


def get_api_key_from_file():
    api_key = None
    try:
        with open(r'Assets/Keys/OpenAI_Private.txt', 'r') as file:
            for line in file:
                if line.startswith('APIKEY'):
                    # Updated to strip whitespace and quotation marks from both ends
                    api_key = line.split('=')[1].strip(" \n\r'\"")
                    break  # Exits the loop once the API key is found
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return api_key

def preprocess_input(posts):
    titles = [f"- {post['title']}" for post in posts]
    return "\n".join(titles)

def convert_to_list(multi_line_string):
    return multi_line_string.split('\n')



def normalize_string(s):
    return re.sub(r'[^a-z0-9\s]', '', s.lower())
