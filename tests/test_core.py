"""Your tests. Each milestone in README.md gets one here."""
import pytest

from app.core import NGramModel, anonymize, complete, milestone_1, milestone_2, milestone_3, milestone_4

TINY = [["please", "bring", "your", "insurance", "card"]] * 3 + [["please", "bring", "your", "id"]]


# Milestone 1: Curate an anonymized corpus of administrative medical text.
def test_milestone_1():
    assert anonymize("Call 555-123-4567 or mail a@b.org on 12/05/2026") == "Call <phone> or mail <email> on <date>"
    sentences = milestone_1()
    assert len(sentences) >= 30
    words = {w for s in sentences for w in s}
    assert "<phone>" in words and "<email>" in words
    assert not any(ch.isdigit() or ch == "@" for w in words for ch in w)


# Milestone 2: Implement the n-gram language model and apply smoothing.
def test_milestone_2():
    model = milestone_2(TINY, n=3, k=0.1)
    seen = model.prob("insurance", ["bring", "your"])
    unseen = model.prob("card", ["bring", "your"])
    assert seen > unseen > 0  # smoothing keeps unseen words possible
    total = sum(model.prob(w, ["bring", "your"]) for w in model.vocab)
    assert total == pytest.approx(1.0)


# Milestone 3: Develop a text generation feature that suggests words based on input.
def test_milestone_3():
    model = milestone_2(TINY, n=3)
    suggestions = milestone_3(model, "Please bring your", top=2)
    assert suggestions[0][0] == "insurance"
    assert len(suggestions) == 2
    assert complete(model, "please bring", max_words=2).startswith("please bring your")


# Milestone 4: Create a CLI for users to interact with the suggestion engine.
def test_milestone_4(capsys):
    from app.cli import main

    text = milestone_4(milestone_2(TINY), "please bring your")
    assert "1. insurance" in text
    main(["suggest", "please bring your", "--top", "2"])
    assert "Suggestions after" in capsys.readouterr().out
