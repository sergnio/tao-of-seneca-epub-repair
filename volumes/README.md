# Volumes

One folder per volume: the repaired `.epub` and the `config.py` that produced it.

| Volume | Source | Headers removed | Words unglued | Status |
|---|---|---|---|---|
| 1 | CleverPDF job 182870 | 253 | 220 | repaired |
| 2 | CleverPDF job 185218 | 254 | 142 | repaired |
| 3 | CleverPDF job 185221 | 254 | 131 | repaired |

Originals are deliberately not committed — the repair is reproducible from any
copy of the source EPUB.

## Each volume needs its own config

`config.py` holds the two tables that cannot be shared between volumes:

- **`HEADER_PATTERNS`** — the running headers name the volume and its sections.
- **`GLUED`** — the run-together words, which come from that volume's vocabulary.

What actually differed, all found by running the `--list-*` passes:

| | Volume 1 | Volume 2 | Volume 3 |
|---|---|---|---|
| sections | foreword, 28 Books on Stoicism | — | proper-name and subject indexes |
| oddity | — | `pROFILES` with a lowercase p | header with no page number at all |
| oddity | — | embeds a Volume 3 *sample* with its own header | letter numbers reach three digits |

Volume 3's indexes also break an assumption the first two volumes never tested:
their alphabetical dividers are single letters standing alone on a line, which the
paragraph rejoiner would happily weld onto the first entry. Hence the
one-character guard.

## Adding another volume

```bash
python3 tao_of_seneca_fix.py --list-headers "vol.epub"

# first pass with an empty GLUED, so the next listing is not polluted by
# hyphenation fragments (ourable, oured, mence) that the repair itself removes
python3 tao_of_seneca_fix.py "vol.epub" pass1.epub --config volumes/volume-N/config.py
python3 tao_of_seneca_fix.py --list-glued pass1.epub --config volumes/volume-N/config.py

python3 tao_of_seneca_fix.py "vol.epub" out.epub --config volumes/volume-N/config.py \
    --title "The Tao of Seneca, Volume N of 3"
```

Listing glued words against the **raw** file wastes your time: every word the
converter split across a line break shows up as two bogus tokens. Do the first
pass first.
