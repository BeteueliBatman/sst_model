from __future__ import annotations

import argparse

from .agent import STTCorrectionAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Georgian STT autocorrect using local LLM")
    parser.add_argument("text", help="Raw STT text in Georgian")
    args = parser.parse_args()

    agent = STTCorrectionAgent()
    result = agent.correct_text(args.text)
    print(result.corrected_text)


if __name__ == "__main__":
    main()
