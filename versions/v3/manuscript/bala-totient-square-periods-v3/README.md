# Totient-square periods for Bala's inverse-function sequences

This package contains **A jet-space proof and extension of Su's theorem on Bala's totient-square period conjectures**, by Haobo Ma (ChronoAI Pte Ltd, Singapore) and Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore).

For every positive integer `q` and nonnegative integer `e`, let `C'=C^q S`, `S'=C^(q+1)`, `C(0)=1`, `S(0)=0`, and `A(q,e,n)=(2n)! [t^(2n)] C(t)^e`. The note proves integrality and

`A(q,e,n+phi(k)^2) = A(q,e,n) (mod k)` for every positive integer `k` and `n >= k^2`.

For odd `q`, this is an alternative proof of results of Lien-Hung Su, *Quadratic Derivations and Uniform Modular Periods for Six Inverse-Function Sequences*, version 1, 31 October 2026, DOI [10.5281/zenodo.23835577](https://doi.org/10.5281/zenodo.23835577), Theorem 3.2 and Corollary 3.3. Su gives the stronger period `phi(k)^2/2` for `k>=3` and sharper preperiod bounds. The origin of the principal question is Peter Bala's 16 February 2026 comment on [OEIS A281181](https://oeis.org/A281181), revision 103. Companion entries are A281180, A281183, A281184 and A281440. For A281180, the source index is one greater than the column index.

## Files

- `note.tex`: complete mathematical argument, source coverage, references and pinned Lean declaration links.
- `metadata.json`: title, creators, license and exact covered problem identifiers.
- `verify.py`: standard-library Python 3 program using integer, rational and modular polynomial arithmetic.
- `check-results.json`: deterministic output of the verification command below.
- `verify-siblings.py` and `sibling-check-results.json`: exact checks of the additional A281432 and A281439 specializations.

## Build the PDF

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively use a standard LaTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in `note.tex`; there are no external bibliography or figure dependencies.

## Reproduce the exact checks

```sh
python3 verify.py --output reproduced-check-results.json
cmp check-results.json reproduced-check-results.json
python3 verify-siblings.py --output reproduced-sibling-check-results.json
cmp sibling-check-results.json reproduced-sibling-check-results.json
```

No network connection or third-party Python package is required. The program compares the integer differential-operator coefficients with independent rational coefficients of the defining ODEs, checks the displayed initial terms, computes exact coefficients through column index 256, and gives all-index certificates for the five columns modulo each integer from 2 through 24. It also certifies the seven least periods in the note, the constant residue modulo 12, and the geometric-column relation modulo 13. Consecutive scalar differences in a finite-dimensional matrix representation imply the corresponding infinite identities by Cayley-Hamilton; this implication is proved in the note. Exact coefficient hashes use the UTF-8 decimal representation with no final newline.

The theorem for arbitrary moduli and every positive integer `q`, including its bound, has a written proof. The pinned Lean declaration scope is specified separately in the note; the extra scope of the written theorem is not attributed to those declarations.

Two further specializations are A281432(n)=A(5,1,n) and A281439(n)=A(7,8,n-1). Their sufficient source-index bounds are `n>=k^2` and `n>=k^2+1`, respectively. They also follow from Su's general Theorem 3.2. Their OEIS definitions are at <https://oeis.org/A281432> and <https://oeis.org/A281439>. The separate sibling checker compares their displayed initial terms, rational ODE coefficients and finite-dimensional period certificates modulo 2 through 24. Metadata identifies the five posed source conjectures; the note's tables give the further companion congruences.

## Further companion columns

The odd-prime coordinate uses the unique square root `b^2=1+y^2` with constant term one in the truncated ring and the polynomial coefficient `b^(q+1)`. This extends the argument to even positive `q` without changing the two-adic proof. In addition to the seven original table entries, the note covers A281428 and A281427 (`q=4`), A281436 and A281435 (`q=6`), A281444 and A281443 (`q=8`), and A281431 (`q=5`, odd column). Their square-totient congruences are consequences of the stated theorem; the OEIS entries do not pose those additional congruences. Su's Theorem 4.1 proves the stronger original A281428 assertions about eventual vanishing and the single-totient shift.

For A281182, the even and odd indexed terms are `A(3,1,n)` and `A(3,4,n)`. Thus a shift of `2*phi(k)^2` is a period modulo `k` from full index `2*k^2`. The double shift, rather than the single-column shift, is the assertion proved here.

`verify-general.py` checks rational ODE normalization for `q=1,...,8` and observables `e` in `{0,1,2,q+1}`. Its finite-dimensional period certificates cover each modulus from 2 through 16 and imply the corresponding infinite tail congruences by the Cayley-Hamilton argument in the note. It also checks all displayed initial terms for the eight further entries.

```sh
python3 verify-general.py --output reproduced-general-check-results.json
cmp general-check-results.json reproduced-general-check-results.json
```

## License

The note, metadata and verification code are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0): <https://creativecommons.org/licenses/by/4.0/>. Attribution: Haobo Ma and Wenlin Zhang. Third-party publications linked in the bibliography retain their respective licenses.
