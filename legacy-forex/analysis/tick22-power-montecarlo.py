import random, bisect
random.seed(20260906)

# The R outcomes his decoded spec actually produces -- a SHAPE assumption about trade
# anatomy, NOT a performance claim. Every probability below is varied, not asserted.
#   -1.0R  full stop, just beyond the broken level   (11._STOP_LOSS_ADJUSTMENT [00:07])
#   -0.3R  early cut when volume dies                (9._VOLUME [03:18] "seven points" vs 15)
#    0.0R  break-even close of the weaker leg        (SYSTEM.md 24.4)
#   +1..+4R target rungs; observed ceiling is 4R     (SYSTEM.md 24.2)
OUT = [-1.0, -0.3, 0.0, 1.0, 2.0, 3.0, 4.0]


def calibrate(shape):
    """Scale the winning tail until the POPULATION profit factor is exactly 1.0."""
    lo, hi = 0.0, 50.0
    for _ in range(300):
        mid = (lo + hi) / 2
        w = [p * (mid if o > 0 else 1.0) for o, p in zip(OUT, shape)]
        s = sum(w); w = [x / s for x in w]
        g = sum(p * o for o, p in zip(OUT, w) if o > 0)
        l = -sum(p * o for o, p in zip(OUT, w) if o < 0)
        if g / l < 1.0: lo = mid
        else: hi = mid
    w = [p * (hi if o > 0 else 1.0) for o, p in zip(OUT, shape)]
    s = sum(w)
    return [x / s for x in w]


SHAPES = {
    "ladder-heavy (many small rungs)":  [0.30, 0.15, 0.10, 0.20, 0.12, 0.08, 0.05],
    "target-heavy (mostly 3R exits)":   [0.45, 0.10, 0.05, 0.05, 0.10, 0.20, 0.05],
    "chop (early cuts dominate)":       [0.20, 0.40, 0.15, 0.10, 0.08, 0.05, 0.02],
    "two-outcome (pure 3R binomial)":   [0.75, 0.00, 0.00, 0.00, 0.00, 0.25, 0.00],
}

POOL = 2_000_000
NS = (30, 100, 400, 2000)
TRIALS = 40_000

print("TRUE profit factor forced to EXACTLY 1.0 in every row -- zero edge by construction.")
print("Reported: how often the protocol's accept rule 'PF > 1.0' PASSES the worthless system.")
print(f"(Monte Carlo, {TRIALS:,} trials/cell, pool {POOL:,}; MC error ~ +/-0.005)\n")
print(f"{'R-distribution shape':34s}" + "".join(f"n={n:<9d}" for n in NS))

for name, sh in SHAPES.items():
    w = calibrate(sh)
    cum = []; t = 0.0
    for x in w:
        t += x; cum.append(t)
    # one pool of iid draws; prefix sums make each trial O(1)
    G = [0.0] * (POOL + 1); L = [0.0] * (POOL + 1)
    g = l = 0.0
    for i in range(POOL):
        o = OUT[bisect.bisect(cum, random.random())]
        if o > 0: g += o
        elif o < 0: l -= o
        G[i + 1] = g; L[i + 1] = l
    row = ""
    for n in NS:
        hits = 0
        top = POOL - n
        for _ in range(TRIALS):
            s = random.randrange(top)
            gl = L[s + n] - L[s]
            if gl == 0 or (G[s + n] - G[s]) / gl > 1.0:
                hits += 1
        row += f"{hits/TRIALS:<11.4f}"
    print(f"{name:34s}{row}")
