# Medical Notes Helper

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/medical-notes-helper/badge.svg)](https://ask.thili.ai)

A command-line tool that helps clinic staff draft administrative sections of medical notes. It suggests the next word using an n-gram language model trained on an anonymized corpus. It runs on your laptop with no API key, no downloads and no extra packages.

## How it works

1. **Corpus (data/corpus.txt):** 36 administrative clinic sentences. Names, emails, phones, dates, times and numbers are replaced with placeholders such as <phone> and <date>, then the text is lowercased and tokenized.
2. **N-gram model with smoothing:** counts every sequence of n words and estimates P(next word | previous n-1 words). Add-k smoothing gives unseen words a small probability. If the context was never seen, it falls back to overall word frequency.
3. **Suggestions:** the top words by probability for the text typed so far, plus a greedy "draft the rest" mode.
4. **CLI:** suggest, complete and chat commands.

## Run it

You need Python 3.12 and git.

    python3.12 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    python -m app.cli hello
    pytest

## Use it

    python -m app.cli suggest "please bring your"
    python -m app.cli suggest "the patient was" --n 2 --top 5
    python -m app.cli complete "your appointment with"
    python -m app.cli chat

Use --n 2 for a bigram model or --n 3 for a trigram model.

## Files

- app/core.py: cleaning, n-gram model, suggestions, output formatting.
- app/cli.py: the command-line interface.
- tests/test_core.py: one test per milestone.
- data/corpus.txt: the anonymized training text.

## Notes

- The corpus is small and written for this project, so suggestions are limited to its phrases. Adding more text improves them.
- Never commit .env.
