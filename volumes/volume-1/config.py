"""Volume 1 of The Tao of Seneca.

Both tables are specific to this volume. The running headers name the volume
and its sections; the glued-word table was built by reading every candidate
--list-glued proposed and throwing out the wrong ones.
"""

# Running page headers, matched against a whole line (re.fullmatch).
HEADER_PATTERNS = [
    r'\d+ THE TAO OF SENECA \| VOLUME \d+',
    r'MORaL LETTERS TO LUCILIUS \d+',
    r'THOUGHTS FROM MODERN STOICS \| .+? \d+',
    r'PROFILES OF MODERN-Day STOICS FROM TOOLS OF TITaNS \d+',
    r'\d+ BOOkS ON STOICISM \d+',
    r'FOREwORD: HOw TO USE THIS BOOk \d+',
]

# Words the converter ran together where the PDF had a thin space.
# HAND-REVIEWED: the heuristics that propose these also flag Latin, Greek and
# proper nouns ("Hecato" is not "He cato", "publicam" is not "public am").
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
