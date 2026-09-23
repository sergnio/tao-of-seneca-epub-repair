# Tao of Seneca — EPUB repair notes

What was broken in `Tao of Seneca v1.epub`, what was changed, and how to do the same
to Volumes 2 and 3.

Companion script: **`tao_of_seneca_fix.py`** (repo root). It performs every change
below in one pass and was verified to reproduce `Tao of Seneca v4.epub`
byte-for-byte from the untouched original.

---

## The source of all of it

The EPUB was made by **Lighten PDF Converter 5.2.0** from the print PDF. The layout:

```
OEBPS/Text/1.html … 7.html      the whole book, 7 files
OEBPS/content.opf, toc.ncx
OEBPS/Images/*.jpg
```

Inside `<body>`, every paragraph is one physical line ending in `<br/>`, and
paragraphs are separated by a line containing only `<br/>`:

```html
<body>
		Paragraph text, with  a wrapped line shown as two spaces.<br/>
<br/>
		Next paragraph.<br/>
	</body>
```

Two structural facts that everything below depends on:

- A **line wrap inside** a paragraph became **two spaces**, not a tag.
- A **page break** became a **real paragraph break** — which is the bug.

---

## Versions produced

| File | Contains |
|---|---|
| `Tao of Seneca v1.epub.backup` | untouched original |
| `Tao of Seneca v2.epub` | running headers removed |
| `Tao of Seneca v3.epub` | + de-hyphenation and mid-sentence rejoining |
| `Tao of Seneca v4.epub` | + ornament removal, heading spacing, real title |
| `Tao of Seneca v5.epub` | + `L E T T E R 2 1` collapsed to `LETTER 21` |
| `Tao of Seneca v6.epub` | + footnote markers spaced, glued words split |

---

## The eight artifacts

### 1. Running page headers dropped into the middle of sentences — 253 removed

Each printed page's header became its own paragraph, wherever the page happened to
break:

```
…let the bread be hard and grimy. Endure all this for three or four days
at a time, sometimes for more, so that

92 THE TAO OF SENECA | VOLUME 1

it may be a test of yourself instead of a mere hobby.
```

Six header shapes in Volume 1:

| Pattern | Count |
|---|---|
| `N THE TAO OF SENECA \| VOLUME 1` | 122 |
| `MORaL LETTERS TO LUCILIUS N` | 104 |
| `PROFILES OF MODERN-Day STOICS FROM TOOLS OF TITaNS N` | 11 |
| `THOUGHTS FROM MODERN STOICS \| <NAME> N` | 10 |
| `28 BOOkS ON STOICISM N` | 4 |
| `FOREwORD: HOw TO USE THIS BOOk N` | 2 |

The odd capitalisation (`MORaL`, `BOOkS`, `TITaNS`, `HOw`) is the converter
mis-reading small caps. Match it literally.

**Do not** delete: the table-of-contents rows, the `THOUGHTS FROM MODERN STOICS`
section title pages (no page number, no `|`), or the `L E T T E R N` chapter
headings — those are real content with the same shape.

### 2. Paragraphs split mid-sentence — 350 rejoined

Removing a header leaves two halves of one sentence. The same split also happens at
column breaks with no header involved. Rejoined with two spaces (matching how the
converter renders a wrapped line):

- 154 at a removed header
- 193 elsewhere in a file
- 3 across a file boundary (3→4, 5→6, 6→7 — the continuation paragraph is moved to
  the end of the previous file)

### 3. Words split by a hyphen at a line break — 171 healed

```
immu -  nity   →  immunity
backstab -  bing  →  backstabbing
…practical phi -   +  losophies in the real world  →  philosophies
```

155 inside a paragraph, 16 across a paragraph break. Two of the cross-break ones sit
inside `<a href>` + `<b>` markup in the book list, so the fix edits only the text
*between* tags — otherwise it would corrupt the Amazon URLs.

### 4. A stray `A` after every heading — 69 removed

```
L E T T E R 2
On Discursiveness in Reading
A                      ← this
Judging by what you write me…
```

A decorative ornament from the PDF that OCR'd as a capital A. The real drop cap is
the bold first letter of the next paragraph (`<b>J</b>udging…`), so the `A` is pure
noise.

### 5. Letter-spaced chapter headings — 65 collapsed

The converter preserved the print edition's letter spacing as real spaces:

```html
<a id="C23"><b>L</b></a><b> E T T E R 2 1</b><br/>     →  "L E T T E R 2 1"
```

Collapsed to `LETTER 21`. The `L` stays inside its `<a id="C23">` anchor — that is
the target the table of contents links to — and only the run after `</a>` is
rewritten:

```html
<a id="C23"><b>L</b></a><b>ETTER 21</b><br/>          →  "LETTER 21"
```

All 65 headings use one of two shapes (`L E T T E R N` and `L E T T E R N N`) and
nothing else in the book is letter-spaced, so this is a safe blanket rewrite. All 76
anchors survive unchanged.

### 6. Footnote markers jammed against the word before — 247 spaced

The book was inconsistent about this: 89 markers already had a space, 246 did not.

```
in the writings of our[2] Hecato   →   in the writings of our [2] Hecato
```

All of them now carry a space, matching the style the book already used more than a
third of the time. This is the one blanket rule here with no exceptions: `[n]` that
follows a non-space character gets a space inserted. It is applied to text between
tags, so a marker that already sits outside its `<b>` (`<b>On Despising Death </b>[1]`
— one case) is left alone, since it already renders with a space.

### 7. Words run together by a lost thin space — 220 split

```
Whydo I fast     →   Why do I fast
the NFLin the    →   the NFL in the
myown, mydear, whomyou, amglad, menwho, Doyou, Howmuch, CEOand, HOWTO …
```

**This is the one fix that cannot be fully automated, and the reason is worth
understanding before you do Volume 2.** The obvious heuristic — "if the token is not
a dictionary word, try splitting it into two words" — produces a large number of
confident, wrong answers on this book:

| Token | The heuristic says | Reality |
|---|---|---|
| `Hecato` | He + cato | a Stoic philosopher |
| `publicam` | public + am | Latin (`rem publicam`) |
| `Naturalis` | Natural + is | Latin (`Naturalis Quaestiones`) |
| `countrymen`, `workmen`, `foemen` | … + men | ordinary English |
| `forgiven` | for + given | ordinary English |
| `Betake`, `novices`, `online`, `summoned` | be + take, no + vices, … | ordinary English |

Two further traps that cost me a rewrite each:

- **`/usr/share/dict/words` is missing many plurals** (`ears`, `feelings`, `plans`),
  so `myears` and `myfeelings` were silently skipped. The generator now falls back
  to the book's own vocabulary — a token that appears 8+ times elsewhere in the book
  counts as a real word.
- **Drop caps live in their own tag.** `<b>I</b>amglad` reads as `Iamglad` if you
  strip tags first, but the actual text node holds `amglad`. The table is keyed on
  text-node tokens and applied between tags, so the entry is `amglad`, not `Iamglad`.

So the script carries an **explicit, hand-reviewed table** (`GLUED`, 177 entries for
Volume 1) rather than a rule. `--list-glued` generates candidates; a human decides.
Running it against the finished v6 leaves 33 candidates, all of them correct keepers
(`Aeneas`, `adoremus`, `measures`, `online`, `YouTube`, …) — a useful shape to
compare against when you review another volume's list.

### 8. Heading spacing and title metadata

The blank line between the heading and its title was removed for all 65 letters
(68 blanks — three letters have two-line titles). Combined with fixes 4 and 5, a
letter opens like this:

```
LETTER 2
On Discursiveness in Reading

Judging by what you write me…
```

`<dc:title>` in `content.opf` and `<docTitle>` in `toc.ncx` both held the
converter's Windows build path —
`D:\wwwroot\cleverpdf-web\182870\Tao of Seneca v1.epub` — replaced with
`The Tao of Seneca, Volume 1 of 3`.

---

## The rules used to decide when to rejoin

This is where the judgment lives. Being conservative is the whole point: a missed
join leaves text that reads a bit broken, but a wrong join merges quoted verse into
prose and is much harder to spot later.

**Rejoin the previous and next paragraph when both hold:**

1. The previous paragraph does **not** end a sentence — ignoring a trailing footnote
   marker (`[4]`) and trailing quotes/brackets, so `poverty? [1]` counts as
   *finished* and `so that` does not. A trailing `:` counts as finished (it
   introduces a displayed quote).
2. The next paragraph starts with a **lowercase letter**.

**Except — never rejoin when:**

| Guard | Why |
|---|---|
| previous line has `<a id=…>` | it is a chapter heading |
| either line has `<img` | a full-page artwork |
| previous is under 45 chars, has no internal double space, and is not bold | a displayed verse line (`Lands and cities are left astern,`) |
| next is under 5 chars | a verse connector (the bare `or` between two Vergil lines) |
| previous is entirely bold and next has no bold | a title followed by its byline |

At a removed **header** rule 1 alone is used (rule 2 adds nothing there — the two
signals agreed on all 253).

Five splits in Volume 1 are left in place on purpose: two Vergil verse lines with
their commentary, one verse connector, and two heading/byline pairs
(`HOW TO USE THIS BOOK` / `by Tim Ferriss`).

Splits where the continuation starts with a **capital** are also left alone — too
close to verse to automate.

### Other things left alone deliberately

- The standalone `. . .` lines in the foreword mark skipped text between quoted
  Seneca excerpts, and the `. . .` in "I'm excited for you . . . and envious of you"
  is a rhetorical pause. Both are intentional.
- `Artwork opposite by <name>` credit lines had been stranded mid-sentence; they were
  moved to sit directly under their image (5 of them) rather than deleted.
- `Calligrapher: Noriko Lake` lines were already correctly placed.

---

## Doing Volumes 2 and 3

### Step 1 — check the conversion matches

```bash
python3 tao_of_seneca_fix.py --list-headers "vol2.epub"
```

This prints every repeating header-shaped line with a count. It only works if the
EPUB has the Lighten layout (`OEBPS/Text/N.html`).

> **The `taoofseneca_vol2.epub` currently in Downloads will not work.** It is from a
> different converter: 308 files, one per *page* (`EPUB/page_N.html`), each page's
> text as a single `<p>` blob with the header glued to the front and all paragraph
> breaks already lost — `MORAL LETTERS TO LUCILIUS 59 from wine or to be routed…`.
> Footnote markers are mangled too (`1151` for `[15]`). Nothing here applies to it.
> Re-convert Volumes 2 and 3 with **Lighten PDF Converter** the way Volume 1 was
> done, then this script works.

### Step 2 — set the header patterns and review the glued words

Edit `HEADER_PATTERNS` at the top of the script. Expect these to change per volume:

- `VOLUME 1` → `VOLUME 2` / `VOLUME 3`
- the interviewee names in `THOUGHTS FROM MODERN STOICS | <NAME> N`
- the section headers — each volume has its own back matter

Copy the odd capitalisation exactly as `--list-headers` prints it.

Then rebuild the glued-word table. **Do not reuse Volume 1's** — different text,
different names, different Latin:

```bash
python3 tao_of_seneca_fix.py --list-glued "vol2.epub"
```

It prints ready-to-paste `'token': 'replacement',` lines with an occurrence count.
Read every one and delete the wrong ones before pasting into `GLUED`; see the traps
in artifact 7. When a split is right but the *split point* is wrong (`ALife` →
`AL ife`), just correct the replacement by hand. Checking a token in context is the
fastest way to decide:

```bash
python3 - <<'EOF'
import re,html,zipfile
z=zipfile.ZipFile('vol2.epub')
t=' '.join(html.unescape(re.sub('<[^>]+>','',z.read(n).decode()))
           for n in z.namelist() if n.endswith('.html'))
t=re.sub(r'\s+',' ',t)
for m in re.finditer(r'(?<![A-Za-z])TOKEN(?![A-Za-z])',t):
    print('…'+t[max(0,m.start()-70):m.end()+70]+'…')
EOF
```

### Step 3 — run it

```bash
python3 tao_of_seneca_fix.py \
    "vol2.epub" "Tao of Seneca vol2 fixed.epub" \
    --title "The Tao of Seneca, Volume 2 of 3"
```

It prints a count for each change. Sanity-check them against Volume 1's numbers below — a wildly different count
usually means a header pattern is wrong.

| Count | Volume 1 |
|---|---|
| `headers_removed` | 253 |
| `joined_at_header` + `joined_mid_sentence` + `joined_across_files` | 154 + 193 + 3 |
| `hyphens_inline` + `joined_hyphen` | 155 + 16 |
| `ornament_A_removed` | 69 |
| `headings_tightened` | 68 |
| `letter_headings_despaced` | 65 |
| `footnotes_spaced` | 247 |
| `words_unglued` | 220 |

### Step 4 — verify

Three checks worth doing every time:

1. **Nothing lost.** Strip all whitespace from the before and after text, apply the
   same de-hyphenation to both, and compare. They must be identical. That is how
   each version here was checked.
2. **Still valid XML.** `python3 -c "import xml.dom.minidom,glob;
   [xml.dom.minidom.parse(f) for f in glob.glob('OEBPS/**/*.*ml',recursive=True)]"`
3. **`mimetype` is the first zip entry and stored uncompressed.** The script handles
   this; if you ever repack by hand, `zip -X -0 out.epub mimetype` first, then
   `zip -X -9 -r out.epub META-INF OEBPS`.

---

## Still present in v6 (not fixed)

- Glued words not in the reviewed table. The table covers what `--list-glued` and a
  read-through surfaced; a rarer one could survive. `cakeseller` and `sausageman`
  were left as-is deliberately — the print edition hyphenates them, so a lost hyphen
  rather than a lost space, and either reading is defensible.
- The `<dc:creator>` field is empty; the book shows no author in a library.
- `toc.ncx` has a single nav point (`begin` → `1.html`), so there is no chapter list.
  The `<a id="C2">…<a id="C69">` anchors on the letter headings are already in place,
  so a real TOC could be generated from them.
