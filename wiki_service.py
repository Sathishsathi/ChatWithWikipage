import wikipedia

def get_page_content(page_title):
	page_content = wikipedia.page(page_title).content
	return page_content

