# -*- coding: utf-8 -*-

import scraperwiki
import lxml.html
import requests
import urlparse
from dateutil import parser
from dateutil.parser import parserinfo

BASE_URL = "http://www.reykjavik.is"
DATA_URL = "http://reykjavik.is/fundargerdir?page=0"

class Icelandic(parserinfo):
    def __init__(self):
        self.WEEKDAYS = [(u"Mán", u"Mánudagur"),
                         (u"Þri", u"Þriðjudagur"),
                         (u"Mið", u"Miðvikudagur"),
                         (u"Fim", u"Fimmtudagur"),
                         (u"Fös", u"Föstudagur"),
                         (u"Lau", u"Laugardagur"),
                         (u"Sun", u"Sunnudagur")]
        self.MONTHS = [(u"Jan", u"janúar"),
                       (u"Feb", u"febrúar"),
                       (u"Mar", u"mars"),
                       (u"Apr", u"apríl"),
                       (u"maí", u"maí"),
                       (u"jún", u"júní"),
                       (u"júl", u"júlí"),
                       (u"ágú", u"ágúst"),
                       (u"sep", u"september"),
                       (u"okt", u"október"),
                       (u"nov", u"nóvember"),
                       (u"des", u"desember")]
        parserinfo.__init__(self)

    def __call__(self):
        return self


icelandic_dateutil_parserinfo = Icelandic()

r = requests.get(DATA_URL)
root = lxml.html.fromstring(r.text)

items = root.xpath("//div[@class='item-wrapper']")

data = []
for item in items:
    meeting = {}
    title = item.xpath("div[@class='views-field views-field-title col-xs-12 col-sm-4 d-nog']/span/a")[0]
    date = item.xpath("div[@class='views-field views-field-field-dagsetning-fundar col-xs-12 col-sm-4']/div/span")[0]
    committee = item.xpath("div[@class='views-field views-field-field-rad-nefnd col-xs-12 col-sm-4']/div")[0]
    meeting["titill"] = title.text
    meeting["url"] = urlparse.urljoin(BASE_URL, title.attrib["href"])
    meeting["dagsetning"] = date.text
    meeting["date"] = parser.parse(date.attrib["content"], ignoretz=True)
    meeting["nefnd"] = committee.text
    data.append(meeting)
scraperwiki.sqlite.save(unique_keys=['url'],
                        data=data)
