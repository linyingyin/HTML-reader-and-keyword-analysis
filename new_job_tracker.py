### Automated New Job Tracker ###

## This code will: ##
#   1. Automatically check user-defined job sites
#          - meant for the career page of companies, not job sites like Indeer or LinkedIn
#   2. Check the text for user-defined key phrases
#   3. Return a report

## Updated: ##
#   11/18/2026 - started file

## Side note: this file is commented tf out because I'm learning HTML parsing and web scraping as I go. Using this as a way to teach myself something new. :)

# ############################################ #

### Libraries
 # Run these lines in terminal to install libraries if you don't have them already #
# py -m pip install beautifulsoup4


import html
from urllib.request import urlopen  # request info from websites
from bs4 import BeautifulSoup       # HTML information parsing


### Functions

## Extract webpage text
    # works with .icms
def extract_text_icms(url):
    html = urlopen(url).read()  #open the url and read the html
    
    soup = BeautifulSoup(html, features="html.parser") #read html using html.parser

    for script in soup(["script", "style"]): #remove "script" and "style" elements from HTML
        script.extract()

    text = soup.get_text() #extract text from HTML (the chars between the <> tags)

    lines = (line.strip() for line in text.splitlines()) #split text by the line breaks, remove whitespace at each end of the string, then store the results in a generator object called lines.

    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) #split string by double spaces and call it "phrase", do it for each line in lines, then remove whitspace at each end of the results, then store the results in a generator object called chunks.

    text = '\n'.join(chunk for chunk in chunks if chunk) #join chunks together with a line break between each chunk, and remove any empty chunks.

    return text #output of the function.


def extract_text_phenompeople(url):
    html = urlopen(url).read()

    html_text = html.decode("utf-8", errors="replace")

    soup = BeautifulSoup(html, features="html.parser")

    # Locate the embedded job data
    for script in soup.find_all("script"):
        script_text = script.get_text()

        if "eagerLoadRefineSearch" in script_text:
            print("Found the job data!")
            print(script_text.find("eagerLoadRefineSearch"))

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    # Clean up extracted text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


urls = ["https://jobs.thecignagroup.com/us/en/search-results?s=1&in_iframe=1"]


# urls = [ 
#     "https://staff-emory.icims.com/jobs/search?ss=1&searchKeyword=statistician&searchRelation=keyword_all", 
#     "https://staff-emory.icims.com/jobs/search?ss=1&searchKeyword=data&searchRelation=keyword_all"
#     ]



# Results storage list
results = []

# URL processing
for url in urls:
    webpage_text = extract_text_phenompeople(url)

    results.append([url, webpage_text])

# # Display results
# for result in results:
#     print("URL:", result[0])
#     print("Text:", result[1][:500])
#     print("-------------------------")