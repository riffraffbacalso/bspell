import json

from bs4 import BeautifulSoup as BS
import httpx

from retry_msg import retry_msg

URL = "https://www.nytimes.com/puzzles/spelling-bee"


def get_problem() -> tuple[str, list[str]]:
    @retry_msg("persistent network error when requesting today's puzzle")
    def request_page() -> httpx.Response:
        return httpx.get(URL, follow_redirects=True)

    res = request_page()
    soup = BS(res.text, "html.parser")
    js = soup.find_all("script")[3].string
    obj_str = js[18:]
    obj = json.loads(obj_str)
    problem = "".join(obj["today"]["validLetters"])
    answers = obj["today"]["answers"]
    return problem, answers
