import requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4

url = "https://etc.usf.edu/lit2go/32/the-adventures-of-sherlock-holmes/345/adventure-1-a-scandal-in-bohemia/"
response = requests.get(url)

if response.status_code == 200:
    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Example: get all text from the page
    text = soup.get_text(separator="\n", strip=True)
    print(text[:1000])  # print first 1000 characters
else:
    print("Error:", response.status_code)
