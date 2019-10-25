from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import os
import itertools

# change these if you want to scrape a different cse hw site
cse_url = "https://courses.cs.washington.edu/courses/cse143/19au/"
diff_site = "diff.html"

# get the html from a website
def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            return resp.content

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

# get the cse diff site webpage
webpage = simple_get(cse_url + diff_site).decode('utf-8')

# ok I shouldn't use regex to parse html, 
# but whatever this is easy, there's no way it'll break
webpage_no_comments = re.sub("(<!--.*?-->)", "", webpage, flags=re.DOTALL)

# look for the hw log links
soup = BeautifulSoup(webpage_no_comments, 'html.parser')
hw = soup.find(id="homework")
logGroups = soup.find_all('optgroup')

for logs in logGroups:
    # BeautifulSoup broke here :(
    # (thanks uw cse, for not having closing brackets for your <optgroup> tags)
    # so now we parse stuff manually
    
    title = logs['label']

    out_file_path = 'out_' + title + '.txt'
    inp_file_path = 'inp_' + title + '.txt'

    if(os.path.exists(out_file_path)):
        os.remove(out_file_path)

    if(os.path.exists(inp_file_path)):
        os.remove(inp_file_path)

    inp = open(inp_file_path, "a")
    out = open(out_file_path, "a")
    pretty = iter(logs.prettify().splitlines())

    for testCase in pretty:
        if("optgroup" in testCase and title not in testCase):
            break
        elif "optgroup" in testCase:
            continue
            
        # bleh more regex... basically this gets all stuff between quotes
        hwlink = "".join(re.findall(r'\"(.+?)\"', testCase))
        
        line = ""
        if(hwlink != ""):
            line = pretty.__next__()
        else:
            continue

        log = simple_get(cse_url + hwlink).decode('utf-8')

        # get text after '?'. Usually that's where input happens for these cse assignments.
        iterlog = iter(log.splitlines())
        inputs = [line]
        for line in iterlog:
            questionMark = line.rfind("?")
            if questionMark != -1:
                inputs.append(line[questionMark + 1:])

        inp.write(" ".join(inputs))
        inp.write("\n")
        out.write(log)

    inp.close()
    out.close()