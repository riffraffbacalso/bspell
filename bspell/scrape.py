from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.nytimes.com/puzzles/spelling-bee"
CLASS_NAME = "cell-letter"


def get_letters() -> str:
    ops = webdriver.ChromeOptions()
    ops.add_argument("headless")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=ops
    )
    driver.get(URL)
    els = driver.find_elements(By.CLASS_NAME, CLASS_NAME)
    letter_list = [str(el.get_property("textContent")) for el in els]
    return "".join(letter_list)


if __name__ == "__main__":
    print(get_letters())
