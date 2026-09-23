# tao-of-seneca-epub-repair

Repairs a PDF-to-EPUB conversion of *The Tao of Seneca* (Tim Ferriss's free
compilation of Seneca's *Moral Letters to Lucilius*).

The conversion was done by CleverPDF's online converter from the print PDF, and it carried
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

Eight artifact classes in all, fixed in one pass. All three volumes are repaired:

| # | Artifact | Vol 1 | Vol 2 | Vol 3 |
|---|---|---|---|---|
| 1 | Running page headers dropped mid-sentence | 253 | 254 | 254 |
| 2 | Paragraphs split mid-sentence at page/column breaks | 350 | 276 | 338 |
| 3 | Words split by a hyphen at a line break (`immu -  nity`) | 171 | 492 | 481 |
| 4 | Stray ornament `A` paragraph after every heading | 69 | 31 | 36 |
| 5 | Letter-spaced headings (`L E T T E R 2 1`) | 65 | 28 | 32 |
| 6 | Footnote markers jammed against the word (`our[2]`) | 247 | 334 | 228 |
| 7 | Words run together by a lost thin space (`Whydo`, `NFLin`) | 220 | 142 | 131 |
| 8 | Heading spacing | 68 | 28 | 32 |

`FIXES.md` documents each one, the rules used to decide when to rejoin text, and
what was deliberately left alone and why.

## Usage

```bash
python3 tao_of_seneca_fix.py --list-headers "in.epub"            # per-volume: running headers
python3 tao_of_seneca_fix.py --list-glued   "in.epub" --config … # per-volume: glued words

python3 tao_of_seneca_fix.py "in.epub" "out.epub" \
    --config volumes/volume-1/config.py \
    --title "The Tao of Seneca, Volume 1 of 3"
```

`--config` is required and volume-specific: it carries that volume's running-header
patterns and its hand-reviewed glued-word table. See `volumes/README.md`.

No dependencies beyond the Python 3 standard library. `--list-glued` reads
`/usr/share/dict/words` to screen out real words.

The two `--list-*` steps are not optional for a new volume, and `GLUED` in
particular needs a human to review every line.

## Verifying a run

The check that caught real bugs during development: strip all whitespace from the
text before and after, apply the same de-hyphenation to both, and compare. Repairing
this conversion only ever removes junk, joins halves, or inserts a space — so with
the deleted junk (running headers, ornament `A`s) and the relocated artwork credits
excluded from both sides, the two come out character-identical: **431,471 /
418,983 / 409,902** for volumes 1, 2 and 3.

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
volumes/volume-N/config.py                        that volume's headers + glued words
volumes/volume-N/tao-of-seneca-volN-repaired.epub
volumes/README.md                                 per-volume notes and status
LICENSE                                           MIT, scoped to the code and docs
NOTICE                                            credit and rights for the book itself
```

## License

The script and the documentation are MIT — use them for anything.

**The MIT license does not cover the ebooks under `volumes/`.** That is Tim Ferriss's
book, not mine, and I have no rights to grant in it. See `NOTICE` for the full
statement. Short version: all credit for the book goes to Tim Ferriss and its
contributors, the Gummere translation of Seneca underneath it is public domain, and
the repaired files are here because his download page says sharing is encouraged.

Please get the book from [his page](https://tim.blog/2017/07/06/tao-of-seneca/)
rather than from here. It is free, and going to the source supports the person who
made it.

## Where the broken EPUB came from

Worth recording, because reproducing the repair means reproducing the conversion.

The source EPUB was produced by [CleverPDF](https://www.cleverpdf.com/)'s online
PDF-to-EPUB converter. It wrote its own server-side output path into the title
field, which is how we know:

```xml
<dc:title>D:\wwwroot\cleverpdf-web\182870\Tao of Seneca v1.epub</dc:title>
<meta name="Lighten PDF Converter version" content="5.2.0" />
```

Two things in that file are misleading and cost me time:

- `dc:date modification` reads `2016-12-09`, seven months *before* the source PDFs
  were produced (2017-06-26). It is the converter's build date, not a conversion
  date.
- The zip's directory entries are stamped seven hours behind its file entries — a
  timezone bug in the converter's zip writer.

To repair another volume, convert its PDF with the same service so the structure
matches. A different converter means different artifacts; see `volumes/README.md`.
