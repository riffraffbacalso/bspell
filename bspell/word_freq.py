from concurrent.futures import ThreadPoolExecutor
from retry_msg import retry_msg
import httpx

URL = "https://api.datamuse.com/words"


def get_freqs(words: list[str]) -> dict[str, float]:
    with httpx.Client(http2=True) as client:

        @retry_msg("persistent network error when retrieving word frequencies")
        def request(word: str) -> httpx.Response:
            return client.get(f"{URL}?sp={word}&md=f&max=1")

        def extract(res: httpx.Response, word: str) -> float:
            if not (obj_list := res.json()):
                return 0
            else:
                obj = obj_list[0]
            return float(obj["tags"][0][2:]) if obj["word"] == word else 0

        with ThreadPoolExecutor(max_workers=50) as pool:
            freqs = [
                extract(res, word) for res, word in zip(pool.map(request, words), words)
            ]

    return dict(zip(words, freqs))


def sort_by_freq(words) -> list[str]:
    freqs = get_freqs(words)
    return sorted(words, key=freqs.__getitem__, reverse=True)


if __name__ == "__main__":
    words = ["career", "the", "avaricious"]
    print(sort_by_freq(words))
