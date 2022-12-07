import json

from bs4 import BeautifulSoup as BS
import httpx

URL = "https://www.nytimes.com/puzzles/spelling-bee"


def get_problem() -> str:
    res = httpx.get(URL, follow_redirects=True)
    soup = BS(res.text, "html.parser")
    js = soup.find_all("script")[2].string
    obj_str = js[18:]
    obj = json.loads(obj_str)
    return "".join(obj["today"]["validLetters"])
