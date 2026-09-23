"""Volume 2 of The Tao of Seneca.

Differences from volume 1, both found with --list-headers:
  * "pROFILES" is spelled with a lowercase p in this volume's headers.
  * Volume 2 ends with a sample of volume 3, which carries its own running
    header ("MORaL LETTERS TO LUCILIUS | VOLUME 3 SaMpLE 281").
Volume 2 has no "28 BOOkS ON STOICISM" or foreword sections.
"""

HEADER_PATTERNS = [
    r'\d+ THE TAO OF SENECA \| VOLUME \d+',
    r'MORaL LETTERS TO LUCILIUS \| VOLUME \d+ SaMpLE \d+',
    r'MORaL LETTERS TO LUCILIUS \d+',
    r'THOUGHTS FROM MODERN STOICS \| .+? \d+',
    r'[pP]ROFILES OF MODERN-Day STOICS FROM TOOLS OF TITaNS \d+',
]

# HAND-REVIEWED. Kept out on purpose: "godbrother", "Aethiopian", "manet" and
# "Metam." (Ovid) are real; "WilliamBIrvine" is the domain williambirvine.com.
# "mea" is deliberately absent -- it appears 3 times, twice glued ("saved mea
# lot of time") and once as real Latin ("quid, mea cum pugnat sententia"), and
# the table matches whole tokens, so splitting it would corrupt the Latin.
GLUED = {
    'Abrief': 'A brief', 'Acure': 'A cure', 'Adwarf': 'A dwarf', 'Agood': 'A good',
    'amashamed': 'am ashamed', 'ambeing': 'am being', 'amcoming': 'am coming',
    'amnot': 'am not', 'Andthe': 'And the', 'Andwhat': 'And what', 'Andwhy': 'And why',
    'Andyet': 'And yet', 'Ashort': 'A short', 'Atrue': 'A true',
    'commonattribute': 'common attribute', 'commonherd': 'common herd',
    'commonsort': 'common sort', 'CUNYsalary': 'CUNY salary', 'Donot': 'Do not',
    'Doyou': 'Do you', 'Howfeather': 'How feather', 'Howoften': 'How often',
    'manalso': 'man also', 'manand': 'man and', 'mancan': 'man can', 'mandoes': 'man does',
    'manexcept': 'man except', 'manfrom': 'man from', 'manhappier': 'man happier',
    'manhas': 'man has', 'manhave': 'man have', 'manmay': 'man may', 'manwas': 'man was',
    'manwho': 'man who', 'manwhois': 'man who is', 'manwhompoverty': 'man whom poverty',
    'manwill': 'man will', 'meand': 'me and', 'mearound': 'me around',
    'meconcerning': 'me concerning', 'mekindly': 'me kindly', 'menis': 'men is',
    'menot': 'me not', 'mensay': 'men say', 'menteach': 'men teach',
    'menthink': 'men think', 'menwho': 'men who', 'Menwho': 'Men who',
    'menwhowould': 'men who would', 'meover': 'me over', 'methat': 'me that',
    'methe': 'me the', 'muchmore': 'much more', 'muchto': 'much to',
    'myassistance': 'my assistance', 'myattention': 'my attention',
    'mybrother': 'my brother', 'mycurtain': 'my curtain', 'mydaily': 'my daily',
    'mydear': 'my dear', 'Mydoor': 'My door', 'myentire': 'my entire',
    'myestimation': 'my estimation', 'myformer': 'my former', 'myfriends': 'my friends',
    'myinterview': 'my interview', 'Mykids': 'My kids', 'myletters': 'my letters',
    'mylife': 'my life', 'myown': 'my own', 'mypresent': 'my present',
    'myreading': 'my reading', 'myriches': 'my riches', 'mysaying': 'my saying',
    'Mysecond': 'My second', 'mystate': 'my state', 'mythoughts': 'my thoughts',
    'MyVirginity': 'My Virginity', 'mywords': 'my words', 'Nowall': 'Now all',
    'NowI': 'Now I', 'Nowif': 'Now if', 'Nowthe': 'Now the', 'Nowthis': 'Now this',
    'Onanother': 'On another', 'Onthe': 'On the', 'Ontop': 'On top',
    'onyourself': 'on yourself', 'OVERALLout': 'OVERALL out', 'Owhat': 'O what',
    'Weare': 'We are', 'Weconsider': 'We consider', 'Weget': 'We get', 'Wehave': 'We have',
    'Weknow': 'We know', 'Wemay': 'We may', 'Wemeet': 'We meet', 'Wemust': 'We must',
    'Weought': 'We ought', 'Weshall': 'We shall', 'Weshould': 'We should',
    'Wespeak': 'We speak', 'WeStoics': 'We Stoics', 'WhenLibo': 'When Libo',
    'Whenthe': 'When the', 'Whenthis': 'When this', 'Whenwill': 'When will',
    'whoare': 'who are', 'whois': 'who is', 'whomcruelty': 'whom cruelty',
    'whomhe': 'whom he', 'whomthey': 'whom they', 'whomwere': 'whom were',
    'whoowe': 'who owe', 'whoregard': 'who regard', 'whowill': 'who will',
    'Whyneed': 'Why need', 'Whyshould': 'Why should', 'Whytry': 'Why try',
    'XVSeneca': 'XV Seneca', 'XXVis': 'XXV is'
}
