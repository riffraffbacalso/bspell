from concurrent.futures import ThreadPoolExecutor
import httpx


def get_ranks(words):
    url = "https://api.datamuse.com/words"
    with httpx.Client(http2=True) as client:

        def get_rank(word):
            return client.get(f"{url}?sp={word}&md=f&max=1").json()

        with ThreadPoolExecutor(max_workers=200) as pool:
            ranks = [float(obj[0]["tags"][0][2:]) for obj in pool.map(get_rank, words)]

    return dict(zip(words, ranks))


def sort_words(words):
    ranks = get_ranks(words)
    return sorted(words, key=lambda x: ranks[x], reverse=True)


if __name__ == "__main__":
    words = ["career", "the", "avaricious"]
    print(sort_words(words))
