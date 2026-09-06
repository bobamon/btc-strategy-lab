from math import lgamma, exp, log

def lbinom(n,k): return lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)
def binom_sf(k,n,p):                      # P(W >= k), exact in log space
    if k<=0: return 1.0
    if k>n: return 0.0
    return sum(exp(lbinom(n,i)+i*log(p)+(n-i)*log(1-p)) for i in range(k,n+1))
def kmin_pf_gt1(n,b):                     # fewest wins giving PF>1
    we=n/(1.0+b)
    k=int(we)+1
    while (k*b)/(n-k) <= 1.0: k+=1
    return k
def p_for_pf(pf_,b): return pf_/(pf_+b)   # win rate implying a given true PF

print("=== 1. SIZE of the pre-registered accept rule 'PF > 1.0', when the TRUE PF is exactly 1.0 ===")
print("  b |   n   | wins needed | P(passes | ZERO edge)")
for b in (1,2,3,4):
    for n in (30,100,400,2000):
        k=kmin_pf_gt1(n,b)
        print(f" {b}  |{n:6d} |    {k:5d}    |      {binom_sf(k,n,p_for_pf(1.0,b)):.4f}")
    print()

print("=== 2. What PF threshold at n=100 would give a real 5% false-positive rate? ===")
print("  b | wins needed for 5% | that corresponds to PF >=")
for b in (1,2,3,4):
    p0=p_for_pf(1.0,b); n=100
    k=next(k for k in range(n+1) if binom_sf(k,n,p0)<=0.05)
    print(f" {b}  |        {k:4d}        |        {(k*b)/(n-k):.3f}")

print("\n=== 3. POWER at n=100, testing at a real 5% level, if the method's TRUE PF were... ===")
print("  b | true PF 1.3 | 1.5 | 2.0")
for b in (1,2,3,4):
    p0=p_for_pf(1.0,b); n=100
    k=next(k for k in range(n+1) if binom_sf(k,n,p0)<=0.05)
    row=[binom_sf(k,n,p_for_pf(t,b)) for t in (1.3,1.5,2.0)]
    print(f" {b}  |    {row[0]:.3f}    | {row[1]:.3f} | {row[2]:.3f}")

print("\n=== 4. n needed for 80% power at a real 5% level ===")
print("  b | true PF 1.3 | true PF 1.5 | true PF 2.0")
for b in (1,2,3,4):
    p0=p_for_pf(1.0,b); out=[]
    for t in (1.3,1.5,2.0):
        pa=p_for_pf(t,b); n=10
        while n<40000:
            k=next((k for k in range(n+1) if binom_sf(k,n,p0)<=0.05), None)
            if k is not None and binom_sf(k,n,pa)>=0.80: break
            n+=5
        out.append(n)
    print(f" {b}  |    {out[0]:6d}   |   {out[1]:6d}    |   {out[2]:6d}")
