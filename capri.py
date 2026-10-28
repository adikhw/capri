import sys
import os
import difflib

from pathlib import Path
from dataclasses import dataclass

START_DIR = Path.home()
IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".cache", ".venv", "venv", ".npm"}
MAX_RESULTS = 10
MAX_SUGGESTIONS = 3
CLOSE_CUTOFF = 0.6
BASE_POINT = 1
CONSECUTIVE_BONUS = 2
WORD_START_BONUS = 3
PREFIX_BONUS = 5
EXACT_MATCH_BONUS = 10
LENGTH_PENALTY = 0.01
NAME_WEIGHT = 2
SEPARATOR = {"/", "_", "-", ".", " "}


@dataclass
class Entry:
    name: str
    full_path: str
    is_dir: bool


def parse_query(argv):
    words = argv[1:]
    query = " ".join(words).strip()

    if not query:
        print("Usage: capri <file/folder name>", file=sys.stderr)
        sys.exit(2)

    return query


def collect_entries(start_dir):
    entries = []

    for current_folder, dirs, files in os.walk(start_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for d in dirs:
            full_path = os.path.join(current_folder, d)
            entries.append(Entry(name=d, full_path=full_path, is_dir=True))

        for f in files:
            full_path = os.path.join(current_folder, f)
            entries.append(Entry(name=f, full_path=full_path, is_dir=False))

    return entries


def fuzzy_score(query, target):
    q = query.lower()
    t = target.lower()
    score = 0
    start_position = 0
    previous_position = -1

    for char in q:
        position = t.find(char, start_position)

        if position == -1:
            return 0

        score += BASE_POINT

        if position == previous_position + 1:
            score += CONSECUTIVE_BONUS

        if position == 0 or t[position - 1] in SEPARATOR:
            score += WORD_START_BONUS

        previous_position = position
        start_position = position + 1

    if t == q:
        score += EXACT_MATCH_BONUS
    elif t.startswith(q):
        score += PREFIX_BONUS 

    score -= len(t) * LENGTH_PENALTY

    return max(score, 1)

