# 06. Next steps and open items

## Agreed next steps (in order)
1. **Policy intake:** a template the user can paste a bank's real policy into, a converter into `risk-platform/packs/<bank>/` YAML, and an automatic tighten-only check against the regulator pack. This gets the platform ready for the bank policies the user will supply.
2. **Write the run-2 research summary** (`research.md` in the finance houses / SME / corporate run). The digests are already there.
3. **Light public-rules research** (~2 researchers each), ideally in a fresh session:
   - collections and recovery;
   - trade finance (guarantees, letters of credit, ICC rules);
   - Islamic corporate (CBUAE / AAOIFI);
   - financial-crime screening inputs (sanctions, adverse media).
4. **Risk appetite step** (Faisal's step 4): bad-loan target scenarios (1% vs 2% NPL) using the stress engine.
5. **Organs:** a real default model (US mortgages on Freddie Mac / Fannie Mae data), fuller regulator packs, and the UI.

## Open checks ("verify")
- US card late-fee safe harbor (disputed); SR 26-2 scope for AI models.
- HSBC UK and Barclays mortgage maximum age; UAE minimum-salary removal (press-reported only); UAE real-estate exposure cap.
- Open the master-rulebook xlsx once in Excel to confirm the formula labels calculate.

## Open sign-offs from the policy packs
See `HANDOFF.md` §6:
- Islamic [A] items.
- Conventional conversions.
- 26 finance-company sign-offs and 3 validator flags:
  1. no CBUAE no-objection letters on file;
  2. salary-advance minimum;
  3. the AED 3m home cap vs the AED 1m individual cap.

## Coverage gaps (honest list)
- **Covered well:** retail. **Covered partly:** finance houses, and SME/corporate *rules*.
- **Not covered yet:**
  - collections and recovery;
  - SME and corporate *bank policies* (to be supplied by the bank);
  - trade finance;
  - Islamic corporate;
  - risk appetite and pricing;
  - financial-crime inputs;
  - market, liquidity, operational and vendor risk engines (listed in `risk-platform/config/risk_register.yaml`).

## People actions
- Faisal to review the retail outputs.
- Send the Tanveer update.
- Hire experts (credit risk/policy, compliance).
