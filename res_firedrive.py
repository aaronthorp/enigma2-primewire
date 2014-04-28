#putlocker / firedrive resolver
import urllib, urllib2, re

def gethtml(url, data ='', referer = ''):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Host', url.split("/")[2])

    if not referer == '':
        req.add_header('Referer', referer)
    if data == '':
        response = urllib2.urlopen(req)
    else:
        response = urllib2.urlopen(req, data)     
    htmldoc = str(response.read())
    response.close()
    return htmldoc 

def resolve(url):
    url = url.replace("putlocker", "firedrive")
    html = gethtml(url)
    confirm = re.search('<input type="hidden" name="confirm" value="(.+?)"/>', html).group(1)
    data = "confirm=" + urllib.quote_plus(confirm)
    html = gethtml(url,data)
    #print html
    link = re.search('<a href="(.+?)" target="_blank" id=\'top_external_download\' title=\'Download This File\'><i></i>Download</a>', html).group(1)
    return link
