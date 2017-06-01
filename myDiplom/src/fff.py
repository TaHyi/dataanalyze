from __future__ import with_statement   # Not required in Python 2.6 any more

import codecs

p = u"абвгдежзийкл"  # note the 'u' prefix

print (p)   # probably won't work on Windows due to a complex issue

with codecs.open("tets.csv", "w", "utf-16") as stream:   # or utf-8
    stream.write(p + u"\n")
# import csv
#
# tests={'German': [u'Straße',u'auslösen',u'zerstören'],
#        'French': [u'français',u'américaine',u'épais'],
#        'Chinese': [u'中國的',u'英語',u'美國人']}
#
# with open('utf.csv','w') as fout:
#     writer=csv.writer(fout)
#     writer.writerows([tests.keys()])
#     for row in zip(*tests.values()):
#         row=[s.encode('utf-8-sig') for s in row]
#         writer.writerows([row])

# with open('utf.csv','r') as fin:
#     reader=csv.reader(fin)
#     for row in reader:
#         temp=list(row)
#         fmt=u'{:<15}'*len(temp)
#         print(fmt.format(*[s.decode('utf-8') for s in temp]))