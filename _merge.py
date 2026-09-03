import json, os, subprocess, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def show(ref, path):
    return subprocess.run(['git','show',f'{ref}:{path}'], capture_output=True, text=True).stdout

# ---- results/backtests.json : union, mine renumbered 35 -> 36 ----
theirs = json.loads(show('HEAD', 'results/backtests.json'))          # cloud side (rebase base)
mine   = json.loads(show('27d7106', 'results/backtests.json'))       # my commit

have = {r['id'] for r in theirs}
added = 0
for r in mine:
    if r['id'] == 'attack35a-narrow-day-expansion-h1':
        r['id']   = 'attack36a-narrow-day-expansion-h1'
        r['name'] = 'Attack 36a: narrow-range day expansion, NEVER-TUNED half'
        r['specPath'] = 'strategies/pine/attack36-narrow-day-expansion.pine'
        r['description'] = r['description'].replace('Discovery mechanism #4', 'Discovery mechanism #4 (numbered 36 after the cloud routine claimed 35 for a 1.5R sweep on Attack 34)')
        r['notes'] = ('NUMBERING: run as "Attack 35" locally, renumbered to 36 on merge -- the cloud '
                      'routine independently claimed 35 the same hour for a 1.5R target sweep on Attack 34 '
                      '(PF 1.277564/31 and 1.08255083/24, REVERTED because it does not touch the drawdown). '
                      'Same collision class as the v50 clash. ') + r['notes']
    if r['id'] not in have:
        theirs.append(r); have.add(r['id']); added += 1
json.dump(theirs, open('results/backtests.json','w'), indent=1)
print('btc records:', len(theirs), '| added', added)

# ---- CHAMPION-BOARD.md : their version + my Attack 36 section renumbered ----
board_theirs = show('HEAD', 'CHAMPION-BOARD.md')
board_mine   = show('27d7106', 'CHAMPION-BOARD.md')
marker = '\n\n---\n\n# ██ ATTACK 35 — NARROW-RANGE DAY EXPANSION.'
assert marker in board_mine
my_section = board_mine[board_mine.index(marker):]
my_section = (my_section
    .replace('# ██ ATTACK 35 — NARROW-RANGE DAY EXPANSION. DISCARDED, AND IT CORRECTS THE BOARD\'S OWN QUEUE ITEM.',
             '# ██ ATTACK 36 — NARROW-RANGE DAY EXPANSION. DISCARDED, AND IT CORRECTS THE BOARD\'S OWN QUEUE ITEM.')
    .replace('Attack 35 was built to attack that number at its root.',
             'Attack 36 was built to attack that number at its root.\n\n**NUMBERING NOTE.** This ran locally as "Attack 35" while the cloud routine, in the same hour,\nindependently claimed 35 for a 1.5R target sweep on Attack 34 (PF 1.277564 / 31 trades and\n1.08255083 / 24 trades, **REVERTED** because a lower target does not touch the drawdown — the correct\ncall, and consistent with this board\'s queue). Renumbered to 36 on merge. Same collision class as the\nv50 clash in 3M: two lineages numbering into the same space.')
    .replace('Attack 35\'s stop is the compressed day\'s low', 'Attack 36\'s stop is the compressed day\'s low')
    .replace('| | 35a · NEVER-TUNED |', '| | 36a · NEVER-TUNED |'))
open('CHAMPION-BOARD.md','w').write(board_theirs + my_section)
print('board merged')

# ---- pine file rename ----
old, new = 'strategies/pine/attack35-narrow-day-expansion.pine', 'strategies/pine/attack36-narrow-day-expansion.pine'
if os.path.exists(old):
    s = open(old, encoding='utf-8').read()
    s = s.replace('// BTC ATTACK 35 - NARROW-RANGE DAY EXPANSION (BARE).',
                  '// BTC ATTACK 36 - NARROW-RANGE DAY EXPANSION (BARE).\n// NUMBERING: ran as Attack 35; renumbered on merge after the cloud routine claimed 35 the same hour\n// for a 1.5R sweep on Attack 34 (both halves cleared 1.0, REVERTED for not touching the drawdown).')
    s = s.replace('strategy("BTC Attack35 narrow-range day expansion"', 'strategy("BTC Attack36 narrow-range day expansion"')
    open(new,'w',encoding='utf-8').write(s)
    os.remove(old)
    print('pine renamed')
