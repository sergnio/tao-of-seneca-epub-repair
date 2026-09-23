# tao-of-seneca-epub-repair

Repairs a PDF-to-EPUB conversion of *The Tao of Seneca* (Tim Ferriss's free
compilation of Seneca's *Moral Letters to Lucilius*).

The conversion was done by Lighten PDF Converter from the print PDF, and it carried
the print layout across literally: running page headers landed in the middle of
sentences, page breaks became paragraph breaks, and words hyphenated across a line
break stayed broken. This repository holds the script that undoes all of it and the
repaired volume 1.

## What was wrong

A representative sample — the page header dropped into the middle of a sentence:

> …let the bread be hard and grimy. Endure all this for three or four days at a
> time, sometimes for more, so that
>
> **92 THE TAO OF SENECA | VOLUME 1**
>
> it may be a test of yourself instead of a mere hobby.

Eight artifact classes in all, fixed in one pass:

| # | Artifact | Volume 1 count |
|---|---|---|
| 1 | Running page headers dropped mid-sentence | 253 removed |
| 2 | Paragraphs split mid-sentence at page/column breaks | 350 rejoined |
| 3 | Words split by a hyphen at a line break (`immu -  nity`) | 171 healed |
| 4 | Stray ornament `A` paragraph after every heading | 69 removed |
| 5 | Letter-spaced headings (`L E T T E R 2 1`) | 65 collapsed |
| 6 | Footnote markers jammed against the word (`our[2]`) | 247 spaced |
| 7 | Words run together by a lost thin space (`Whydo`, `NFLin`) | 220 split |
| 8 | Heading spacing, and a `<dc:title>` holding a Windows build path | 68 + title |

`FIXES.md` documents each one, the rules used to decide when to rejoin text, and
what was deliberately left alone and why.

## Usage

```bash
python3 tao_of_seneca_fix.py --list-headers "in.epub"   # per-volume: running headers
python3 tao_of_seneca_fix.py --list-glued   "in.epub"   # per-volume: glued words
python3 tao_of_seneca_fix.py "in.epub" "out.epub" --title "The Tao of Seneca, Volume 1 of 3"
```

No dependencies beyond the Python 3 standard library. `--list-glued` reads
`/usr/share/dict/words` to screen out real words.

The two `--list-*` steps are not optional for a new volume: `HEADER_PATTERNS` and
`GLUED` are both volume-specific, and `GLUED` in particular needs a human to review
every line. See `volumes/README.md`.

## Verifying a run

The check that caught real bugs during development: strip all whitespace from the
text before and after, apply the same de-hyphenation to both, and compare. Repairing
this conversion only ever removes junk, joins halves, or inserts a space — so the
two must come out character-identical. For volume 1 that is 431,617 characters
either way.

Then confirm the XHTML still parses, and that `mimetype` is the first zip entry and
stored uncompressed (the script handles the latter).

## Scope

The script targets this specific converter's output, not EPUBs in general. It
assumes `OEBPS/Text/N.html` with one paragraph per physical line ending in `<br/>`,
paragraphs separated by a bare `<br/>`, and a wrapped line represented as two
spaces. Those assumptions are what make the paragraph rejoining tractable.

## Contents

```
tao_of_seneca_fix.py                              the repair, all eight passes
FIXES.md                                          what was wrong and how each fix decides
volumes/volume-1/tao-of-seneca-vol1-repaired.epub
volumes/README.md                                 per-volume notes and status
```

## A note on the book

*The Tao of Seneca* is given away free by Tim Ferriss at
[tim.blog/2017/07/06/tao-of-seneca](https://tim.blog/2017/07/06/tao-of-seneca/).
Seneca's letters in the Richard Gummere translation are public domain; the
compilation around them — foreword, commissioned interviews, artwork, design — is
not. This repository is private for that reason: free to download is not the same as
free to redistribute. If you want to make it public, drop the `volumes/` EPUBs and
publish the script and notes on their own.
