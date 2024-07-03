import regex as re
from datetime import datetime, timedelta

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

#Maintancing 7/3/2024
############################################################################################################
def Store_Varation_Data(variation_data):
    # The goal of this function is to store the variation match data to a file. 
    #We will store the data as MM/DD/YYYY - Artist, This is Title
    #Will will not rewrite of previous lines only add to the file
    #Before storeing the data we will make sure that the data is not already in the file by checking the artist, This is Title part of the string
    current_date = datetime.now().strftime("%m/%d/%Y")
    with open("Assets/Variation_Data.txt", 'a+') as file:
        lines = file.readlines()

        for line in lines:
            print(f"Line: {line}")
            # Check if the data is already in the file
            if variation_data[11:] in line:
                print("Data already in file")
                break
            else:
                file.write(f"{current_date} - {variation_data}\n")
                print(f"Data added to file: {current_date} - {variation_data}")




def Read_Variation_Data():
    # The goal of this function is to read the variation data from a file
    # This file will be cross-referenced against new data to ensure that the data is not repeated more than three times
    try:
        with open(r"Assets/Variation_Data.txt", "r") as file:
            lines = file.readlines()
        
        # Strip newline characters and any leading/trailing whitespace
        cleaned_lines = [line.strip() for line in lines]
        
        return cleaned_lines
    except Exception as e:
        print(f"Error, This is likely due to the file not existing. If this is the first time running the program, this is normal. {e}")
        return []

def Remove_Variation_History(Keep_For):
    removed_lines = ""
    current_date = datetime.now()
    keep_duration = timedelta(days=Keep_For)  # Convert Keep_For to timedelta object
    
    # Open the file in write mode to overwrite existing content
    History = Read_Variation_Data()
    with open("Assets/Variation_Data.txt", 'w') as file:
        for search in History:
            entry_date = datetime.strptime(search[:10], "%m/%d/%Y")
            if entry_date > current_date - keep_duration:  # Use keep_duration instead of Keep_For
                file.write(f"{search}\n")
            else:
                removed_lines += f"{search}\n"

    return removed_lines

    

############################################################################################################
#Returns the History Title with no Date
def extract_titles(searches):
    return [search[11:].strip() for search in searches]

def preprocess_input(posts):
    titles = [f"- {post['title']}" for post in posts]
    return "\n".join(titles)

def convert_to_list(multi_line_string):
    return multi_line_string.split('\n')

def normalize_string(s):
    return re.sub(r'[^a-z0-9\s]', '', s.lower())
