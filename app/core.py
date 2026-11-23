"""Your code. One stub per milestone; build them in order and keep each one small."""
import re
from collections import Counter
from pathlib import Path

CORPUS_PATH = Path(__file__).resolve().parent.parent / "data" / "corpus.txt"


# --- Milestone 1: Curate an anonymized corpus of administrative medical text.
def anonymize(text):
    """Replace personal details (emails, dates, phones, times, numbers, names) with placeholders."""
    text = re.sub(r"\[([A-Za-z]+)\]", lambda m: f"<{m.group(1).lower()}>", text)
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "<email>", text)
    text = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "<date>", text)
    text = re.sub(r"\b\d{3}[-. ]?\d{3}[-. ]?\d{4}\b", "<phone>", text)
    text = re.sub(r"\b\d{1,2}:\d{2}\b", "<time>", text)
    return re.sub(r"\b\d+\b", "<num>", text)


def tokenize(text):
    """Lowercase and split into words and placeholders (punctuation is dropped)."""
    return re.findall(r"<[a-z]+>|[a-z]+", text.lower())


def milestone_1(path=CORPUS_PATH):
    """Read the corpus, anonymize it, and return one list of tokens per sentence."""
    lines = Path(path).read_text().splitlines()
    return [tokens for tokens in (tokenize(anonymize(line)) for line in lines) if tokens]


# --- Milestone 2: Implement the n-gram language model and apply smoothing.
class NGramModel:
    """An n-gram model with add-k smoothing."""

    def __init__(self, n=3, k=0.1):
        self.n = n
        self.k = k
        self.ngrams = Counter()    # counts of (context..., word)
        self.contexts = Counter()  # counts of context
        self.unigrams = Counter()  # counts of single words
        self.vocab = set()

    def fit(self, sentences):
        for sentence in sentences:
            tokens = ["<s>"] * (self.n - 1) + sentence + ["</s>"]
            self.vocab.update(sentence + ["</s>"])
            for i in range(self.n - 1, len(tokens)):
                context = tuple(tokens[i - self.n + 1:i])
                self.ngrams[context + (tokens[i],)] += 1
                self.contexts[context] += 1
                self.unigrams[tokens[i]] += 1
        return self

    def _context(self, words):
        padded = ["<s>"] * (self.n - 1) + list(words)
        return tuple(padded[len(padded) - (self.n - 1):])

    def prob(self, word, words):
        """P(word | previous words) with add-k smoothing; falls back to word frequency if the context is new."""
        context = self._context(words)
        size = len(self.vocab)
        if self.contexts[context] == 0:
            return (self.unigrams[word] + self.k) / (sum(self.unigrams.values()) + self.k * size)
        return (self.ngrams[context + (word,)] + self.k) / (self.contexts[context] + self.k * size)

    def suggest(self, words, top=3):
        """The `top` most likely next words as (word, probability) pairs."""
        scored = [(w, self.prob(w, words)) for w in self.vocab if w != "</s>"]
        scored.sort(key=lambda pair: (-pair[1], pair[0]))
        return scored[:top]


def milestone_2(sentences=None, n=3, k=0.1):
    """Train an n-gram model (on the bundled corpus unless sentences are given)."""
    return NGramModel(n=n, k=k).fit(sentences if sentences is not None else milestone_1())


# --- Milestone 3: Develop a text generation feature that suggests words based on input.
def milestone_3(model, text, top=3):
    """Next-word suggestions for the text typed so far."""
    return model.suggest(tokenize(anonymize(text)), top)


def complete(model, text, max_words=8):
    """Draft a continuation by repeatedly adding the most likely next word."""
    words = tokenize(anonymize(text))
    for _ in range(max_words):
        word = model.suggest(words, 1)[0][0]
        words.append(word)
        if word in ("<phone>", "<email>"):
            break
    return " ".join(words)


# --- Milestone 4: Create a CLI for users to interact with the suggestion engine.
def milestone_4(model, text, top=3):
    """The text the CLI prints: a numbered list of suggestions with percentages."""
    lines = [f'Suggestions after "{text}":']
    for i, (word, p) in enumerate(milestone_3(model, text, top), start=1):
        lines.append(f"  {i}. {word}  ({p * 100:.1f}%)")
    return "\n".join(lines)
