import requests  
from bs4 import BeautifulSoup  
import json
from collections import deque
import argparse
  
BASE_URL = ''  
BASE_PATH = ''  
PATH_TO_SKIP = []  
LOG = False
  
def get_html(url):  
    try:  
        response = requests.get(url, timeout=2)  
        response.raise_for_status()  
        return response.text  
    except requests.RequestException:  
        return None  
  
  
def get_links(html, current_path):  
    soup = BeautifulSoup(html, 'html.parser')  
    links = []  
    for link in soup.find_all('a'):  
        l = link.get('href')  
        if l.startswith('?') or l in current_path or l in PATH_TO_SKIP:   
            continue  
        links.append(l)  
    return links  
  
  
def DFS(path, max_depth, current_depth=1):
    result = {"files": []}
    try:
        html = get_html(BASE_URL + path)  
        if html:  
            links = get_links(html, path) 
            for link in links:
                if LOG:
                    print("\t" * current_depth, link)
                if link.endswith("/"):
                    if current_depth <= max_depth:
                        result[link], r =  DFS(path + link, max_depth, current_depth + 1) 
                        if r:
                            return result, True
                        
                    else:
                        result[link] = None
                else:
                    result["files"].append(link)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully...")
        return result, True
    return result, False


def add_path(result, path, val):
    rs = path.split("/")
    for r in rs[1:-1]:
        result = result[r]
    result[val[:-1]] = {"files": []}


def add_file(result, path, val):
    rs = path.split("/")
    for r in rs[1:-1]:
        result = result[r]
    result["files"].append(val)


def BFS(path, max_depth):
    result = {BASE_PATH[1:-1] : {"files": []}}
    try:
        q = deque()
        q.append(path)
        current_depth = 0
        while q:
            path = q.popleft()
            new_depth = len(path.split("/")[1:-1])
            if current_depth != new_depth:
                current_depth = new_depth
                if LOG:
                    print(f"================ Current Depth {current_depth} ================")

            html = get_html(BASE_URL + path)  
            if html:
                links = get_links(html, path) 
                for link in links:
                    if link.endswith("/"):
                        add_path(result, path, link)
                        if  current_depth < max_depth:
                            q.append(path + link)
                    else:
                        add_file(result, path, link)
            if LOG:
                print(path, ": ")
                for l in links:
                    print("\t", l)
                print()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully...")
    finally:
        return result
    

def remove_empty_files(obj):
    if isinstance(obj, list):
        # Recursively clean each item in the list
        return [remove_empty_files(item) for item in obj if not (isinstance(item, dict) and 'files' in item and not item['files'])]
    elif isinstance(obj, dict):
        # Recursively clean each value in the dictionary
        return {k: remove_empty_files(v) for k, v in obj.items() if not (k == 'files' and not v)}
    return obj


def replace_empty_objects_with_none(obj):
    if isinstance(obj, list):
        # Recursively process each item in the list
        return [replace_empty_objects_with_none(item) for item in obj]
    elif isinstance(obj, dict):
        # Replace empty dictionaries with None, otherwise process each key-value pair
        if not obj:
            return None
        return {k: replace_empty_objects_with_none(v) for k, v in obj.items()}
    return obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('url', type=str, help='url to search')
    parser.add_argument('path', type=str, help='Base path to the apache directory')
    parser.add_argument('output_file', type=str, help='Path to the output file')
    parser.add_argument('search_type', type=str, choices=['BFS', 'DFS'], help='Type of search: BFS or DFS')
    parser.add_argument('max_depth', type=int, help='Maximum depth for the search')
    parser.add_argument('--log', action='store_true', help='Enable logging of the search process')
    
    args = parser.parse_args()
    
    BASE_URL = args.url
    BASE_PATH = args.path
    output_file = args.output_file
    search_type = args.search_type
    max_depth = args.max_depth
    LOG = args.log
    

    if search_type == "BFS":
        result = BFS(BASE_PATH, max_depth)
    elif search_type == "DFS":
        if LOG:
            print(BASE_PATH)
        result, r = DFS(BASE_PATH, max_depth)

    result = remove_empty_files(result)
    result = replace_empty_objects_with_none(result)

    with open(output_file, "w") as f:
        json.dump(result, f)