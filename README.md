# Stepwise

A word-ladder game: change one thing at a time, and every step must be a new, real word.

Pick a mode: **Classic** gives you 50 steps to score as many points as you can, and **Free play** goes on until you run out of legal moves. Start from a common 4-letter word with a bank of 6 letters. Each move must make a real word of 3+ letters that isn't already on your ladder:

- **Add** a bank letter anywhere in the word (the bank refills)
- **Remove** a letter
- **Shift** a letter to a new spot
- **Swap** two letters
- **Replace** a letter with one from the bank (the bank refills)

Each word scores the value of its letters, from 1 for common letters like A and E up to 5 for J, Q, X and Z, and letters from the starting word are worth 0. Words of 6+ letters score their length on top (+6 for 6 letters, +7 for 7). A word that fits the current **category bonus** (Animal, Color, Music, …) scores +20, and using all five kinds of move lights up the **Toolkit bonus** for +10. Three one-time powers (Exchange letters, Choose a letter, Backtrack), a one-step undo, 3 hints per game and 19 achievements round it out.

## Play

The game is a single self-contained page with no server or dependencies:

- `index.html` is the main layout (recent words and bonuses in the right column).
- `classic.html` is the original layout (full ladder in the right column).

Open either file in a browser, or serve the repository with any static host. To publish with **GitHub Pages**: Settings → Pages → Source: *Deploy from a branch* → Branch: `main`, folder `/ (root)`. The game will be at `https://<user>.github.io/<repo>/`.

Progress, best score, achievements and the light/dark choice are saved in the player's browser (`localStorage`).

## Change the game

Edit the source in `src/`, then rebuild the two pages:

```sh
python3 src/build.py
```

- `src/template.html` holds the layout, styles and all game logic.
- `src/build.py` holds the bonus-category word lists and embeds the dictionary, start words and categories into `index.html` and `classic.html`.
- `src/data/enable1.txt` is the ENABLE word list (public domain), used to check words.
- `src/data/google-10000-english-usa-no-swears.txt` comes from [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english) and is used to pick common starting words.

Commit the rebuilt `index.html` and `classic.html` along with your source changes, since those are the files the host serves.
