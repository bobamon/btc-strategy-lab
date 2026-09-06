import json, math, statistics as st
from datetime import date

GAMMA = 0.5772156649015329
E = math.e

def norm_cdf(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def norm_ppf(p):
    # Acklam's inverse normal CDF, |eps| < 1.15e-9
    a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00]
    b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,-1.328068155288572e+01]
    c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00]
    dd=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00]
    pl,ph=0.02425,1-0.02425
    if p<pl:
        q=math.sqrt(-2*math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((dd[0]*q+dd[1])*q+dd[2])*q+dd[3])*q+1)
    if p>ph:
        q=math.sqrt(-2*math.log(1-p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((dd[0]*q+dd[1])*q+dd[2])*q+dd[3])*q+1)
    q=p-0.5; r=q*q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)

def expected_max_sr(N, sd, mu=0.0):
    """Bailey & Lopez de Prado expected maximum Sharpe of N independent null trials."""
    return mu + sd*((1-GAMMA)*norm_ppf(1-1.0/N) + GAMMA*norm_ppf(1-1.0/(N*E)))

def yrs(r):
    return (date.fromisoformat(r['backtestEnd'])-date.fromisoformat(r['backtestStart'])).days/365.25

d=json.load(open('/home/user/btc-strategy-lab/results/backtests.json'))
recs=[r for r in d if 'sharpeRatio' in r['metrics']]

def report(label, pool):
    srs=[r['metrics']['sharpeRatio'] for r in pool]
    N=len(srs); sd=st.stdev(srs); mu=st.mean(srs)
    best=max(pool, key=lambda r:r['metrics']['sharpeRatio'])
    e0=expected_max_sr(N, sd, 0.0)
    em=expected_max_sr(N, sd, mu)
    print(f"\n### {label}")
    print(f"  N trials = {N}   trial-SR mean = {mu:+.4f}   sd = {sd:.4f}")
    print(f"  E[max SR] null centred at 0    = {e0:.4f}")
    print(f"  E[max SR] null centred at mean = {em:.4f}")
    print(f"  BEST OBSERVED SR = {best['metrics']['sharpeRatio']:.4f}  ({best['id']})")
    print(f"  best - E[max|0]  = {best['metrics']['sharpeRatio']-e0:+.4f}")
    print(f"  how many trials exceed E[max|0]: {sum(1 for s in srs if s>e0)}")
    return e0,em,N,sd,mu

pools = {
 'ALL recorded Sharpes': recs,
 'n>=10 trades': [r for r in recs if r['metrics']['totalTrades']>=10],
 'n>=10 and SR>-5 (drops the attack57 fee blowout)': [r for r in recs if r['metrics']['totalTrades']>=10 and r['metrics']['sharpeRatio']>-5],
 'H1 window only (2022-01-01 -> 2024-06-08)': [r for r in recs if r['backtestStart']=='2022-01-01'],
 'H1, n>=10 and SR>-5': [r for r in recs if r['backtestStart']=='2022-01-01' and r['metrics']['totalTrades']>=10 and r['metrics']['sharpeRatio']>-5],
 'H2 window only (2024-06-08 -> 2026-09-01)': [r for r in recs if r['backtestStart']=='2024-06-08'],
}
res={}
for k,v in pools.items(): res[k]=report(k,v)

print("\n\n### TOP 12 BY SHARPE, WITH IMPLIED t = SR * sqrt(years)")
print(f"{'id':<52}{'win':<4}{'SR':>8}{'yrs':>7}{'t':>7}{'PF':>8}{'n':>6}")
for r in sorted(recs,key=lambda r:-r['metrics']['sharpeRatio'])[:12]:
    m=r['metrics']; y=yrs(r); t=m['sharpeRatio']*math.sqrt(y)
    win='H1' if r['backtestStart']=='2022-01-01' else 'H2'
    print(f"{r['id'][:52]:<52}{win:<4}{m['sharpeRatio']:>8.3f}{y:>7.2f}{t:>7.2f}{m['profitFactor']:>8.3f}{m['totalTrades']:>6d}")

print("\n### BONFERRONI z-HURDLE FROM THE BOARD'S OWN TRIAL COUNT")
for N in (79,73,98):
    for alpha in (0.05,0.10):
        z=norm_ppf(1-alpha/(2*N))
        print(f"  N={N:<4} alpha={alpha:<5} two-sided Bonferroni z = {z:.3f}")

# ---------------------------------------------------------------------------
# Reproduces every number in CHAMPION-BOARD.md "THE MULTIPLE-TESTING AUDIT".
# Reads only results/backtests.json. Runs no backtest and spends no credits.
#   python3 analysis/multiple_testing_audit.py
# ---------------------------------------------------------------------------
import collections, re
def _years(r):
    return (date.fromisoformat(r['backtestEnd'])-date.fromisoformat(r['backtestStart'])).days/365.25

def main(path='results/backtests.json'):
    recs=[r for r in json.load(open(path)) if 'sharpeRatio' in r['metrics']]
    print(f"recorded Sharpes: {len(recs)}\n")

    print("PART 1 - per-trade Sharpe CEILING (two-point trade distribution = minimum variance)")
    for r in sorted(recs,key=lambda r:-r['metrics']['sharpeRatio'])[:8]:
        m=r['metrics']
        if 'avgWinningTrade' not in m: continue
        p=m['winRatePct']/100.0; W=m['avgWinningTrade']; L=-abs(m['avgLosingTrade'])
        ceil=(p*W+(1-p)*L)/(math.sqrt(p*(1-p))*(W-L))
        print(f"  {r['id'][:44]:<44} max SR/trade {ceil:6.3f}   recorded {m['sharpeRatio']:6.3f}")

    print("\nPART 2 - E[max SR | null] by trial pool")
    pools={'all':recs,
           'n>=10':[r for r in recs if r['metrics']['totalTrades']>=10],
           'n>=10 & SR>-5':[r for r in recs if r['metrics']['totalTrades']>=10 and r['metrics']['sharpeRatio']>-5],
           'H1':[r for r in recs if r['backtestStart']=='2022-01-01'],
           'H1 trimmed':[r for r in recs if r['backtestStart']=='2022-01-01' and r['metrics']['totalTrades']>=10 and r['metrics']['sharpeRatio']>-5],
           'H2':[r for r in recs if r['backtestStart']=='2024-06-08']}
    for k,v in pools.items():
        s=[r['metrics']['sharpeRatio'] for r in v]
        print(f"  {k:<16} N={len(s):<3} mean {st.mean(s):+.4f}  sd {st.stdev(s):.4f}  "
              f"E[max]={expected_max_sr(len(s),st.stdev(s)):.3f}  best={max(s):.3f}  clearing={sum(1 for x in s if x>expected_max_sr(len(s),st.stdev(s)))}")

    print("\nPART 4 - implied t = SR*sqrt(years), and the board's own Bonferroni bar")
    for r in sorted(recs,key=lambda r:-r['metrics']['sharpeRatio'])[:8]:
        m=r['metrics']; y=_years(r)
        print(f"  {r['id'][:44]:<44} SR {m['sharpeRatio']:5.3f}  {y:.2f}y  t={m['sharpeRatio']*math.sqrt(y):.2f}")
    for N in (73,79,98):
        print(f"  Bonferroni N={N:<4} alpha=0.05 -> z={norm_ppf(1-0.05/(2*N)):.3f}   alpha=0.10 -> z={norm_ppf(1-0.10/(2*N)):.3f}")

    print("\nPART 5 - break-even N_eff, and the mechanism-family census")
    for sd,lab in ((1.4579,'all 79'),(0.7835,'n>=10 & SR>-5'),(0.8749,'H1 trimmed')):
        for tgt,who in ((1.2942,'attack88a'),(0.9424,'attack46b')):
            lo,hi=1.0001,1e6
            for _ in range(200):
                mid=math.sqrt(lo*hi)
                (lo,hi)=(mid,hi) if expected_max_sr(mid,sd)<tgt else (lo,mid)
            print(f"  sd={sd:<7} {who} (SR {tgt}) clears only if N_eff <= {lo:.2f}")
    fams={re.sub(r'-h[12]$','',re.sub(r'^attack\d+[ab]?-','',r['id'])) for r in recs}
    obv={f for f in fams if 'obv' in f}
    neff=len(fams)-len(obv)+1
    print(f"  distinct slugs {len(fams)}, OBV family {len(obv)}, ultra-conservative N_eff {neff}")
    for sd in (0.7835,0.8749):
        print(f"    hurdle at N_eff={neff}, sd={sd}: {expected_max_sr(neff,sd):.3f}")

if __name__=='__main__':
    main()

def t_units(path='results/backtests.json'):
    """The follow-up entry: both hurdles expressed in t units, so they are commensurable."""
    recs=[r for r in json.load(open(path)) if 'sharpeRatio' in r['metrics']]
    pools={'all':recs,
           'all trimmed':[r for r in recs if r['metrics']['totalTrades']>=10 and r['metrics']['sharpeRatio']>-5],
           'H1':[r for r in recs if r['backtestStart']=='2022-01-01'],
           'H1 trimmed':[r for r in recs if r['backtestStart']=='2022-01-01' and r['metrics']['totalTrades']>=10 and r['metrics']['sharpeRatio']>-5],
           'H2':[r for r in recs if r['backtestStart']=='2024-06-08']}
    print(f"{'pool':<14}{'N':>4}{'sd(t)':>8}{'sqrt(2lnN)':>12}{'E[max t] meas':>15}{'ratio':>8}")
    for k,v in pools.items():
        ts=[r['metrics']['sharpeRatio']*math.sqrt(_years(r)) for r in v]
        N=len(ts); sdt=st.stdev(ts); ap=math.sqrt(2*math.log(N)); me=expected_max_sr(N,sdt)
        print(f"  {k:<12}{N:>4}{sdt:>8.3f}{ap:>12.3f}{me:>15.3f}{me/ap:>7.2f}x")
    best=max(r['metrics']['sharpeRatio']*math.sqrt(_years(r)) for r in recs)
    print(f"\n  best observed implied t = {best:.3f}")
    for sdt,lab in ((1.365,'H1 trimmed'),(1.218,'all trimmed')):
        lo,hi=1.0001,1e6
        for _ in range(200):
            mid=math.sqrt(lo*hi); (lo,hi)=(mid,hi) if expected_max_sr(mid,sdt)<best else (lo,mid)
        print(f"  measured sd(t)={sdt} ({lab}): clears only if N_eff <= {lo:.2f}")
    print(f"  sqrt(2 ln N) approximation:      clears only if N_eff <= {math.exp(best**2/2):.2f}")
    print("\n  E[max t] by N_eff (measured sd(t)=1.218 vs approximation):")
    for n in (8,12,50,73):
        print(f"    N_eff={n:<4} measured {expected_max_sr(n,1.218):.3f}   sqrt(2lnN) {math.sqrt(2*math.log(n)):.3f}")
    top=sorted(recs,key=lambda r:-r['metrics']['sharpeRatio'])[:10]
    print(f"\n  OBV members in the top ten by Sharpe: {sum(1 for r in top if 'obv' in r['id'])} of 10")
    print(f"  full OBV roster: {sorted({r['id'].split('-')[0][:8] for r in recs if 'obv' in r['id']})}")
