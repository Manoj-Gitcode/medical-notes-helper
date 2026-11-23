# Medical Notes Helper

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/dgtg7wpgzp/badge.svg)](https://ask.thili.ai/b/dgtg7wpgzp)

The Medical Notes Helper is a CLI tool designed for clinic staff to streamline the drafting of administrative medical notes. It uses a next-word prediction engine, built from scratch, to offer context-aware suggestions, enhancing consistency and efficiency in documentation. This project demonstrates your ability to apply language models for practical text generation tasks, as taught in `lfllm-lfnextword`.

## What you are building

**Goal.** You will build a command-line interface (CLI) tool that helps clinic staff draft administrative sections of medical notes by generating next-word suggestions, ensuring consistency and reducing manual typing.

**Done when.** The project is complete when you have a CLI tool that takes user input, provides next-word suggestions using an n-gram language model trained on medical text, and allows clinic staff to interact with the suggestion engine.

## Milestones

Tick these off as you go, and commit after each one.

- [ ] **1. Curate an anonymized corpus of administrative medical text.**  
      Hint: Focus on text preprocessing techniques from `lfllm-lfnextword` to clean and tokenize your corpus.
- [ ] **2. Implement the n-gram language model and apply smoothing.**  
      Hint: Apply the n-gram counting and probability calculation methods, including smoothing, as covered in `lfllm-lfnextword`.
- [ ] **3. Develop a text generation feature that suggests words based on input.**  
      Hint: Use your implemented n-gram model to predict the next word given a sequence, similar to the generation examples in `lfllm-lfnextword`.
- [ ] **4. Create a CLI for users to interact with the suggestion engine.**  
      Hint: Design a user-friendly command-line interface to take input and display suggestions from your language model.

## Run it

You need Python 3.12 and git.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then choose a model; see the comments inside
python -m app.cli hello
pytest
```

Your work goes in `app/core.py` (one stub per milestone) and `tests/test_core.py`. The first tests pass already; they
check the plumbing.

## Settings and secrets

Model settings live in `.env`, which is ignored by git. **Never commit `.env` or paste a key into code.** If a key ever
reaches GitHub, treat it as leaked and make a new one.

## Stretch ideas

- Allow the user to specify the n-gram order (e.g., bigram, trigram) at runtime for different suggestion behaviors.
- Implement a feature to save and load user-specific common phrases or acronyms to influence suggestions.
