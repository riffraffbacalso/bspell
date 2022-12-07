from args import get_args
from formatting import fprint
from scrape import get_problem
from solve import solve_bee
from word_freq import sort_by_freq


def main() -> None:
    args = get_args()
    problem, answers = (args.problem, []) if args.problem else get_problem()
    words = solve_bee(problem, args.word_src)
    words = sort_by_freq(words)
    fprint(words, answers)


if __name__ == "__main__":
    main()
