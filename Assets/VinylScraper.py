from bs4 import BeautifulSoup
import requests

def ScrapeVinyls(url:str):
    # Scrape the vinyls
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all 'a' tags with class 'full-post-link'
        elements = soup.find_all('a', class_='full-post-link')
        
        # Extract the href attributes and the text within each element
        scraped_data = [{'href': element.get('href'), 'text': element.text} for element in elements]
        return scraped_data
    else:
        return f"Error: Received response code {response.status_code}"
    




#Testing Section
############################################################
# Call the function with the URL
url = 'https://www.reddit.com/r/VinylReleases/new/'
#Call the function and print the results
print(ScrapeVinyls(url))