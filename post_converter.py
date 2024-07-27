import requests
from bs4 import BeautifulSoup
import sys


def get_html(url: str):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    real_url = f"http://blog.naver.com{soup.find(id="mainFrame")["src"]}"

    req = requests.get(real_url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
      
    return soup

def extract_text(soup: BeautifulSoup):
    p_list = soup.find_all("p", {"class": ["se-text-paragraph", "se-text-paragraph-align-"]})
    
    text_list = []
    for p in p_list:
        for span in p.find_all("span"):
            text = span.text
            if text != "\u200b" and text != " ":
                text = text.rstrip()
                style = span["style"]
                if style != "":
                    text = f"<span style=\"{style}\">" + text + "</span>"
                text_list.append(text)
                text_list.append("&nbsp;")
                text_list.append("")
    return text_list


def main(argv):
    target_url = argv[1]
    # target_url = "https://blog.naver.com/camomileclinic/223083926819"
    soup = get_html(target_url)
    text_list = extract_text(soup)
    with open("output.txt", "w") as f:
         f.write('\n'.join(text_list))



if __name__ == "__main__":
    argv = sys.argv
    main(argv)
