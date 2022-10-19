from scrape import get_letters
from solve import solve_bee


def main() -> None:
    print(solve_bee(get_letters()))


if __name__ == "__main__":
    main()
