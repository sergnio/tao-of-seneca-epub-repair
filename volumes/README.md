# Volumes

One folder per volume, holding the repaired `.epub`.

| Volume | Source | Status |
|---|---|---|
| 1 | Lighten PDF Converter output of the print PDF | repaired |
| 2 | not yet obtained | — |
| 3 | not yet obtained | — |

Originals are deliberately not committed — the repair is reproducible from any
copy of the source EPUB by running the script.

## Adding volume 2 or 3

The repair is **not** turnkey for a new volume. Two inputs are volume-specific and
must be rebuilt by hand before the script will do the right thing:

1. `HEADER_PATTERNS` — the running page headers name the volume and its sections.
   `--list-headers` prints candidates.
2. `GLUED` — the table of run-together words. Different text means different names
   and different Latin, so **do not reuse volume 1's table**. `--list-glued` prints
   candidates; every line needs a human decision.

`../FIXES.md` walks through both, with the traps that produce confident wrong
answers (`Hecato` is not "He cato").

The script also assumes the Lighten PDF Converter layout (`OEBPS/Text/N.html`, one
paragraph per line ending in `<br/>`). A conversion that emits one file per page
with each page as a single `<p>` blob needs a different approach entirely.
