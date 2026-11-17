# tiny-chess-01-engine

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/hy3188/tiny-chess-01-engine/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/hy3188/tiny-chess-01-engine/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A complete chess engine in a single 4,085-byte Python file, built for
[the tiny-chess-01 contest](https://make.fun/bounty/tiny-chess-01): `main.py`
is at most 4,096 bytes, Python 3.13 standard library only, fully
deterministic (fixed node budget, never a clock).

## What is inside

- 0x88 board, pseudo-legal move generation with king-capture detection
  (castling and queen promotions included; en-passant captures omitted
  for size)
- Negamax alpha-beta with a transposition table (exact/lower/upper
  bounds), late-move reductions, and captures-only quiescence with
  stand-pat
- MVV-LVA capture ordering plus transposition-table move ordering
- Repetition avoidance: positions already seen in the current game score
  as draws inside the search, so a better position is never shuffled away
- Evaluation: material, formula piece-square tables (pawn advancement,
  piece centrality, rook files), and a king term that switches between
  middlegame shelter (advanced kings are penalised) and endgame
  centrality by game phase
- Iterative deepening to a fixed budget of 100,000 nodes per move

## Run it

```sh
MAKEFUN_ENV_URL=http://localhost:PORT python3 main.py
```

The bot loops on the env: `POST /game` for the next position, search,
`POST /move` with the chosen move, until the trial reports `done`.

Local practice (kit trial 0 / trial 1, six house rungs each): practice
Elo ≈ 1191 and ≈ 1279 against the kit anchors (final gate: 1154).

MIT licensed.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qzrn75rv&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
