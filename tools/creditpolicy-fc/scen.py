def pmt(P, r, n):
    i = r/12
    return P*i/(1-(1+i)**-n)
def flat_inst(P, fr, n):
    return P*(1+fr*n/12)/n
def flat_to_apr(fr, n):
    # solve reducing rate with same instalment
    P=1000; inst=flat_inst(P,fr,n); lo,hi=0.0001,1.0
    for _ in range(200):
        mid=(lo+hi)/2
        if pmt(P,mid,n)>inst: hi=mid
        else: lo=mid
    return mid
print("S1 Mariam 60k 48m")
for r in (0.1799,0.20,0.24,0.28,0.3999):
    p=pmt(60000,r,48); print(f"  {r:.4f} inst {p:,.0f} total int {p*48-60000:,.0f}  DBR {(p+500)/6500:.1%}")
print("  max 20x", 20*6500)
print("S3 Khalid buyout 120k 36m left")
old=pmt(120000,0.28,36); print(f"  old inst {old:,.0f} remaining paid {old*36:,.0f} interest {old*36-120000:,.0f}")
es=1200*1.05; P=120000+es
for r in (0.1399,0.0549):
    n=pmt(P,r,36); print(f"  new {r} P {P:,.0f} inst {n:,.0f} total {n*36:,.0f} saving vs old {old*36-n*36:,.0f} monthly saving {old-n:,.0f} DBR {n/18000:.1%}")
print("S4 Fatima gold 100k")
for (P,r) in ((70000,0.1499),(70000,0.16),(75000,0.16)):
    n=pmt(P,r,24); print(f"  P {P} r {r} inst {n:,.0f} int {n*24-P:,.0f}")
print("  call drop %.1f%% sale drop %.1f%%"%((1-0.70/0.80)*100,(1-0.70/0.85)*100))
print("  FH 75 -> call at 80: drop %.1f%%"%((1-0.75/0.80)*100))
print("S5 Arjun auto")
for fr in (0.0449,0.0349,0.0599,0.0250,0.0290,0.0215):
    i=flat_inst(36000,fr,48); print(f"  flat {fr} inst {i:,.0f} total int {i*48-36000:,.0f} reducing~ {flat_to_apr(fr,48):.2%}")
print("  DBR", flat_inst(36000,0.0449,48)/5000)
for fr,n in ((0.0349,60),(0.0599,60),(0.0449,60)):
    print("  apr",fr,n,f"{flat_to_apr(fr,n):.2%}")
print("S2 Ravi")
print("  50% net", 0.5*3500, "fee 60+VAT", 63, "pct", 63/1500, "easyCredit", 1500*0.08*1.05, " APR simple", 60/1500*12)
print("S6 Sara DBR")
inc=9000; pl=3200; cards=20000*0.05; bnpl=600
print("  before new loan with bnpl", (pl+cards+bnpl)/inc, " without bnpl", (pl+cards)/inc)
print("  headroom without bnpl", 0.5*inc-(pl+cards), "loan possible at 21.49%/48m", (0.5*inc-(pl+cards))*(1-(1+0.2149/12)**-48)/(0.2149/12))
