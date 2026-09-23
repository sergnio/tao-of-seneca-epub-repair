#!/usr/bin/env python3
"""
Repair a Lighten-PDF-Converter EPUB of "The Tao of Seneca".

Five conversion artifacts are undone, in order:
  1. running page headers dropped into the middle of sentences
  2. paragraphs split mid-sentence at page/column boundaries
  3. words split by a hyphen at a line break  ("immu -  nity")
  4. a stray ornament "A" paragraph after every heading
  5. letter-spaced chapter headings ("L E T T E R 2 1")
  6. footnote markers jammed against the preceding word ("our[2]")
  7. words glued together by a lost thin space ("Whydo", "NFLin")
  8. a garbage <dc:title> (a Windows build path)

Usage
  python3 fix_epub.py --list-headers "in.epub"     # step 1: see what repeats
  python3 fix_epub.py --list-glued   "in.epub"     # step 2: review glued words
  python3 fix_epub.py "in.epub" "out.epub" --title "The Tao of Seneca, Volume 2 of 3"

Every volume needs --list-headers run FIRST: the running headers name the
volume and its sections, so HEADER_PATTERNS below must be checked per volume.
"""
import re, html, os, sys, shutil, zipfile, tempfile, argparse
from collections import Counter

# ---------------------------------------------------------------- headers ---
# Confirmed for Volume 1. Re-run --list-headers for other volumes and edit.
HEADER_PATTERNS = [
    r'\d+ THE TAO OF SENECA \| VOLUME \d+',
    r'MORaL LETTERS TO LUCILIUS \d+',
    r'THOUGHTS FROM MODERN STOICS \| .+? \d+',
    r'PROFILES OF MODERN-Day STOICS FROM TOOLS OF TITaNS \d+',
    r'\d+ BOOkS ON STOICISM \d+',
    r'FOREwORD: HOw TO USE THIS BOOk \d+',
]

# Words the converter ran together where the PDF had a thin space. HAND-REVIEWED
# for Volume 1 -- run --list-glued on another volume and review its list before
# trusting it: the same heuristics also flag Latin, Greek and proper nouns
# ("Hecato" is not "He cato", "publicam" is not "public am").
GLUED = {
    'adistillation': 'a distillation', 'Agood': 'A good', 'Agreat': 'A great',
    'Ahall': 'A hall', 'ALife': 'A Life', 'amabove': 'am above', 'amafraid': 'am afraid',
    'amaware': 'am aware', 'amdoing': 'am doing', 'amglad': 'am glad',
    'amgrieved': 'am grieved', 'amindeed': 'am indeed', 'amnot': 'am not',
    'Amomentago': 'A moment ago', 'amready': 'am ready', 'amrunning': 'am running',
    'amsituated': 'am situated', 'amstill': 'am still', 'amsure': 'am sure',
    'Amust': 'A must', 'amwasting': 'am wasting', 'amwont': 'am wont',
    'amworking': 'am working', 'Andmotion': 'And motion', 'AndnowI': 'And now I',
    'Andwhen': 'And when', 'Andwhich': 'And which', 'Asingle': 'A single',
    'Aspirit': 'A spirit', 'CDBaby': 'CD Baby', 'CDsold': 'CD sold', 'CDwas': 'CD was',
    'CEOand': 'CEO and', 'commoncrowd': 'common crowd', 'commonphrase': 'common phrase',
    'commonproperty': 'common property', 'commonstrategy': 'common strategy',
    'Donot': 'Do not', 'Doyou': 'Do you', 'Godcannot': 'God cannot', 'Godhas': 'God has',
    'Howare': 'How are', 'Howcomforting': 'How comforting', 'Howmany': 'How many',
    'Howmuch': 'How much', 'Howotherwise': 'How otherwise', 'HOWTO': 'HOW TO',
    'madea': 'made a', 'madeuse': 'made use', 'Manand': 'Man and', 'manfrom': 'man from',
    'mannoteworthy': 'man noteworthy', 'manpass': 'man pass', 'manregards': 'man regards',
    'manwhomade': 'man who made', 'manwould': 'man would', 'manyof': 'many of',
    'mayhinder': 'may hinder', 'maynever': 'may never', 'maytend': 'may tend',
    'meabout': 'me about', 'meaway': 'me away', 'mehad': 'me had', 'meintact': 'me intact',
    'meinto': 'me into', 'melittle': 'me little', 'memore': 'me more',
    'menbefore': 'men before', 'meneven': 'men even', 'menfrom': 'men from',
    'Menhave': 'Men have', 'menhave': 'men have', 'menmeet': 'men meet',
    'menpersuade': 'men persuade', 'menshould': 'men should', 'menshrink': 'men shrink',
    'menwere': 'men were', 'menwhen': 'men when', 'menwho': 'men who',
    'menwould': 'men would', 'meone': 'me one', 'methat': 'me that',
    'methrough': 'me through', 'mewhyI': 'me why I', 'mewill': 'me will',
    'mewith': 'me with', 'muchas': 'much as', 'muchtime': 'much time',
    'myadvancing': 'my advancing', 'myassistance': 'my assistance',
    'myconstitution': 'my constitution', 'mycore': 'my core', 'mycredit': 'my credit',
    'mycustomary': 'my customary', 'mydanger': 'my danger', 'mydear': 'my dear',
    'mydebt': 'my debt', 'mydrink': 'my drink', 'myears': 'my ears',
    'myendurance': 'my endurance', 'myenthusiasm': 'my enthusiasm',
    'myentire': 'my entire', 'Myfather': 'My father', 'myfault': 'my fault',
    'myfeelings': 'my feelings', 'myfirst': 'my first', 'myfood': 'my food',
    'myfriend': 'my friend', 'myGod': 'my God', 'mygood': 'my good', 'mygreed': 'my greed',
    'myhand': 'my hand', 'myhapless': 'my hapless', 'myhead': 'my head',
    'myintent': 'my intent', 'mylife': 'my life', 'myLucilius': 'my Lucilius',
    'mymind': 'my mind', 'myobject': 'my object', 'myold': 'my old', 'myown': 'my own',
    'mypart': 'my part', 'mypilot': 'my pilot', 'myplans': 'my plans',
    'myprofession': 'my profession', 'myreading': 'my reading', 'myseal': 'my seal',
    'myseat': 'my seat', 'mystomach': 'my stomach', 'mytrouble': 'my trouble',
    'myturnaround': 'my turnaround', 'myvices': 'my vices', 'NFLin': 'NFL in',
    'Nowthe': 'Now the', 'Nowthere': 'Now there', 'Nowwhat': 'Now what',
    'OnJuly': 'On July', 'Onthe': 'On the', 'onyou': 'on you', 'Ourfriend': 'Our friend',
    'Owhen': 'O when', 'ownperson': 'own person', 'summonyou': 'summon you',
    'TEDconferences': 'TED conferences', 'Wasthat': 'Was that', 'Waythe': 'Way the',
    'Weare': 'We are', 'Weblush': 'We blush', 'Wecannot': 'We cannot', 'Wehave': 'We have',
    'Wemust': 'We must', 'Weought': 'We ought', 'Wereally': 'We really',
    'Weshall': 'We shall', 'Weshould': 'We should', 'Wewould': 'We would',
    'WhenI': 'When I', 'Whenpersons': 'When persons', 'Whenyou': 'When you',
    'whocomefrom': 'who come from', 'whois': 'who is', 'whomI': 'whom I',
    'whomit': 'whom it', 'whomno': 'whom no', 'whomstarvation': 'whom starvation',
    'whomVergil': 'whom Vergil', 'whomwe': 'whom we', 'whomyou': 'whom you',
    'whostands': 'who stands', 'Whyare': 'Why are', 'Whydo': 'Why do',
    'Whyshould': 'Why should', 'Whythen': 'Why then', 'Whywait': 'Why wait',
    'Youare': 'You are', 'Youcan': 'You can', 'youstill': 'you still'
}

TOK     = re.compile(r'(<[^>]*>)')        # odd split indices are tags
LETTER  = r'[^\W\d_]'
INLINE_HYPH = re.compile(rf'({LETTER})\s+-\s+({LETTER})')
FOOTNOTE    = re.compile(r'(?<![\s\[])(\[\d+\])')
GLUED_RE    = re.compile(r'(?<![A-Za-z])(' + '|'.join(sorted(GLUED, key=len, reverse=True))
                         + r')(?![A-Za-z])') if GLUED else None
CAPTION = re.compile(r'^Artwork opposite by ')
# "<a id="C23"><b>L</b></a><b> E T T E R 2 1</b>" -> the anchor stays on the L,
# the rest loses its letter spacing: "LETTER 21".
LETTER_HEAD = re.compile(r'(<a\s+id="C\d+"><b>L</b></a><b>)((?:\s+[A-Za-z])+)((?:\s+\d)+)(</b>)')

def is_blank(l): return l.strip() == '<br/>'
def core(l):
    s = l.strip()
    return s[:-5] if s.endswith('<br/>') else s
def plain(l):    return html.unescape(re.sub('<[^>]+>', '', core(l))).strip()
def is_content(l): return bool(l.strip()) and not is_blank(l)

def sentence_final(t):
    """Does t read as a finished sentence? Trailing [4] and quotes don't count."""
    prev = None
    while prev != t:
        prev = t
        t = re.sub(r'(\s*\[\d+\])+$', '', t).strip()
        t = re.sub(r'[)\]”’"\'»]+$', '', t).strip()
    return bool(t) and t[-1] in '.!?:'

def fully_bold(l):
    raw = core(l)
    if '<b>' not in raw:
        return False
    rest = re.sub('<[^>]+>', '', re.sub(r'<b>.*?</b>', '', raw, flags=re.S))
    return not re.sub(r'\[\d+\]', '', rest).strip()

def is_letter_heading(l):
    return bool(re.search(r'<a\s+id="C\d+"', l)) and re.match(r'L ?E ?T ?T ?E ?R\b', plain(l))

def ends_hyphenated(raw):
    return re.search(rf'{LETTER}\s*-$', re.sub('<[^>]+>', '', core(raw)).rstrip()) is not None

# ------------------------------------------------------------------ merge ---
def merge(a_line, b_line, stats):
    """Join two halves of one paragraph, healing a word broken at the seam.
    Only text between tags is touched, so markup and URLs survive."""
    indent = re.match(r'\s*', a_line).group(0)
    pa, pb = TOK.split(core(a_line)), TOK.split(core(b_line))
    if ends_hyphenated(a_line):
        cut = False
        for i in range(len(pa) - 1, -1, -1):
            if i % 2:
                continue
            if cut:
                pa[i] = pa[i].rstrip()
                if pa[i]:
                    break
                continue
            t2 = re.sub(r'\s*-\s*$', '', pa[i])
            if t2 != pa[i]:
                cut, pa[i] = True, t2.rstrip()
                if pa[i]:
                    break
            elif pa[i].strip() == '':
                pa[i] = ''
            else:
                break
        for i in range(0, len(pb), 2):
            if pb[i].strip() == '':
                pb[i] = ''
            else:
                pb[i] = pb[i].lstrip()
                break
        sep = ''
        stats['joined_hyphen'] += 1
    else:
        sep = '  '          # the converter renders a wrapped line as two spaces
    a, b = ''.join(pa), ''.join(pb)
    if a.endswith('</b>') and b.startswith('<b>'):
        a, b = a[:-4], b[3:]
    elif a.endswith('</i>') and b.startswith('<i>'):
        a, b = a[:-4], b[3:]
    return indent + a + sep + b + '<br/>'

# --------------------------------------------------- pass 1: page headers ---
def relocate_captions(body, stats):
    """'Artwork opposite by X' gets stranded mid-sentence; put it under its image."""
    for i in [k for k, l in enumerate(body) if CAPTION.match(plain(l))][::-1]:
        imgs = [k for k in range(i) if '<img' in body[k]]
        if not imgs:
            continue
        j, line = imgs[-1], body[i]
        rm = {i, i + 1} if i + 1 < len(body) and is_blank(body[i + 1]) else \
             ({i - 1, i} if is_blank(body[i - 1]) else {i})
        body = [l for k, l in enumerate(body) if k not in rm]
        body[j + 1:j + 1] = [line, '<br/>']
        stats['captions_moved'] += 1
    return body

def strip_headers(body, hdr, stats):
    out, i = [], 0
    while i < len(body):
        if not (is_content(body[i]) and hdr.fullmatch(plain(body[i]))):
            out.append(body[i]); i += 1; continue
        stats['headers_removed'] += 1
        p = len(out) - 1
        while p >= 0 and is_blank(out[p]):
            p -= 1
        n = i + 1
        while n < len(body) and is_blank(body[n]):
            n += 1
        if (p >= 0 and n < len(body) and '<img' not in out[p] and '<img' not in body[n]
                and not sentence_final(plain(out[p]))):
            out[p] = merge(out[p], body[n], stats)
            del out[p + 1:]
            stats['joined_at_header'] += 1
            i = n + 1
        else:                                  # header only; keep the break
            if i + 1 < len(body) and is_blank(body[i + 1]):
                i += 2
            else:
                if out and is_blank(out[-1]):
                    out.pop()
                i += 1
    return out

# ----------------------------------- pass 2: de-hyphenate + rejoin the rest ---
def fix_inline_hyphens(line, stats):
    parts = TOK.split(line)
    for i in range(0, len(parts), 2):
        parts[i], n = INLINE_HYPH.subn(r'\1\2', parts[i])
        stats['hyphens_inline'] += n
    return ''.join(parts)

def fix_words(line, stats):
    """Space out footnote markers and split glued words. Text between tags only,
    so a drop cap in its own <b> never hides half a word and URLs stay intact."""
    parts = TOK.split(line)
    for i in range(0, len(parts), 2):
        parts[i], n = FOOTNOTE.subn(r' \1', parts[i])
        stats['footnotes_spaced'] += n
        if GLUED_RE:
            parts[i], n = GLUED_RE.subn(lambda m: GLUED[m.group(1)], parts[i])
            stats['words_unglued'] += n
    return ''.join(parts)

def joinable(a, b):
    """Conservative: only rejoin when the next line clearly continues a sentence."""
    pa, pb = plain(a), plain(b)
    if not pa or not pb:                        return False
    if '<img' in a or '<img' in b:              return False
    if re.search(r'<a\s+id=', a):               return False   # a chapter heading
    if sentence_final(pa):                      return False
    if not pb[0].islower():                     return False
    if len(pa) < 45 and '  ' not in pa and '<b>' not in a:
        return False        # a standalone short line = displayed verse, not prose
    if len(pb) < 5:                             return False   # verse connector ("or")
    if fully_bold(a) and '<b>' not in b:        return False   # title + byline
    return True

def rejoin(body, stats):
    out = []
    for line in body:
        if not is_content(line):
            out.append(line); continue
        p = len(out) - 1
        while p >= 0 and is_blank(out[p]):
            p -= 1
        if p >= 0 and joinable(out[p], line):
            out[p] = merge(out[p], line, stats)
            del out[p + 1:]
            stats['joined_mid_sentence'] += 1
        else:
            out.append(line)
    return out

# ------------------------------------- pass 3: ornaments + heading spacing ---
def drop_stray_A(body, stats):
    out = []
    for l in body:
        if is_content(l) and plain(l) == 'A':
            stats['ornament_A_removed'] += 1
            if out and is_blank(out[-1]):
                out.pop()
            continue
        out.append(l)
    return out

def tighten_headings(body, stats):
    i = 0
    while i < len(body):
        if is_letter_heading(body[i]):
            j = i + 1
            while j + 1 < len(body) and is_blank(body[j]) and fully_bold(body[j + 1]):
                del body[j]
                stats['headings_tightened'] += 1
                j += 1
        i += 1
    return body

def despace_letter_headings(body, stats):
    """'L E T T E R 2 1' -> 'LETTER 21', keeping the TOC anchor on the L."""
    for i, l in enumerate(body):
        if not is_letter_heading(l):
            continue
        new = LETTER_HEAD.sub(
            lambda m: m.group(1) + re.sub(r'\s+', '', m.group(2)) + ' '
                      + re.sub(r'\s+', '', m.group(3)) + m.group(4), l)
        if new != l:
            body[i] = new
            stats['letter_headings_despaced'] += 1
    return body

# ------------------------------------------------------------------- main ---
def text_files(root):
    d = os.path.join(root, 'OEBPS', 'Text')
    return [os.path.join(d, f) for f in
            sorted(os.listdir(d), key=lambda x: int(re.sub(r'\D', '', x) or 0))
            if f.endswith('.html')]

def list_headers(root):
    c = Counter()
    for path in text_files(root):
        for l in open(path, encoding='utf-8').read().split('\n')[9:-3]:
            if not is_content(l):
                continue
            t = plain(l)
            if len(t) < 90 and (re.match(r'^\d{1,3}\s+\S', t) or re.search(r'\s\d{1,3}$', t)):
                c[re.sub(r'\d+', '#', t)] += 1
    print('Repeating header-shaped lines (# = a page number).')
    print('Anything with a high count is a running header -- add it to HEADER_PATTERNS.')
    print('Leave table-of-contents rows and real headings alone.\n')
    for t, n in c.most_common(40):
        print(f'  {n:4d}  {t}')

def list_glued(root):
    """Print tokens that look like two words run together, for hand review."""
    node = Counter()
    for path in text_files(root):
        for l in open(path, encoding='utf-8').read().split('\n')[9:-3]:
            parts = TOK.split(l)
            for i in range(0, len(parts), 2):
                node.update(re.findall(r"[A-Za-z][A-Za-z\u2019']*", html.unescape(parts[i])))
    freq = Counter()
    for w, n in node.items():
        freq[w.lower()] += n
    try:
        D = set(w.strip().lower() for w in open('/usr/share/dict/words'))
    except OSError:
        sys.exit('no /usr/share/dict/words on this machine; cannot screen real words')
    def real(x):
        x = x.lower()
        return len(x) >= 2 and (x in D or freq[x] >= 8)
    # short words a lost thin space tends to weld to a neighbour
    STICKY = ['common', 'summon', 'many', 'much', 'made', 'whom', 'when', 'what', 'your',
              'who', 'why', 'how', 'you', 'men', 'man', 'may', 'our', 'own', 'and', 'now',
              'god', 'was', 'way', 'one', 'am', 'my', 'me', 'we', 'do', 'on', 'a', 'o']
    def cut(w, d=0):
        for s in STICKY:
            if w.lower().startswith(s) and len(w) > len(s) + 1:
                rest = w[len(s):]
                if real(rest) or re.match(r'^[A-Z]', rest):
                    return [w[:len(s)], rest]
                if d < 2 and (sub := cut(rest, d + 1)):
                    return [w[:len(s)]] + sub
        return None
    found = {}
    for w, n in node.items():
        if len(w) < 5 or '\u2019' in w or "'" in w:
            continue
        if m := re.match(r'^([A-Z]{2,})([a-z].+)$', w):       # NFLin, CEOand
            found[w] = (f'{m.group(1)} {m.group(2)}', n); continue
        if w.lower() in D:
            continue
        if re.search(r'[a-z][A-Z]', w):                        # myGod, whomI
            found[w] = (re.sub(r'([a-z])([A-Z])', r'\1 \2', w), n); continue
        if c := cut(w):
            found[w] = (' '.join(c), n)
    print(f'{len(found)} tokens look glued. REVIEW EVERY LINE before adding to GLUED --')
    print('Latin, Greek and proper nouns land here too, and some splits are wrong.\n')
    for w in sorted(found, key=str.lower):
        rep, n = found[w]
        mark = '  <-- already in GLUED' if w in GLUED else ''
        print(f"    '{w}': '{rep}',{'':{max(0, 34 - len(w) - len(rep))}} # x{n}{mark}")

def run(root, title, stats):
    hdr = re.compile('|'.join(HEADER_PATTERNS))
    docs = []
    for path in text_files(root):
        L = open(path, encoding='utf-8').read().split('\n')
        head, body, tail = L[:9], L[9:-3], L[-3:]
        body = strip_headers(relocate_captions(body, stats), hdr, stats)
        body = rejoin([fix_inline_hyphens(l, stats) for l in body], stats)
        body = [fix_words(l, stats) for l in body]
        body = tighten_headings(drop_stray_A(body, stats), stats)
        body = despace_letter_headings(body, stats)
        docs.append([path, head, body, tail])

    # paragraphs split across the file boundary
    for a, b in zip(docs, docs[1:]):
        ai = max(k for k, l in enumerate(a[2]) if is_content(l))
        bi = min(k for k, l in enumerate(b[2]) if is_content(l))
        if ('<img' in a[2][ai] or '<img' in b[2][bi] or 'id=' in b[2][bi]
                or sentence_final(plain(a[2][ai]))):
            continue
        a[2][ai] = merge(a[2][ai], b[2][bi], stats)
        del a[2][ai + 1:]
        rm = {bi, bi + 1} if bi + 1 < len(b[2]) and is_blank(b[2][bi + 1]) else {bi}
        b[2] = [l for k, l in enumerate(b[2]) if k not in rm]
        stats['joined_across_files'] += 1

    for path, head, body, tail in docs:
        open(path, 'w', encoding='utf-8').write('\n'.join(head + body + tail))

    if title:
        opf = os.path.join(root, 'OEBPS', 'content.opf')
        s = open(opf, encoding='utf-8').read()
        s = re.sub(r'(<dc:title>).*?(</dc:title>)', rf'\g<1>{title}\g<2>', s, flags=re.S)
        open(opf, 'w', encoding='utf-8').write(s)
        ncx = os.path.join(root, 'OEBPS', 'toc.ncx')
        s = open(ncx, encoding='utf-8').read()
        s = re.sub(r'(<docTitle>\s*<text>).*?(</text>)', rf'\g<1>{title}\g<2>', s, flags=re.S)
        open(ncx, 'w', encoding='utf-8').write(s)
        stats['title_set'] = 1

def repack(root, dest):
    """mimetype must be the first entry and stored uncompressed."""
    if os.path.exists(dest):
        os.remove(dest)
    with zipfile.ZipFile(dest, 'w') as z:
        z.write(os.path.join(root, 'mimetype'), 'mimetype', zipfile.ZIP_STORED)
        for base, _, files in os.walk(root):
            for f in sorted(files):
                full = os.path.join(base, f)
                rel  = os.path.relpath(full, root)
                if rel == 'mimetype':
                    continue
                z.write(full, rel, zipfile.ZIP_DEFLATED)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dest', nargs='?')
    ap.add_argument('--title')
    ap.add_argument('--list-headers', action='store_true')
    ap.add_argument('--list-glued', action='store_true')
    a = ap.parse_args()

    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(a.src) as z:
            z.extractall(tmp)
        if a.list_headers:
            list_headers(tmp)
            return
        if a.list_glued:
            list_glued(tmp)
            return
        if not a.dest:
            sys.exit('need a destination .epub (or pass --list-headers / --list-glued)')
        stats = Counter()
        run(tmp, a.title, stats)
        repack(tmp, a.dest)
        for k in ('headers_removed', 'joined_at_header', 'captions_moved',
                  'joined_across_files', 'hyphens_inline', 'joined_mid_sentence',
                  'joined_hyphen', 'ornament_A_removed', 'headings_tightened',
                  'letter_headings_despaced', 'footnotes_spaced', 'words_unglued',
                  'title_set'):
            print(f'  {k:22} {stats[k]}')
        print(f'\nwrote {a.dest}')
    finally:
        shutil.rmtree(tmp)

if __name__ == '__main__':
    main()
