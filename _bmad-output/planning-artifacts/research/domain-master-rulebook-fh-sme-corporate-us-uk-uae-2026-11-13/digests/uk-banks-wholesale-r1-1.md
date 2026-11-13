# UK banks: SME and corporate lending disclosures (digest r1-1)

Scope: HSBC UK, Barclays (UK Business Banking + UK Corporate Bank), Lloyds Banking Group (Business & Commercial Banking), NatWest (Business Banking / Commercial & Institutional).
Accessed: 2026-11-13. Status: COMPLETE (round 1). Parts A-D first, then per-bank evidence notes.

Rules used: only values found in the banks' own documents (or the British Business Bank for scheme data). Gaps say "not published" or "not found". "Computed" means we divided two published numbers ourselves. No bank publishes its internal corporate credit policy; this digest reports only what is disclosed.

Plain-language key (for new risk staff):
- **Stage 2** = loans whose risk has risen noticeably since they were made (not yet in default). **Stage 3** = loans in default / credit-impaired.
- **Cost of risk** = yearly impairment charge as % of loans. **LTV** = loan-to-value (loan size / property value).
- **FINREP** = a standard regulatory reporting template. Its "SME" and "non-financial corporations" lines use regulatory definitions, so they do not match each bank's own business divisions.

**Read with care:** the four banks define "SME" and "corporate" differently. Do not compare the columns across banks as if they were like-for-like. Each cell names its basis in Part B.

## Part A: Summary table (CSV)

```csv
bank,sme_loans_bn,corp_loans_bn,sme_loan_min,sme_loan_max,sme_rep_apr,sme_term_max_y,security_threshold,cre_pct,top_sector_1,top_sector_1_pct,stage2_pct,stage3_pct,cost_of_risk_pct,cre_ltv_gt70_pct,period,confidence,key_source_url
HSBC UK,7.11 (FINREP SMEs),71.48 (FINREP non-financial corporations),1000,25000,11.3 (<=10k) / 8.6 (>10k),10,"Security may be required, case by case; no threshold or personal-guarantee rule published",17.7 (real estate activities / NFC loans),Real estate activities,17.7,13.6 (NFC),3.2 (NFC),0.23 (computed; whole UK segment incl. retail; FY2025; USD basis),not published,"30 Jun 2026 (Pillar 3); FY2025 (cost of risk); product page as accessed",M,https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2026/interim/pdfs/hsbc-uk-bank-plc/260810-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-june-2026.pdf
Barclays,17.6 (Business Banking segment),33.0 (UK Corporate Bank),1000,25000,11.2 overall (14.9 / 11.2 / 8.5 by band),10 (unsecured; up to 25 for loans >25k),"Unsecured up to GBP 25k (up to GBP 100k for existing customers); above GBP 100k a secured loan is required",47.0 (Barclays Bank UK PLC NFC loans only; excludes most of UKCB),Real estate activities,47.0,9.9 (UK corporate loans incl. Business Banking),2.5 (UK corporate loans incl. Business Banking),0.08 (UKCB loan loss rate 9M 2026); Business Banking net release,not published,"30 Sep 2026 (loans, staging, impairment); 31 Dec 2025 (sector)",M,https://www.investegate.co.uk/announcement/rns/barclays--barc/3rd-quarter-results/9835199
Lloyds Banking Group,29.8 (Business and Commercial Banking),69.7 (Corporate and Institutional Banking),1000,50000 (top of 11.2% APR band),11.2 (snippet only),not verified,not verified,10.4 (computed: UK Real Estate 10.1 / Commercial Banking 97.0; 30 Jun 2026),not published,not published,11.8 (BCB),3.4 (BCB),0.11 (computed; Commercial Banking; annualised 9M 2026),not published (average LTV 45%),"30 Sep 2026 (loans, staging); 30 Jun 2026 (CRE)",M,https://www.investegate.co.uk/announcement/rns/lloyds-banking-group--lloy/2026-q3-interim-management-statement/9846888
NatWest Group,25.65 (FINREP SMEs; 31 Dec 2025),170.4 (Commercial & Institutional net loans),1000,100000,8.2 (L; calculator example; see Part C),7,"Personal, director or member's guarantee may be required; no threshold published",16.9 (CRE / group 'corporate and other' loans),Commercial real estate,16.9,14.3 (C&I),1.0 (C&I),0.19 (C&I loan impairment rate Q3 2026),5.1,"30 Sep 2026 (loans, staging, sector); 30 Jun 2026 (CRE LTV); 31 Dec 2025 (FINREP SMEs)",H,https://www.investegate.co.uk/announcement/rns/natwest-group--nwg/natwest-group-q3-2026-interim-management-statement/9849208
```

Growth Guarantee Scheme (British Business Bank, drawn value to 30 Jun 2026): HSBC UK GBP 550.83m / 1,566 facilities; Barclays Bank GBP 212.05m / 455; Lloyds Bank GBP 139.44m / 510 (plus Bank of Scotland GBP 12.03m / 30); NatWest Group GBP 130.19m / 541. All four take part.

## Part B: Claims list

Format: {claim | source URL | publisher | pub_date | accessed | confidence | class}

HSBC UK
1. {Small business loan GBP 1,000-25,000; term 12 months-10 years; fixed; rep APR 11.3% (<=GBP 10k) and 8.6% (>GBP 10k); no arrangement fee | https://www.business.hsbc.uk/en-gb/products/small-business-loan | HSBC UK | not dated (live page) | 2026-11-13 | H | product-term}
2. {"Security may be required - each case is considered on its individual merits"; no personal-guarantee wording; early repayment deducts 1 month + 28 days' interest | same as 1 | HSBC UK | live page | 2026-11-13 | H | product-term}
3. {Loans to non-financial corporations GBP 71.48bn gross at 30 Jun 2026; Stage 2 9.70bn (13.6%), Stage 3 2.28bn (3.2%) | https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2026/interim/pdfs/hsbc-uk-bank-plc/260810-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-june-2026.pdf (Table 12) | HSBC UK Bank plc | 2026-08-10 | 2026-11-13 | H | asset-quality}
4. {FINREP SMEs GBP 7.11bn; Stage 2 1.24bn (17.4%), Stage 3 0.45bn (6.4%) at 30 Jun 2026 | same as 3 | HSBC UK Bank plc | 2026-08-10 | 2026-11-13 | H | loan-book / asset-quality}
5. {NFC loans by industry (GBP 73.76bn): real estate 13.03bn (17.7%), wholesale and retail 11.41bn (15.5%), manufacturing 9.47bn (12.8%) | same as 3 (Table 18, CQ5) | HSBC UK Bank plc | 2026-08-10 | 2026-11-13 | H | sector}
6. {Credit granted "on the basis of capacity to repay, rather than placing primary reliance on credit risk mitigants ... facilities may be provided unsecured" | same as 3 (p.22) | HSBC UK Bank plc | 2026-08-10 | 2026-11-13 | H | risk-appetite}
7. {UK segment 2025: net customer loans USD 303.7bn; change in ECL USD 696m (computed 0.23%) | https://www.investegate.co.uk/announcement/rns/hsbc-holdings--hsba/hsbc-holdings-2025-results/9445238 | HSBC Holdings plc | 2026-02-25 | 2026-11-13 | M (computed; segment includes retail) | cost-of-risk}
8. {HSBC UK Bank Plc GGS drawn GBP 550.83m, 1,566 facilities | https://www.british-business-bank.co.uk/about/research-and-publications/ggs-including-rls-iteration-3-performance-data-30-june-2026 | British Business Bank | 2026 (data to 30 Jun 2026) | 2026-11-13 | H | scheme}

Barclays
9. {Business Banking serves SMEs with < GBP 6.5m annual revenue; UKCB serves > GBP 6.5m to FTSE 350, about 13,000 clients | https://www.investegate.co.uk/announcement/rns/barclays--barc/3rd-quarter-results/9835199 | Barclays PLC | 2026-10-22 | 2026-11-13 | H | segment-definition}
10. {Business Banking loans GBP 17.6bn; UKCB loans GBP 33.0bn at 30 Sep 2026 (Dec 2025: 17.9bn and 30.0bn) | same as 9 | Barclays PLC | 2026-10-22 | 2026-11-13 | H | loan-book}
11. {UK corporate loans GBP 64.9bn gross: Stage 2 6.39bn (9.9%), Stage 3 1.62bn (2.5%) at 30 Sep 2026 | same as 9 | Barclays PLC | 2026-10-22 | 2026-11-13 | H | asset-quality}
12. {Business Banking gross GBP 12.5bn: Stage 2 1.7bn (13.6%), Stage 3 0.7bn (5.6%), allowance GBP 280m | same as 9 (footnote) | Barclays PLC | 2026-10-22 | 2026-11-13 | H | asset-quality}
13. {9M 2026 impairment: Business Banking net release GBP 18m; UKCB charge GBP 21m, loan loss rate 8 bps | same as 9 | Barclays PLC | 2026-10-22 | 2026-11-13 | H | cost-of-risk}
14. {Barclays Bank UK PLC NFC loans GBP 16.55bn (Stage 2 2.42bn, Stage 3 0.80bn); FINREP SMEs 11.32bn (Stage 2 19.7%, Stage 3 7.0%) at 31 Dec 2025 | https://home.barclays/content/dam/home-barclays/documents/investor-relations/ResultAnnouncements/FullYear2025Results/FY25-BBUKPLC-Pillar-3.pdf (Table 38) | Barclays Bank UK PLC | 2026-02-10 | 2026-11-13 | H | asset-quality}
15. {Barclays Bank UK PLC NFC loans by industry (GBP 17.35bn): real estate 8.16bn (47.0%), agriculture 3.17bn (18.3%) | same as 14 (Table 45, CQ5) | Barclays Bank UK PLC | 2026-02-10 | 2026-11-13 | H (value) / M (as a proxy for all Barclays UK business lending) | sector}
16. {Risk appetite = acceptable deterioration in profit after tax, CET1 % and a liquidity constraint under a severe but plausible internal stress; enforced by stress loss limits and mandate-and-scale limits | same as 14 (p.84-85) | Barclays Bank UK PLC | 2026-02-10 | 2026-11-13 | H | risk-appetite}
17. {"The Group implements limits on concentrations in order to mitigate the risk." (no numbers) | https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2025/Barclays-PLC-Annual-Report-2025.pdf (p.294) | Barclays PLC | 2026-02-10 | 2026-11-13 | H | risk-appetite}
18. {Unsecured small business loan GBP 1,000-25,000, 1-10 years, fixed; rep APR 11.2% overall (14.9% / 11.2% / 8.5% by band); loans > GBP 100k must be secured; larger loans up to 25 years and up to GBP 25m | https://www.barclays.co.uk/business-banking/borrow/loans/ | Barclays Bank UK PLC | live page | 2026-11-13 | H | product-term}
19. {Barclays Bank Plc GGS drawn GBP 212.05m, 455 facilities | BBB URL as in 8 | British Business Bank | data to 30 Jun 2026 | 2026-11-13 | H | scheme}

Lloyds Banking Group
20. {BCB loans GBP 29.8bn; CIB GBP 69.7bn at 30 Sep 2026 (comparatives re-presented after client migration CIB -> BCB) | https://www.investegate.co.uk/announcement/rns/lloyds-banking-group--lloy/2026-q3-interim-management-statement/9846888 | Lloyds Banking Group plc | 2026-10 (Q3 IMS) | 2026-11-13 | H | loan-book}
21. {BCB gross GBP 30.13bn: Stage 2 11.8%, Stage 3 3.4%; CIB Stage 2 2.9%, Stage 3 1.0%; Commercial Banking Stage 2 5.6%, Stage 3 1.7% at 30 Sep 2026 | same as 20 | Lloyds Banking Group plc | 2026-10 | 2026-11-13 | H | asset-quality}
22. {Commercial Banking impairment 9M 2026: GBP 81m pre-MES + GBP 4m MES (computed annualised about 0.11%) | same as 20 | Lloyds Banking Group plc | 2026-10 | 2026-11-13 | M (computed) | cost-of-risk}
23. {UK Real Estate committed drawn lending GBP 10.1bn (net of GBP 2.2bn SRT-protected); average LTV 45% | https://www.investegate.co.uk/announcement/rns/lloyds-banking-group--lloy/2026-half-year-results/9694683 | Lloyds Banking Group plc | 2026-07-30 (approx.) | 2026-11-13 | H | sector}
24. {"Sector and product risk parameters help to manage the Group's exposure to higher risk and cyclical sectors, segments and asset classes" | same as 23 | Lloyds Banking Group plc | 2026-07 | 2026-11-13 | H | risk-appetite}
25. {Commercial Banking net impairment charge FY2025 GBP 60m (2024 credit GBP 14m); UK Real Estate GBP 10.0bn at Dec 2025 | https://www.investegate.co.uk/announcement/rns/lloyds-banking-group--lloy/2025-results-/9392603 | Lloyds Banking Group plc | 2026-01-29 | 2026-11-13 | H | cost-of-risk / sector}
26. {Business loan fixed 11.2% rep APR on GBP 1,000-50,000; APR above GBP 50k on application | https://www.lloydsbank.com/business/business-loans.html (search snippet; page blocked automated fetch) | Lloyds Bank plc | live page | 2026-11-13 | M | product-term}
27. {Lloyds Bank Plc GGS drawn GBP 139.44m (510); Bank of Scotland GBP 12.03m (30) | BBB URL as in 8 | British Business Bank | data to 30 Jun 2026 | 2026-11-13 | H | scheme}

NatWest Group
28. {C&I net loans GBP 170.4bn at 30 Sep 2026 (Dec 2025 154.2bn) | https://www.investegate.co.uk/announcement/rns/natwest-group--nwg/natwest-group-q3-2026-interim-management-statement/9849208 | NatWest Group plc | 2026-10 (Q3 IMS) | 2026-11-13 | H | loan-book}
29. {C&I gross GBP 176.75bn: Stage 2 25.27bn (14.3%), Stage 3 1.77bn (1.0%); Stage 3 coverage 48.87% | same as 28 | NatWest Group plc | 2026-10 | 2026-11-13 | H | asset-quality}
30. {C&I loan impairment rate 19 bps in Q3 2026; charge GBP 80m (H1 2026 GBP 137m); group 21 bps YTD | same as 28 and https://www.investegate.co.uk/announcement/rns/natwest-group--nwg/natwest-group-plc-interim-results-2026-part-1/9697081 | NatWest Group plc | 2026-10 / 2026-07 | 2026-11-13 | H | cost-of-risk}
31. {CRE GBP 21.31bn = 16.9% of 'corporate and other' loans; mobility and logistics 14.4%; consumer industries 13.0% | same as 28 (sector analysis) | NatWest Group plc | 2026-10 | 2026-11-13 | H (values) / M (computed shares) | sector}
32. {CRE investment loans with LTVs GBP 14.24bn: >70-100% 0.51bn, >100% 0.21bn => 5.1% above 70% LTV; average LTV 49% | https://www.investegate.co.uk/announcement/rns/natwest-group--nwg/natwest-group-plc-interim-results-2026-part-1/9697081 | NatWest Group plc | 2026-07 | 2026-11-13 | H | sector / CRE-LTV}
33. {FINREP 31 Dec 2025: NFC GBP 111.48bn (Stage 2 15.8%, Stage 3 1.6%); SMEs GBP 25.65bn (Stage 2 19.4%, Stage 3 3.2%); real estate activities 26.5% of NFC | https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwg-pillar-3-report.pdf (p.70-72) | NatWest Group plc | 2026-02-13 | 2026-11-13 | H | asset-quality / sector}
34. {Non-Personal risk appetite manages concentrations across "single name, sector, country and product and asset classes", backed by "transactional acceptance standards" | same as 33 (p.75) | NatWest Group plc | 2026-02-13 | 2026-11-13 | H | risk-appetite}
35. {Small Business Loan GBP 1,000-100,000; fixed; 1-7 years; no set-up or early repayment fees; "A personal, director or member's guarantee may be required" | https://www.natwest.com/business/loans-and-finance/small-business-loan.html | National Westminster Bank Plc | live page | 2026-11-13 | H | product-term}
36. {NatWest Group plc GGS drawn GBP 130.19m, 541 facilities | BBB URL as in 8 | British Business Bank | data to 30 Jun 2026 | 2026-11-13 | H | scheme}

## Part C: Conflicts and comparability warnings

1. **"SME" means different things.** HSBC UK FINREP SMEs GBP 7.1bn; Barclays Bank UK PLC FINREP SMEs GBP 11.3bn; NatWest FINREP SMEs GBP 25.6bn. Divisions are bigger: Barclays Business Banking GBP 17.6bn, Lloyds BCB GBP 29.8bn. Use the division numbers for book size and FINREP only for staging ratios.
2. **Barclays Business Banking has three sizes.** It is GBP 17.6bn (segment loans at amortised cost, 30 Sep 2026), GBP 12.5bn (gross exposure in the wholesale impairment table footnote, same date) and GBP 11.3bn (FINREP SMEs in Barclays Bank UK PLC, Dec 2025). Barclays does not reconcile them. The likely causes are scope differences, such as government-scheme loans and products booked outside the wholesale table. Not verified.
3. **Barclays CRE share (47%) is entity-only.** It covers Barclays Bank UK PLC non-financial-corporate loans, which are mostly Business Banking. It leaves out most of UKCB, so it overstates CRE for "Barclays UK business lending". The group-wide industry table has no separate real estate line; real estate sits inside "Materials and Building".
4. **Lloyds BCB re-presented.** H1 2026 RNS: BCB GBP 29.1bn at 30 Jun 2026. Q3 2026 IMS shows 30 Jun 2026 as GBP 29.6bn after moving clients from CIB into BCB. Use the Q3 basis.
5. **NatWest CRE share depends on the definition.** It is 16.9% using the bank's own "commercial real estate" of "corporate and other" loans (Sep 2026), and 26.5% using FINREP "real estate activities" of non-financial-corporate loans (Dec 2025). The two use different industry codes and dates; NatWest does not reconcile them (the reason for the gap is not verified).
6. **NatWest representative APR is uncertain.** The captured calculator shows "GBP 7,500 ... 8.2% ... GBP 137.55 ... GBP 8,253.00". But GBP 137.55 x 60 months = GBP 8,253, which implies about 3.8% APR, not 8.2%. The labels could not be matched reliably. Third-party sites quote 12.24% and other figures, which we did not use. Check on the live page.
7. **HSBC APR.** Third-party sites quote one 7.1% representative APR. HSBC's own page shows 11.3% (<= GBP 10k) and 8.6% (> GBP 10k). We used the bank page.
8. **Lloyds product terms.** Third-party sites disagree on the turnover cap (GBP 3m vs GBP 25m) and the term (up to 10 vs 25 years). We used none of them. The bank page could not be fetched.
9. **Stage 2 / Stage 3 are not like-for-like.** HSBC and NatWest (FINREP) are non-financial-corporate totals. Barclays is "UK corporate loans" including Business Banking. Lloyds is a division (BCB). The Stage 2 ratio also depends on each bank's own significant-increase-in-credit-risk triggers.
10. **Cost of risk bases differ.** HSBC: whole UK segment including mortgages, USD, FY2025, computed. Barclays: UKCB 9M 2026 loan loss rate. Lloyds: Commercial Banking, annualised 9M 2026, computed. NatWest: C&I Q3 2026 quarter rate. Treat all four as indicative only.

## Part D: Not found / not published

- **All four banks:** numeric sector concentration limits, single-name limits, maximum LTV rules for CRE, and internal credit policy. Banks describe frameworks only.
- **All four banks:** a published minimum trading history for small business loans. NatWest and Barclays only ask for trading information at application.
- **HSBC UK:** Business Banking / Commercial Banking loan book in GBP (HSBC UK Bank plc Annual Report 2025 and Interim Report 2026 PDFs could not be retrieved); CRE LTV bands; GBP cost of risk for business lending; personal-guarantee rule.
- **Barclays:** CRE LTV bands (share above 70% LTV) for UK business lending; personal-guarantee rule; separate UKCB staging.
- **Lloyds:** sector breakdown of Commercial Banking (top sectors); CRE LTV bands; product term, security threshold and guarantee rule from the bank's own page. The site blocked automated access, and the 2025 Annual Report / Pillar 3 PDFs could not be downloaded.
- **NatWest:** separate Business Banking loan balance; a reliable representative APR (see Part C-6).
- **Next step if needed:** pull the HSBC UK Bank plc Annual Report 2025, the Lloyds Banking Group Annual Report 2025 / Pillar 3 (CQ5 table) and the Barclays PLC Pillar 3 2025 by hand (browser download) to fill the Lloyds sector mix and the HSBC/Barclays CRE LTV gaps.

---

# Evidence notes per bank (working notes, kept for audit)

---

## Bank 1: HSBC UK Bank plc (ring-fenced bank)

Sources used:
- S1 HSBC UK small business loan page: https://www.business.hsbc.uk/en-gb/products/small-business-loan
- S2 HSBC UK Bank plc Pillar 3 Disclosures at 30 June 2026 (pub 2026-08-10): https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2026/interim/pdfs/hsbc-uk-bank-plc/260810-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-june-2026.pdf
- S3 HSBC Holdings plc 2025 Results (RNS, 2026-02-25), UK segment table: https://www.investegate.co.uk/announcement/rns/hsbc-holdings--hsba/hsbc-holdings-2025-results/9445238
- S4 British Business Bank, GGS (incl. RLS iteration 3) performance data to 30 June 2026: https://www.british-business-bank.co.uk/about/research-and-publications/ggs-including-rls-iteration-3-performance-data-30-june-2026
- S5 HSBC UK Bank plc Pillar 3 at 30 September 2026 (pub 2026-11-03), checked: capital/RWA only, no loan-quality tables: https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2026/3q/pdfs/hsbc-uk-bank-plc-ring-fenced-bank/261103-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2026.pdf

Key facts:
- Small business loan: GBP 1,000 to 25,000; term 12 months to 10 years; fixed rate; representative APR 11.3% (up to and incl. GBP 10,000) and 8.6% (over GBP 10,000); no arrangement fee; "Security may be required - each case is considered on its individual merits" (no stated threshold; personal guarantee not mentioned); early repayment deducts one month and 28 days' interest from the rebate. Minimum trading history: not stated (online eligibility checker only). [S1]
- Loans to non-financial corporations (FINREP CR1, gross): GBP 71.48bn at 30 Jun 2026 (Stage 1 61.78bn, Stage 2 9.70bn, Stage 3 2.28bn). At 31 Dec 2025: GBP 67.03bn (Stage 2 7.63bn, Stage 3 2.50bn). [S2, Table 12]
  - Computed: Stage 2 = 13.6% and Stage 3 = 3.2% at 30 Jun 2026 (Dec 2025: 11.4% and 3.7%).
- Of which SMEs (FINREP definition): GBP 7.11bn at 30 Jun 2026 (Stage 1 5.87bn, Stage 2 1.24bn, Stage 3 0.45bn). Computed: Stage 2 17.4%, Stage 3 6.4%. Dec 2025: 7.52bn. [S2, Table 12]
  - Caution: this FINREP "SME" line is much smaller than HSBC UK's Business Banking book as managed; it is a regulatory reporting definition, not the segment.
- Loans to non-financial corporations by industry (CQ5, gross, 30 Jun 2026, total GBP 73.76bn): real estate activities 13.03bn (computed 17.7%); wholesale and retail trade 11.41bn (15.5%); manufacturing 9.47bn (12.8%); accommodation and food 5.87bn (8.0%); administrative and support 5.41bn (7.3%); professional, scientific and technical 5.17bn (7.0%). Real estate non-performing GBP 209m (computed 1.6%). [S2, Table 18]
- Group UK segment 2025 (USD, includes all HSBC UK businesses): loans and advances to customers (net) USD 303.7bn; change in ECL USD 696m. Computed cost of risk about 0.23% of net loans. [S3]
- Risk mitigation stance: "Our approach to granting credit facilities is on the basis of capacity to repay, rather than placing primary reliance on credit risk mitigants. Depending on a customer's standing and the type of product, facilities may be provided unsecured." [S2, p.22]
- Growth Guarantee Scheme: HSBC UK Bank Plc is a GGS lender; drawn GBP 550.83m across 1,566 facilities (to 30 Jun 2026), the largest of the four banks here. [S4]
- Not found for HSBC UK: Business Banking / Commercial Banking loan book in GBP (the HSBC UK Bank plc Annual Report 2025 and Interim Report 2026 PDFs could not be retrieved); CRE LTV bands; published sector limits or risk appetite metrics; minimum trading history.

---

## Bank 2: Barclays (Barclays UK Business Banking + Barclays UK Corporate Bank)

Sources used:
- B1 Barclays PLC Q3 2026 Results Announcement (RNS "3rd Quarter Results", 2026-10-22): https://www.investegate.co.uk/announcement/rns/barclays--barc/3rd-quarter-results/9835199
- B2 Barclays Bank UK PLC Pillar 3 Report 2025 (pub 2026-02-10): https://home.barclays/content/dam/home-barclays/documents/investor-relations/ResultAnnouncements/FullYear2025Results/FY25-BBUKPLC-Pillar-3.pdf
- B3 Barclays PLC Annual Report 2025 (pub 2026-02-10), "Analysis of the concentration of credit risk" (p.294-295): https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2025/Barclays-PLC-Annual-Report-2025.pdf
- B4 Barclays business loans page: https://www.barclays.co.uk/business-banking/borrow/loans/
- S4 British Business Bank GGS performance data to 30 Jun 2026 (as for HSBC)

Key facts:
- Segment definitions: Business Banking (inside Barclays UK) serves SMEs "with less than GBP 6.5m in annual revenue"; UK Corporate Bank (UKCB) serves "clients with annual revenue greater than GBP 6.5m through to FTSE 350 companies", about 13,000 clients. [B1]
- Loan books at amortised cost, 30 Sep 2026: Business Banking GBP 17.6bn (Dec 2025 17.9bn; Sep 2025 18.2bn); UKCB GBP 33.0bn (Dec 2025 30.0bn); "UK Corporate Bank up 14%" year on year. [B1]
- Staging, 30 Sep 2026, "Corporate loans" in the UK (gross, includes Business Banking): GBP 64.9bn; Stage 1 56.88bn, Stage 2 6.39bn, Stage 3 1.62bn. Computed: Stage 2 9.9%, Stage 3 2.5%. Coverage on UK corporate loans excluding Business Banking 1.0%. [B1, staging table]
- Business Banking alone (footnote, 30 Sep 2026): gross GBP 12.5bn; Stage 1 10.1bn, Stage 2 1.7bn, Stage 3 0.7bn; allowance GBP 280m. Computed: Stage 2 13.6%, Stage 3 5.6%. (Dec 2025: gross 12.4bn; Stage 2 2.3bn, Stage 3 0.8bn.) [B1]
- Impairment / cost of risk, 9 months to 30 Sep 2026: Business Banking net release of GBP 18m (Q3 2026 release 12m); UKCB charge GBP 21m, loan loss rate 8 bps (Q325 YTD 16 bps). Group loan loss rate 43 bps in Q3 2026; group guidance "around the top of the 50-60bps through the cycle range". [B1]
- Barclays Bank UK PLC (ring-fenced bank; Business Banking sits here), 31 Dec 2025, FINREP CR1 gross: non-financial corporations GBP 16.55bn (Stage 2 2.42bn, Stage 3 0.80bn); of which SMEs GBP 11.32bn (Stage 2 2.23bn, Stage 3 0.80bn). Computed: SME Stage 2 19.7%, Stage 3 7.0%. [B2, Table 38]
- Sector mix, Barclays Bank UK PLC loans to non-financial corporations (CQ5, 31 Dec 2025, total GBP 17.35bn): real estate activities 8.16bn (computed 47.0%); agriculture, forestry and fishing 3.17bn (18.3%); wholesale and retail 1.27bn (7.3%); human health 0.97bn (5.6%). Book fell GBP 1.2bn in 2025 "primarily due to continued repayment of government scheme lending in Business Banking". [B2, Table 45]
  - Caution: this entity view excludes most of UKCB, so it overstates CRE share versus all Barclays UK business lending.
- Group-wide industry view (all of Barclays, incl. Investment Bank, net, 31 Dec 2025): "Materials and Building" GBP 23.85bn (no separate real estate line). Not usable as a UK SME CRE share. [B3]
- Risk appetite (published): Barclays Bank UK PLC Board expresses appetite "as the acceptable level of deterioration in a set of key financial parameters under a severe but plausible stress scenario" (2025 parameters: profit after tax, CET1 %, liquidity constraint); controlled by "stress loss limits" and "mandate and scale limits". The entity board "cannot approve a higher risk appetite than that determined by the Barclays PLC Board". Group text: "The Group implements limits on concentrations in order to mitigate the risk." No numeric sector limits published. [B2 p.80-85; B3 p.294]
- SME product terms [B4]: small business (unsecured) loan GBP 1,000 to 25,000; terms 1 to 10 years; fixed rate; overall representative APR 11.2% for GBP 1,000-25,000, banded 14.9% (1,000-5,000), 11.2% (5,001-15,000), 8.5% (15,001-25,000). Existing customers: "flexible borrowing options ... on amounts up to GBP 100,000. If you need to borrow more than GBP 100,000, you'll need to apply for a secured business loan instead." Larger loans from GBP 25,001 with terms up to 25 years, fixed or variable; overall range "from GBP 1,000 up to loans of GBP 25 million". Minimum trading history: not stated; personal guarantee: not stated.
- Growth Guarantee Scheme: Barclays Bank Plc drew GBP 212.05m across 455 GGS facilities to 30 Jun 2026; B4 page lists GGS in its menu. [S4, B4]
- Not found for Barclays: CRE LTV bands (share above 70% LTV) for UK business lending; minimum trading history; personal guarantee policy.

---

## Bank 3: Lloyds Banking Group (Business & Commercial Banking; Corporate & Institutional Banking)

Sources used:
- L1 Lloyds Banking Group 2026 Q3 Interim Management Statement (RNS, 2026-10-22 approx.): https://www.investegate.co.uk/announcement/rns/lloyds-banking-group--lloy/2026-q3-interim-management-statement/9846888
- L2 Lloyds Banking Group 2026 Half-Year Results (RNS, 2026-07-30 approx.): https://www.investegate.co.uk/announcement/rns/lloyds-banking-group--lloy/2026-half-year-results/9694683
- L3 Lloyds Banking Group 2025 Results (RNS, 2026-01-29): https://www.investegate.co.uk/announcement/rns/lloyds-banking-group--lloy/2025-results-/9392603
- L4 Lloyds Bank business loans page (could not be fetched: site returned an error page to automated tools; terms taken from search-engine snippet of the page only): https://www.lloydsbank.com/business/business-loans.html
- S4 British Business Bank GGS performance data to 30 Jun 2026

Key facts:
- Loan books (underlying loans and advances to customers), 30 Sep 2026: Business and Commercial Banking (BCB) GBP 29.8bn; Corporate and Institutional Banking (CIB) GBP 69.7bn. Q3 2026 comparatives were re-presented because "the Group migrated certain clients with a net movement from Corporate and Institutional Banking to Business and Commercial Banking". [L1]
- H1 2026 (before re-presentation): "Business and Commercial Banking lending increased marginally to GBP 29.1 billion (31 December 2025: GBP 28.7 billion) ... continued amortisation of the portfolio, particularly government-backed lending"; CIB lending GBP 67.9bn (Dec 2025 62.5bn). [L2]
- Staging, gross, 30 Sep 2026: BCB GBP 30.13bn, Stage 2 3.55bn (11.8%), Stage 3 1.03bn (3.4%); CIB GBP 70.21bn, Stage 2 2.9%, Stage 3 1.0%; Commercial Banking total GBP 100.34bn, Stage 2 5.6%, Stage 3 1.7%. BCB ECL allowance GBP 361m (coverage 1.2%; Stage 3 coverage 15.7%). Note: Stage 3 excludes GBP 201m of BCB loans in recoveries. [L1]
- Staging, 30 Jun 2026: BCB Stage 2 GBP 3,403m = 11.7% (Dec 2025 11.6%); Stage 3 GBP 987m = 3.4% (Dec 2025 3.4%). Commercial Banking Stage 2 5.9%, Stage 3 1.7% (Dec 2025 1.9%). [L2]
- Impairment: Commercial Banking underlying impairment, 9 months to 30 Sep 2026: pre-MES charge GBP 81m plus MES charge GBP 4m (computed total GBP 85m; computed annualised cost of risk about 0.11% of Commercial Banking gross loans). H1 2026 net charge GBP 51m (H1 2025: 100m). FY2025 net charge GBP 60m (2024: credit of 14m). Group asset quality ratio 25 bps (9M 2026). [L1, L2, L3]
- CRE: "Commercial Banking UK Real Estate committed drawn lending increased by net GBP 0.1 billion to GBP 10.1 billion in the first half of 2026 (net of GBP 2.2 billion exposures subject to protection through significant risk transfer (SRT) securitisations) ... The average LTV of 45% remains stable." Computed: about 10% of Commercial Banking lending (10.1 / 97.0bn at 30 Jun 2026). FY2025: GBP 10.0bn (net of GBP 2.6bn SRT protection). [L2, L3]
- Risk appetite (published wording, no numbers): "Sector, asset and product concentrations within the portfolios are closely monitored and controlled ... Sector and product risk parameters help to manage the Group's exposure to higher risk and cyclical sectors, segments and asset classes." Commercial Banking credit strategies operate "within established risk appetite"; "Early warning indicators and risk appetite metrics are actively monitored". [L2]
- SME product terms [L4, snippet only, confidence M]: fixed 11.2% representative APR on loans of GBP 1,000 to 50,000; APR for loans above GBP 50,000 given on application. Term, security threshold, personal guarantee and minimum trading history could not be verified on the bank's own page (third-party sites disagree on term and turnover limits; not used).
- Growth Guarantee Scheme: Lloyds Bank Plc drew GBP 139.44m across 510 facilities, plus Bank of Scotland plc GBP 12.03m across 30 facilities, to 30 Jun 2026. [S4]
- Not found for Lloyds: sector split of business lending (top sectors), CRE LTV bands (share above 70% LTV), numeric concentration limits. The Lloyds 2025 Annual Report and Pillar 3 PDFs could not be downloaded (site blocked automated access).

---

## Bank 4: NatWest Group (Commercial & Institutional, which includes Business Banking, Commercial Mid-market, Corporate & Institutions)

Sources used:
- N1 NatWest Group Q3 2026 Interim Management Statement (RNS, 2026-10): https://www.investegate.co.uk/announcement/rns/natwest-group--nwg/natwest-group-q3-2026-interim-management-statement/9849208
- N2 NatWest Group plc Interim Results 2026, part 1 (RNS, 2026-07): https://www.investegate.co.uk/announcement/rns/natwest-group--nwg/natwest-group-plc-interim-results-2026-part-1/9697081
- N3 NatWest Group plc Pillar 3 Report 2025 (pub 2026-02-13): https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwg-pillar-3-report.pdf
- N4 NatWest Small Business Loan page: https://www.natwest.com/business/loans-and-finance/small-business-loan.html
- S4 British Business Bank GGS performance data to 30 Jun 2026

Key facts:
- Loan book: Commercial & Institutional (C&I) net loans to customers (amortised cost) GBP 170.4bn at 30 Sep 2026 (30 Jun 2026 163.7bn; 31 Dec 2025 154.2bn). Business Banking is part of C&I; a separate Business Banking loan balance is not published in N1/N2. [N1]
- FINREP view, 31 Dec 2025 (UK CR1, gross): non-financial corporations GBP 111.48bn (performing 109.65bn incl. Stage 2 17.55bn; non-performing 1.84bn incl. Stage 3 1.82bn); of which SMEs GBP 25.65bn (performing 24.81bn incl. Stage 2 4.96bn; non-performing 0.84bn incl. Stage 3 0.83bn). Computed: NFC Stage 2 15.8%, Stage 3 1.6%; SME Stage 2 19.4%, Stage 3 3.2%. [N3 p.72]
- Staging by segment, 30 Sep 2026 (gross loans at amortised cost and FVOCI): C&I GBP 176.75bn; Stage 2 25.27bn; Stage 3 1.77bn. Computed: Stage 2 14.3%, Stage 3 1.0% (31 Dec 2025: 159.16bn; Stage 2 11.5%, Stage 3 1.3%). C&I ECL coverage 0.89%; Stage 3 coverage 48.87%. [N1]
- Impairment: C&I charge GBP 80m in Q3 2026 (Q2 43m), loan impairment rate 19 bps in Q3 2026 (Q2 10 bps; Q3 2025 14 bps); C&I H1 2026 charge GBP 137m (H1 2025 154m). Group loan impairment rate 21 bps year to date. C&I post-model adjustment for economic uncertainty GBP 189m (Dec 2025 149m), linked to "the Middle East conflict including second order impacts for sectors considered most vulnerable". [N1, N2]
- Sector concentration (group "Corporate and other" loans, 30 Sep 2026, gross GBP 126.08bn): commercial real estate GBP 21.31bn (computed 16.9%; Stage 2 1.41bn, Stage 3 0.29bn); mobility and logistics GBP 18.21bn (14.4%); consumer industries GBP 16.42bn (13.0%). [N1 sector analysis]
- FINREP industry view, 31 Dec 2025 (UK CQ5, loans to non-financial corporations GBP 111.48bn): real estate activities 29.59bn (computed 26.5%); wholesale and retail trade 14.13bn (12.7%); manufacturing 8.60bn (7.7%); administrative and support 7.59bn (6.8%); transport and storage 7.04bn (6.3%). [N3 p.70]
- CRE LTV distribution, 30 Jun 2026 (CRE investment loans with LTVs, GBP 14.24bn): <=50% 7.86bn; >50-60% 4.68bn; >60-70% 0.98bn; >70-100% 0.51bn; >100% 0.21bn. Computed share above 70% LTV = 5.1% (31 Dec 2025: 5.2%, 0.72bn of 13.82bn). Average LTV 49% (Stage 3: 79%). Total CRE investment GBP 17.28bn plus development and other GBP 2.97bn. "The majority of the CRE portfolio was located and managed in the UK." [N2]
- Risk appetite (published): "The Non-Personal credit risk appetite framework ... is used to manage concentrations of risk which may arise across four lenses - single name, sector, country and product and asset classes. The framework is supported by a suite of transactional acceptance standards that set out the risk parameters within which businesses should operate." No numeric limits published. [N3 p.75]
- SME product terms [N4]: Small Business Loan GBP 1,000 to 100,000 (apply online for GBP 50,001-100,000); fixed rate; terms 1 to 7 years; no set-up, early repayment or early closure fees; "A personal, director or member's guarantee may be required" (no threshold stated); eligibility: aged 18+, a director of the business, no bankruptcy/CCJ, holds a business current account with any provider. Application asks for "the date your business started trading" but no minimum trading period is stated. Larger loans: "from GBP 25,001 with no upper limit on a variable interest rate, or up to GBP 10m on a fixed interest rate". Representative APR: the calculator's default example showed GBP 7,500 and "8.2%" but the label mapping was ambiguous in the captured page (treat as L confidence; see Part C).
- Growth Guarantee Scheme: NatWest Group plc drew GBP 130.19m across 541 facilities to 30 Jun 2026; GGS is listed in the N4 page menu. [S4, N4]
- Not found for NatWest: a separate Business Banking loan balance; minimum trading history; numeric sector limits.

