"""Command-line entry point: `python -m app.cli --help`."""
import argparse

from app.core import complete, milestone_2, milestone_4


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="medical-notes-helper", description="Clinic staff use this CLI tool to draft administrative sections of medical notes by generating next-word suggestions, ensuring consistency and reducing manual typing.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("hello", help="check that everything is wired up")

    suggest = sub.add_parser("suggest", help="show next-word suggestions for some text")
    suggest.add_argument("text")
    suggest.add_argument("--n", type=int, default=3, help="n-gram order (2 = bigram, 3 = trigram)")
    suggest.add_argument("--top", type=int, default=3, help="how many suggestions to show")

    draft = sub.add_parser("complete", help="draft the rest of a sentence")
    draft.add_argument("text")
    draft.add_argument("--n", type=int, default=3)
    draft.add_argument("--words", type=int, default=8, help="how many words to add")

    sub.add_parser("chat", help="type text and get suggestions until you press Enter on an empty line")

    args = parser.parse_args(argv)
    if args.command == "hello":
        print("Medical Notes Helper is ready. Open README.md for your milestones.")
    elif args.command == "suggest":
        print(milestone_4(milestone_2(n=args.n), args.text, args.top))
    elif args.command == "complete":
        print(complete(milestone_2(n=args.n), args.text, args.words))
    elif args.command == "chat":
        model = milestone_2()
        print("Type the start of a sentence. Press Enter on an empty line to quit.")
        while True:
            try:
                text = input("> ").strip()
            except EOFError:
                break
            if not text:
                break
            print(milestone_4(model, text))
            print("Draft:", complete(model, text))


if __name__ == "__main__":
    main()
