from math import lgamma, exp, log

def lb(n, k): return lgamma(n+1) - lgamma(k+1) - lgamma(n-k+1)
def sf(k, n, p):
    if k <= 0: return 1.0
    if k > n: return 0.0
    return sum(exp(lb(n, i) + i*log(p) + (n-i)*log(1-p)) for i in range(k, n+1))
def p_for(pf, b): return pf/(pf+b)
def crit(n, b, alpha=0.05):
    p0 = p_for(1.0, b)
    return next(k for k in range(n+1) if sf(k, n, p0) <= alpha)

print("=== MINIMUM DETECTABLE EDGE: the smallest TRUE profit factor that n=100 can")
print("    detect with 80% power at a real 5% level ===")
print("  payoff b | smallest true PF detectable at n=100")
for b in (1, 2, 3, 4):
    k = crit(100, b)
    pf = 1.0
    while pf < 12.0:
        if sf(k, 100, p_for(pf, b)) >= 0.80: break
        pf += 0.01
    print(f"     {b}     |              {pf:.2f}")

# Protocol's own timeline table: sessions = trades / rate; ~21 NY sessions per month.
print("\n=== CALENDAR COST, on the protocol's OWN timeline assumptions ===")
print("    (his 2-trade/day cap; 21 New York sessions per month)")
print("  target        | trades | @1.0 trade/day | @0.5 trade/day")
rows = [("as pre-registered (n=100)", 100),
        ("80% power vs true PF 2.0 ", 65),
        ("80% power vs true PF 1.5 ", 190),
        ("80% power vs true PF 1.3 ", 460)]
for name, n in rows:
    a = n/1.0/21; b_ = n/0.5/21
    print(f"  {name} | {n:6d} |   {a:5.1f} months  |   {b_:5.1f} months ({b_/12:.1f} yr)")
