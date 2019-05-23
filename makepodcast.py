import sys
import csv
import codecs
import urllib2
import re
from feedgen.feed import FeedGenerator

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


def main():
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.id('https://lbragaglia.github.io/qpodcast/feed.xml')
    fg.title('Luther Blisset - Q')
    fg.description('Il romanzo "Q" di Luther Blisset, letto da Marco Meacci')
    fg.author({'name':'Luther Blisset'})
    fg.contributor({'name':'Marco Meacci'})
    fg.logo('https://www.einaudi.it/content/uploads/2010/01/978880620050GRA.JPG')
    fg.link(href='https://lbragaglia.github.io/qpodcast/feed.xml', rel='self')
    fg.link(href='https://lbragaglia.github.io/qpodcast/', rel='alternate')
    fg.language('it')

    indexre = re.compile(r'\d\d\d - ')
    filereader = UnicodeReader(sys.stdin)
    for row in filereader:
        title = row[1].rsplit('.', 1)[0]
        url = 'https://lbragaglia.github.io/qpodcast/' + urllib2.quote(row[1].encode("utf8"))
        fe = fg.add_entry(order='append')
        fe.id(row[1])
        fe.title(title)
        fe.description(indexre.sub('', title))
        fe.author({'name':row[2]})
        fe.pubDate(row[3])
        fe.enclosure(url, row[4], 'audio/mpeg')
    
    sys.stdout.write(fg.rss_str(pretty=True))
    sys.stdout.flush()
    sys.exit(0)

if __name__ == '__main__':
    main()
