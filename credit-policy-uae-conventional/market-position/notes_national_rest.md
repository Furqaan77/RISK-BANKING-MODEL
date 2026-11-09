# Remaining UAE National Banks: Research Notes (checked 2026-11-09)

The data is in `banks_national_rest.csv`.

**Confidence grades:**
- **H:** bank page or KFS.
- **M:** search extract (cbd.ae, sib.ae and investbank.ae block fetching), a pre-2025 official document, or results reported in the press.
- **L:** aggregator.

Rates are reducing balance unless the field says flat.

## Not included in the product comparison
- Emirates Investment Bank: private bank, bespoke credit only.
- Zand: no retail lending (corporate, SME and wealth only).
- Emirates Development Bank: government housing finance for nationals only.
- Mal: in-principle approval only (May 2026); not launched.

## CSV conventions
- **`nonstl_offered`:** Y = personal loan available without salary transfer; P = only auto, home or cards without salary transfer; N = none found.
- **Proxy rates where no reducing range is published:**
  - SIB: KFS example (2.89% flat ≈ 5.33%).
  - Al Hilal: converted from 3.10–5.80% flat.
  - Ajman: aggregator figures.
- **CBD auto rate:** this is the CBD Islami figure.
- **Aggregator (L) values:**
  - NBF: STL minimum salary and card minimum salary.
  - Al Hilal: STL and non-STL minimum salaries.
  - UAB: STL minimum salary and auto terms.
  - Al Masraf: several fields (STL minimum salary, ages, home terms, auto terms).
  - Card minimum salaries at CBI, Ajman, SIB, Invest Bank and Ruya.

## Notable facts
- CBD non-STL: Quick/Digi loan for expats only, at AED 10k salary with a maximum of AED 150k.
- Personal loans without salary transfer are NOT offered by NBF, NBQ, Invest, CBI, Al Masraf, Ruya or Mbank. NBQ and CBI offer them for auto loans or cards only.
- High personal-loan entry salaries: CBI and Al Masraf AED 15,000; Wio and Mbank 10,000; CBD 8,000; UAB and Reem 7,500; NBQ 7,000 nationals / 10,000 expats.
- Low card rates: NBQ 2.49% per month; NBF 2.99%; Mbank 3.15%.
- Wio personal loan: AED 10k with or without STL, maximum AED 1m, 4.75–18%.

## Data conflicts
| Bank | Conflict |
|---|---|
| CBD | Personal loan max for nationals: 2.5m (KFS) vs 3m (aggregators) |
| CBI | Home loan minimum salary: 10k (KFS) vs 15k/20k (product page); max 20m vs 15m |
| Al Masraf | KFS example rate (5.99%) is below the stated floor (6.49%) |
| Wio | Rate floor: 4.75% (Sep-26) vs 5.25% (Aug-25 KFS) |
| Ruya | Rate: product page from ~5.49% vs KFS 5.90% |
| UAB | KFS allows non-STL loans; the FAQ says STL is mandatory |
| SIB | Deposit advance: 90% vs 70% |
| Ajman | Card minimum payment: 5% now (3% in older material) |

## Gaps
- No numeric AECB floors are published by any of these banks.
- No retail loan splits, except Mbank (AED 0.68bn).
- No published rate range for:
  - Ajman, Mbank: personal finance
  - Al Hilal, Ajman: home finance
  - CBD, NBQ: auto
