#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
from jsonschema.exceptions import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation.benchmark import FILES, evaluate, markdown, read, write


def main():
    parser = argparse.ArgumentParser(description="Evaluate three external JSON results against annotated facts")
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        docs = {k: read(args.predictions / (v + ".json")) for k, v in FILES.items()}
        result = evaluate(read(args.ground_truth), docs)
        write(args.output / "report.json", result)
        with (args.output / "report.md").open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(markdown(result))
    except (ValueError, OSError, KeyError, ValidationError) as exc:
        parser.exit(2, f"Invalid input: {exc}\n")
    print(args.output / "report.md")


if __name__ == "__main__":
    main()
