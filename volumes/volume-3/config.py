"""Volume 3 of The Tao of Seneca.

Differences from volume 1, both found with --list-headers:
  * Volume 3 carries the back-matter indexes, which have their own running
    headers ("INDEx OF PROPER NaMES 285", "SUbjECT INDEx 307").
  * Inside those indexes the header loses its page number entirely, appearing
    as a bare "THE TAO OF SENECA | VOLUME 3" -- hence the optional prefix.
Volume 3 also reaches letter 124, so headings run to three spaced digits
("L E T T E R 1 0 0"); the despacing handles any digit count.
"""

HEADER_PATTERNS = [
    r'(?:\d+ )?THE TAO OF SENECA \| VOLUME \d+',
    r'MORaL LETTERS TO LUCILIUS \d+',
    r'THOUGHTS FROM MODERN STOICS \| .+? \d+',
    r'[pP]ROFILES OF MODERN-Day STOICS FROM TOOLS OF TITaNS \d+',
    r'INDEx OF PROPER NaMES \d+',
    r'SUbjECT INDEx \d+',
]

# HAND-REVIEWED. Kept out on purpose: "@RyanHoliday" and "@SteveHanselman" are
# Twitter handles, "Silence Dogood" is Franklin's pseudonym, "Manilian" (Law)
# and "Asinus" (Gallus) are proper names, and "abest"/"aquis"/"Mecum" are Latin.
GLUED = {
    'Adifferent': 'A different', 'Agood': 'A good', 'Alecturer': 'A lecturer',
    'Amanis': 'A man is', 'amnot': 'am not', 'amoften': 'am often', 'amstill': 'am still',
    'Andif': 'And if', 'Andin': 'And in', 'Andwhat': 'And what', 'Andwhen': 'And when',
    'Areply': 'A reply', 'Asecond': 'A second', 'Awrongdoer': 'A wrongdoer',
    'Doyou': 'Do you', 'Godis': 'God is', 'HOWARNOLD': 'HOW ARNOLD', 'Howcan': 'How can',
    'howfalse': 'how false', 'Howgentleness': 'How gentleness', 'howhe': 'how he',
    'Howjoy': 'How joy', 'Howmany': 'How many', 'howmuchmore': 'how much more',
    'Howoften': 'How often', 'Howsternness': 'How sternness', 'manand': 'man and',
    'manbe': 'man be', 'mancan': 'man can', 'mancould': 'man could', 'manrich': 'man rich',
    'manwho': 'man who', 'meand': 'me and', 'mehow': 'me how', 'memore': 'me more',
    'menare': 'men are', 'menfearful': 'men fearful', 'menfrom': 'men from',
    'menwho': 'men who', 'menwhowere': 'men who were', 'merather': 'me rather',
    'mestretch': 'me stretch', 'metell': 'me tell', 'mewhat': 'me what', 'mewhy': 'me why',
    'mybattered': 'my battered', 'mydear': 'my dear', 'myexistence': 'my existence',
    'myfinal': 'my final', 'myfirst': 'my first', 'myfriends': 'my friends',
    'mymind': 'my mind', 'mynetwork': 'my network', 'myown': 'my own',
    'mypresent': 'my present', 'myprevious': 'my previous', 'mypromise': 'my promise',
    'myremark': 'my remark', 'myspirit': 'my spirit', 'mystomach': 'my stomach',
    'mysubject': 'my subject', 'myvilla': 'my villa', 'myvision': 'my vision',
    'mywhole': 'my whole', 'mywriting': 'my writing', 'Nowevery': 'Now every',
    'Onthat': 'On that', 'Onthis': 'On this', 'Owhat': 'O what', 'ownneeds': 'own needs',
    'OWNOR': 'OWN OR', 'ownwell': 'own well', 'Weabandon': 'We abandon', 'weare': 'we are',
    'Wecan': 'We can', 'Wecontinually': 'We continually', 'Wehave': 'We have',
    'Wehunt': 'We hunt', 'Weknow': 'We know', 'Wemay': 'We may', 'Wemiss': 'We miss',
    'Wemust': 'We must', 'Wesee': 'We see', 'Weshall': 'We shall', 'Weshould': 'We should',
    'Weunderstood': 'We understood', 'Wewould': 'We would', 'Whatyou': 'What you',
    'WhenSotion': 'When Sotion', 'Whenthe': 'When the', 'whodo': 'who do',
    'Whodoes': 'Who does', 'Whois': 'Who is', 'whois': 'who is', 'whomhe': 'whom he',
    'whommany': 'whom many', 'whomwe': 'whom we', 'whomwere': 'whom were',
    'whomyou': 'whom you', 'whoraise': 'who raise', 'Whybe': 'Why be', 'Whydo': 'Why do',
    'Whydress': 'Why dress', 'Whyneed': 'Why need', 'Whyshould': 'Why should'
}
