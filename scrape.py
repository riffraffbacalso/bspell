from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_letters() -> str:
    url = "https://www.nytimes.com/puzzles/spelling-bee"
    class_name = "cell-letter"

    ops = webdriver.ChromeOptions()
    ops.add_argument("headless")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=ops
    )
    driver.get(url)
    els = driver.find_elements(By.CLASS_NAME, class_name)
    let_list = [str(el.get_property("textContent")) for el in els]
    return "".join(let_list)


if __name__ == "__main__":
    print(get_letters())
