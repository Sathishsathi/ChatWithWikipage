import requests
import wikitextparser as wtp  

def fetch_wikipedia_page_content(page_name):
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "prop": "revisions",
            "titles": page_name,
            "rvprop": "content",
            "format": "json"
        }
    
        response = requests.get(url, params=params)
        # print(response.url)
        data = response.json()
        
        page = next(iter(data["query"]["pages"].values()))
        content = page["revisions"][0]["*"] if "revisions" in page else "Page not found"
        return content
    
    except requests.RequestException as e:
        return "page content can not be fetched"
    


def convert_to_plain_text(wikitext_content):
    try:
        parsed = wtp.parse(wikitext_content)
        plain_text = parsed.plain_text()
        return plain_text
    except Exception as e:
        print(f"not able to convert in plain text: {e}")
        return "not able to convert in plain text"



def wiki_page_answer(page_name:str):
    wikitext_content = fetch_wikipedia_page_content(page_name)
    plain_text_content = convert_to_plain_text(wikitext_content)
    return plain_text_content.strip()

# print(wiki_page_answer("Viluppuram"))