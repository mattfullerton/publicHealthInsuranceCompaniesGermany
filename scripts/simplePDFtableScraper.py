# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree
import lxml.html
import time
from urlparse import urlparse

# 2. The URL/web address where we can find the PDF we want to scrape
url = 'http://88.215.113.168/krankenkassenliste.pdf'

# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
#print lxml.etree.tostring(root, pretty_print=True)

# 5. How many pages in the PDF document?
pages = list(root)
#print "There are",len(pages),"pages"

# 6. We can use the positioning attibutes in the XML data to help us regenerate the rows and columns
text = ''
lastTag = 2
recordNo = 0
data = [] #array of records (rows)
temp = [] #each row, added once complete

for page in pages:
    for el in page:
        if el.tag == "text":
            if int(el.attrib['left']) < 61:
                if (lastTag <> 0):
                    #Add the complete last column entry
                    temp.append(text)
                    #Add the record
                    data.append(temp)
                    #clear
                    text = ''
                    temp = []
                    #Add to record
                    lastTag = 0
                else: text += ' '
                text += el.text
                
            elif int(el.attrib['left']) < 328:
                if (lastTag <> 1):
                    temp.append(text) #add the complete last column
                    text = ''
                    lastTag = 1
                text += el.text
            else:
                if (lastTag <> 2):
                    lastTag = 2;
                    #Add the complete last column entry
                    temp.append(text)
                    text = '' #clear
                else: text += ' '
                text += el.text
                #data[recordNo][1] = text #(re)write entry

for entry in data:
    if ((len(entry) == 3) and ('Homepage' not in entry[1]) and ('essanelle' not in entry[1])):
        url = "http://" + entry[1] + '/'
        print 'Trying ' + url
        try:
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            for el in root.cssselect("a"):           
                if "mpressum" in unicode(el.text):
                    o = urlparse(url) #In case there is a path at the end
                    finallink = ''
                    if ('http' in str(el.attrib['href'])): #absolute link
                        finallink = str(el.attrib['href'])
                    elif (str(el.attrib['href'])[0] == '/'): #link relative to root
                        finallink = o.scheme + '://' + o.netloc + str(el.attrib['href'])
                    else: #relative link
                        finallink = str(url) + str(el.attrib['href'])
                    entry.append(finallink)
                    print 'Got ' + finallink + ', trying to get email'
                    html = scraperwiki.scrape(finallink)
                    root = lxml.html.fromstring(html)
                    for el in root.cssselect("a"):
                        if 'href' in el.attrib:
                            '''
                            print 'Parsing'
                            try:
                                o = urlparse(el.attrib['href'])
                            except (ValueError, urllib2.HTTPError) as e:
                                print "Invalid link... ignoring\n"
                            if (o.scheme == 'mailto'):
                                entry.append(str(o.netloc))
                                print 'Got ' + str(o.netloc)
                                break #done, don't want any others
                            '''
                        if (('@' in unicode(el.text)) or ('(at)' in unicode(el.text)) or (' at ' in unicode(el.text))):
                                entry.append(el.text)
                                print 'Got ' + str(el.text)
                                break #done, don't want any others
                    break #done, don't want any others
            #print lxml.html.tostring(root, pretty_print=True)
        except (ValueError, urllib2.HTTPError) as e:
            print "Invalid link\n"
        #except lxml.etree.XMLSyntaxError:
            #print "Webpage unparseable\n"

output = ''

for record in data:
    output += '\n'
    for col in record:
        output += (col + ';')

print output


