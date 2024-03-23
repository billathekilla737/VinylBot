def Parse_Private():
    try:
        with open("Assets/Keys/Private.txt", "r") as tokenFile:
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
        with open('Assets/Keys/API_Private.txt', 'r') as file:
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
        with open('Assets/Keys/OpenAI_Priavate.txt', 'r') as file:
            for line in file:
                if line.startswith('APIKEY'):
                    api_key = line.split('=')[1].strip()  # Splits the string and trims whitespace
                    break  # Exits the loop once the API key is found
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return api_key

# Example usage
file_path = 'path/to/your/file.txt'
api_key = get_api_key_from_file()
print(api_key)
