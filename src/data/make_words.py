#!/usr/bin/env python3
"""Regenerates words.txt, the game's dictionary: everyday words, in the spirit of the NYT Spelling Bee.

A word is kept when it is in ENABLE (enable1.txt), in SCOWL's common-English lists
(size 50 or smaller, American and general English), and used often enough in real text
(wordfreq Zipf frequency of at least MIN_ZIPF). An inflected form (CLANKS, WAKENED, GNASHING)
also counts when its base word does, since inflections are rarer in text than the words they
come from. Offensive words in BLOCK are left out.

  pip install wordfreq
  curl -L -o scowl.tgz https://downloads.sourceforge.net/wordlist/scowl-2020.12.07.tar.gz && tar xzf scowl.tgz
  python3 src/data/make_words.py path/to/scowl-2020.12.07/final
"""
import glob, os, re, sys
from wordfreq import zipf_frequency

SCOWL_SIZE, MIN_ZIPF = 50, 1.5
BLOCK = set("""
bitch bitches bitchy bastard bastards cunt cunts dildo dildos dyke dykes fag fags faggot faggots fuck
fucked fucker fuckers fucking fucks gook gooks homo homos jap japs kike kikes nigger niggers piss pissed pisses
pissing pussy pussies shit shits shitty slut sluts slutty spic spics twat twats wank
wanker whore whores wop wops retard retards retarded tits titty boob boobs crap craps crappy douche
douches jism jizz porn porno pornos skank skanks turd turds wetback wetbacks honky honkies
""".split())

here = os.path.dirname(os.path.abspath(__file__))
enable = {w for w in open(os.path.join(here, "enable1.txt")).read().split() if 3 <= len(w) <= 15}
common = set()
for f in glob.glob(os.path.join(sys.argv[1], "*")):
    m = re.fullmatch(r"(english|american)-words\.(\d+)", os.path.basename(f))
    if m and int(m.group(2)) <= SCOWL_SIZE:
        common |= {w.strip() for w in open(f, encoding="latin-1") if re.fullmatch(r"[a-z]+", w.strip())}
pool = {w for w in enable & common if w not in BLOCK}
base_ok = {w for w in pool if zipf_frequency(w, "en") >= MIN_ZIPF}


def bases(w):
    for suf, rep in (("s", ""), ("es", ""), ("ies", "y"), ("ed", ""), ("ed", "e"), ("ied", "y"), ("ing", ""), ("ing", "e"),
                     ("er", ""), ("er", "e"), ("ier", "y"), ("est", ""), ("est", "e"), ("iest", "y"), ("ly", ""), ("ily", "y")):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            b = w[: -len(suf)] + rep
            yield b
            if len(b) > 3 and b[-1] == b[-2]:
                yield b[:-1]  # doubled consonant: SKIPPED -> SKIP


words = sorted(w for w in pool if w in base_ok or any(b in base_ok for b in bases(w)))
open(os.path.join(here, "words.txt"), "w").write("\n".join(words) + "\n")
print(len(words), "words")
