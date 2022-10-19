from concurrent.futures import ThreadPoolExecutor
import httpx


def get_ranks(words: list[str]) -> dict[str, float]:
    url = "https://api.datamuse.com/words"
    with httpx.Client(http2=True) as client:

        def request(word: str) -> httpx.Response:
            return client.get(f"{url}?sp={word}&md=f&max=1")

        def extract(res: httpx.Response) -> float:
            return float(res.json()[0]["tags"][0][2:])

        with ThreadPoolExecutor(max_workers=50) as pool:
            ranks = [extract(res) for res in pool.map(request, words)]

    return dict(zip(words, ranks))


def sort_words(words) -> list[str]:
    ranks = get_ranks(words)
    return sorted(words, key=lambda x: ranks[x], reverse=True)


if __name__ == "__main__":
    words = ["career", "the", "avaricious"]
    print(sort_words(words))
