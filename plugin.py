#Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/1channel/plugin.py
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.InfoBar import MoviePlayer as MP_parent
from Screens.InfoBar import InfoBar
from Screens.MessageBox import MessageBox
from ServiceReference import ServiceReference
from enigma import eServiceReference
from enigma import eConsoleAppContainer
from enigma import ePicLoad
from enigma import getDesktop
from enigma import eServiceCenter
from Components.MenuList import MenuList
from Screens.MessageBox import MessageBox
from Components.Input import Input
from Screens.InputBox import InputBox
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from cookielib import CookieJar
import urllib
import urllib2
import re
import time
import os
from urllib2 import Request
from urllib2 import urlopen
from urllib2 import URLError
from urllib2 import HTTPError

class ShowHelp(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    skin = '\n        <screen position="100,150" size="' + str(wsize) + ',' + str(hsize) + '" title="1channel" >\n        <widget name="myLabel" position="10,10" size="' + str(wsize - 20) + ',' + str(hsize - 20) + '" font="Console;18" />\n        </screen>'

    def __init__(self, session, args = None):
        self.session = session
        Screen.__init__(self, session)
        text = '\nAbout:\n\nPlugin modified by oRiCLe 24/04/2014'
        self['myLabel'] = ScrollLabel(text)
        self['myActionMap'] = ActionMap(['WizardActions', 'SetupActions', 'ColorActions'], {'cancel': self.close,
         'down': self['myLabel'].pageDown,
         'ok': self.close,
         'up': self['myLabel'].pageUp}, -1)


class MyMenux(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    skin = '\n        <screen position="100,150" size="' + str(wsize) + ',' + str(hsize) + '" title="1channel" >\n        <widget name="myMenu" position="10,10" size="' + str(wsize - 20) + ',' + str(hsize - 20) + '" scrollbarMode="showOnDemand" />\n        </screen>'

    def __init__(self, session, action, value):
        self.session = session
        self.action = action
        self.value = value
        osdList = []
        if self.action is 'start':
            osdList.append((_('Movies A-Z'), 'movie'))
            osdList.append((_('Featured Movies'), 'movie2'))
            osdList.append((_('Featured Movies By Genre'), 'genre'))
            osdList.append((_('Just Added Movies'), 'movie3'))
            osdList.append((_('\n'), ''))
            osdList.append((_('TV Shows A-Z'), 'tvshow'))
            osdList.append((_('Featured TV Shows'), 'tvshow3'))
            osdList.append((_('Featured TV Shows By Genre'), 'genre2'))
            osdList.append((_('Just Added TV Shows'), 'tvshow2'))
            osdList.append((_('\n'), ''))
            osdList.append((_('Kill All Downloads'), 'kill'))
        elif self.action is 'genre' or self.action is 'genre2':
            osdList = [('Action', 'Action'),
             ('Adventure', 'Adventure'),
             ('Animation', 'Animation'),
             ('Biography', 'Biography'),
             ('Comedy', 'Comedy'),
             ('Crime', 'Crime'),
             ('Documentary', 'Documentary'),
             ('Drama', 'Drama'),
             ('Family', 'Family'),
             ('Fantasy', 'Fantasy'),
             ('Game-Show', 'Game-Show'),
             ('History', 'History'),
             ('Horror', 'Horror'),
             ('Japanese', 'Japanese'),
             ('Korean', 'Korean'),
             ('Music', 'Music'),
             ('Musical', 'Musical'),
             ('Mystery', 'Mystery'),
             ('Reality-TV', 'Reality-TV'),
             ('Romance', 'Romance'),
             ('Sci-Fi', 'Sci-Fi'),
             ('Short', 'Short'),
             ('Sport', 'Sport'),
             ('Talk-Show', 'Talk-Show'),
             ('Thriller', 'Thriller'),
             ('War', 'War'),
             ('Western', 'Western'),
             ('Zombies', 'Zombies')]
        elif self.action is 'movie' or 'tvshow':
            osdList = [(' --- 123 --- ', '123'),
             (' ---- A ---- ', 'a'),
             (' ---- B ---- ', 'b'),
             (' ---- C ---- ', 'c'),
             (' ---- D ---- ', 'd'),
             (' ---- E ---- ', 'e'),
             (' ---- F ---- ', 'f'),
             (' ---- G ---- ', 'g'),
             (' ---- H ---- ', 'h'),
             (' ----  I  ---- ', 'i'),
             (' ---- J ---- ', 'j'),
             (' ---- K ---- ', 'K'),
             (' ---- L ---- ', 'l'),
             (' ---- M ---- ', 'm'),
             (' ---- N ---- ', 'n'),
             (' ---- O ---- ', 'o'),
             (' ---- P ---- ', 'p'),
             (' ---- Q ---- ', 'q'),
             (' ---- R ---- ', 'r'),
             (' ---- S ---- ', 's'),
             (' ---- T ---- ', 't'),
             (' ---- U ---- ', 'u'),
             (' ---- V ---- ', 'v'),
             (' ---- W ---- ', 'w'),
             (' ---- X ---- ', 'x'),
             (' ---- Y ---- ', 'y'),
             (' ---- Z ---- ', 'z'),
             ('Search', 'search')]
        elif self.action is 'page':
            print '########PMOVIE#################' + self.value
            page = self.value
            url = 'http://www.primewire.ag/index.php?letter=' + page + '&sort=alphabet&page=1'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile('<a href="/index.php\\?letter=.+?&sort=alphabet&page=([0-9]*)"> >> </a>').findall(htmlDoc)
            for page in range(int(pages[0]) / 5):
                page = int(page + 1) * 5
                osdList.append((_('Page ' + str(page - 4) + ' - ' + str(page)), 'page'))

        osdList.append((_('Help & About'), 'help'))
        osdList.append((_('Exit'), 'exit'))
        Screen.__init__(self, session)
        self['myMenu'] = MenuList(osdList)
        self['myActionMap'] = ActionMap(['SetupActions'], {'cancel': self.cancel,
         'ok': self.go}, -1)

    def go(self):
        returnValue = self['myMenu'].l.getCurrentSelection()[1]
        returnValue2 = self['myMenu'].l.getCurrentSelection()[1] + ',' + self['myMenu'].l.getCurrentSelection()[0]
        if returnValue is 'help':
            self.session.open(ShowHelp)
        elif returnValue is 'exit':
            self.close(None)
        elif self.action is 'start':
            if returnValue is 'movie':
                self.session.open(MyMenux, 'movie', '0')
            elif returnValue is 'movie2':
                self.session.open(MyMenu2, 'movie2', '0')
            elif returnValue is 'movie3':
                self.session.open(MyMenu2, 'movie3', '0')
            elif returnValue is 'genre':
                self.session.open(MyMenux, 'genre', '0')
            elif returnValue is 'tvshow':
                self.session.open(MyMenux, 'tvshow', '0')
            elif returnValue is 'tvshow2':
                self.session.open(MyMenu2, 'tvshow2', '0')
            elif returnValue is 'tvshow3':
                self.session.open(MyMenu2, 'tvshow3', '0')
            elif returnValue is 'genre2':
                self.session.open(MyMenux, 'genre2', '0')
            elif returnValue is 'kill':
                os.system('killall -9 wget')
        elif self.action is 'genre':
            if returnValue is 'search':
                print 'search'
                self.Search1()
            else:
                value = returnValue
                self.session.open(MyMenu2, 'genre', value)
        elif self.action is 'genre2':
            if returnValue is 'search':
                print 'search'
                self.Search1()
            else:
                value = returnValue
                self.session.open(MyMenu2, 'genre2', value)
        elif self.action is 'movie':
            if returnValue is 'search':
                print 'search'
                self.Search1()
            else:
                value = returnValue
                self.session.open(MyMenu2, 'movie', value)
        elif self.action is 'tvshow':
            if returnValue is 'search':
                print 'search'
                self.Search2()
            else:
                value = returnValue
                self.session.open(MyMenu2, 'tvshow', value)
        return

    def Search1(self):
        self.session.openWithCallback(self.askForWord1, InputBox, maxSize=55, text=' ' * 55, title=_('Search:'), type=Input.TEXT)

    def askForWord1(self, returnValue):
        if returnValue is not None:
            value = 'search ' + returnValue
            self.session.open(MyMenu2, 'movie', value)
        return

    def Search2(self):
        self.session.openWithCallback(self.askForWord2, InputBox, maxSize=55, text=' ' * 55, title=_('Search:'), type=Input.TEXT)

    def askForWord2(self, returnValue):
        if returnValue is not None:
            value = 'search ' + returnValue
            self.session.open(MyMenu2, 'tvshow', value)
        return

    def cancel(self):
        self.close(None)
        return


class MyMenu2(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    skin = '\n        <screen position="100,150" size="' + str(wsize) + ',' + str(hsize) + '" title="1channel" >\n        <widget name="myMenu" position="10,10" size="' + str(wsize - 20) + ',' + str(hsize - 20) + '" scrollbarMode="showOnDemand" />\n        </screen>'

    def __init__(self, session, action, value):
        self.session = session
        self.action = action
        self.value = value
        osdList = []
        if self.action is 'movie':
            if value.find('search') > -1:
                value = value[7:]
                value = str(value.strip())
                print value
                value = str(value.replace(' ', '+'))
                print value
                url = 'http://www.primewire.ag/index.php'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc)
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey[0] + '&sort=alphabet&search_section=1'
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = 'search-' + value + '-' + searchkey[0]
            else:
                page = self.value
                url = 'http://www.primewire.ag/index.php?letter=' + page + '&sort=alphabet&page=1'
                restring = '<a href="/index.php\\?letter=.+?&sort=alphabet&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile(restring).findall(htmlDoc)
        if self.action is 'movie2':
            if value.find('search') > -1:
                value = value[7:]
                value = str(value.strip())
                print value
                value = str(value.replace(' ', '+'))
                print value
                url = 'http://www.primewire.ag/index.php'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc)
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey[0] + '&sort=alphabet&search_section=1'
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = 'search-' + value + '-' + searchkey[0]
            else:
                page = self.value
                url = 'http://www.primewire.ag/index.php?' + page + '&sort=featured&page=1'
                restring = '<a href="/index.php\\?.+?&sort=featured&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile(restring).findall(htmlDoc)
        if self.action is 'movie3':
            if value.find('search') > -1:
                value = value[7:]
                value = str(value.strip())
                print value
                value = str(value.replace(' ', '+'))
                print value
                url = 'http://www.primewire.ag/index.php'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc)
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey[0] + '&sort=alphabet&search_section=1'
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = 'search-' + value + '-' + searchkey[0]
            else:
                page = self.value
                url = 'http://www.primewire.ag/index.php?' + page + '&page=1'
                restring = '<a href="/index.php\\?.+?&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile(restring).findall(htmlDoc)
        if self.action is 'genre':
            if value.find('search') > -1:
                value = value[7:]
                value = str(value.strip())
                print value
                value = str(value.replace(' ', '+'))
                print value
                url = 'http://www.primewire.ag/index.php'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc)
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey[0] + '&sort=alphabet&search_section=1'
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = 'search-' + value + '-' + searchkey[0]
            else:
                page = self.value
                url = 'http://www.primewire.ag/index.php?genre=' + page + '&sort=featured&page=1'
                restring = '<a href="/index.php\\?genre=.+?&sort=featured&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile(restring).findall(htmlDoc)
        if self.action is 'tvshow':
            if value.find('search') > -1:
                value = value[7:]
                value = str(value.strip())
                print value
                value = str(value.replace(' ', '+'))
                print value
                url = 'http://www.primewire.ag/index.php?tv='
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc)
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey[0] + '&sort=alphabet&search_section=2'
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = 'search-' + value + '-' + searchkey[0]
            else:
                page = self.value
                url = 'http://www.primewire.ag/index.php?letter=' + page + '&tv=&sort=alphabet&page=1'
                restring = '<a href="/index.php\\?letter=.+?&tv=&sort=alphabet&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile(restring).findall(htmlDoc)
        if self.action is 'tvshow2':
            if value.find('search') > -1:
                value = value[7:]
                value = str(value.strip())
                print value
                value = str(value.replace(' ', '+'))
                print value
                url = 'http://www.primewire.ag/index.php?tv='
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc)
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey[0] + '&sort=alphabet&search_section=2'
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = 'search-' + value + '-' + searchkey[0]
            else:
                page = self.value
                url = 'http://www.primewire.ag/index.php?tv=' + page + '&page=1'
                restring = '<a href="/index.php\\?tv=.+?&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile(restring).findall(htmlDoc)
        if self.action is 'tvshow3':
            if value.find('search') > -1:
                value = value[7:]
                value = str(value.strip())
                print value
                value = str(value.replace(' ', '+'))
                print value
                url = 'http://www.primewire.ag/index.php'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc)
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey[0] + '&sort=alphabet&search_section=1'
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = 'search-' + value + '-' + searchkey[0]
            else:
                page = self.value
                url = 'http://www.primewire.ag/index.php?tv=' + page + '&sort=featured&page=1'
                restring = '<a href="/index.php\\?tv=.+?&sort=featured&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile(restring).findall(htmlDoc)
        if self.action is 'genre2':
            if value.find('search') > -1:
                value = value[7:]
                value = str(value.strip())
                print value
                value = str(value.replace(' ', '+'))
                print value
                url = 'http://www.primewire.ag/index.php'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                searchkey = re.compile('<input type="hidden" name="key" value="(.+?)" />').findall(htmlDoc)
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey[0] + '&sort=alphabet&search_section=1'
                print htmlDoc
                restring = '<a href=.+?&page=([0-9]*)"> >> </a>'
                self.value = 'search-' + value + '-' + searchkey[0]
            else:
                page = self.value
                url = 'http://www.primewire.ag/index.php?tv=&genre=' + page + '&sort=featured&page=1'
                restring = '<a href="/index.php\\?tv=&genre=.+?&sort=featured&page=([0-9]*)"> >> </a>'
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            pages = re.compile(restring).findall(htmlDoc)
        if not pages:
            pages = ['1']
        page_x = 0
        for page in range(int(pages[0]) / 5):
            page = int(page + 1) * 5
            if page < int(pages[0]):
                page_str = str(page - 4) + ' - ' + str(page)
                osdList.append((_('Page ' + page_str), self.value + ',' + page_str))
                page_x = page
                continue

        if int(pages[0]) - page_x is 1 or 2 or 3 or 4:
            page_str = str(page_x + 1) + ' - ' + pages[0]
            osdList.append((_('Page ' + page_str), self.value + ',' + page_str))
        osdList.append((_('Help & About'), 'help'))
        osdList.append((_('Exit'), 'exit'))
        Screen.__init__(self, session)
        self['myMenu'] = MenuList(osdList)
        self['myActionMap'] = ActionMap(['SetupActions'], {'cancel': self.cancel,
         'ok': self.go}, -1)

    def go(self):
        returnValue = self['myMenu'].l.getCurrentSelection()[1]
        if returnValue is 'help':
            self.session.open(ShowHelp)
        elif returnValue is 'exit':
            self.close(None)
        else:
            value = returnValue
            self.session.open(MovieList, self.action, value)
            print value
        return

    def cancel(self):
        self.close(None)
        return


class MovieList(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    skin = '\n        <screen position="100,150" size="' + str(wsize) + ',' + str(hsize) + '" title="1channel (green button Subtitle player)" >\n        <widget name="myMenu" position="10,10" size="' + str(wsize - 20) + ',' + str(hsize - 20) + '" scrollbarMode="showOnDemand" />\n        </screen>'

    def __init__(self, session, action, value):
        self.session = session
        self.action = action
        self.value = value
        osdList = []
        if self.action is 'movie':
            self.value = self.value.split(',')
            if self.value[0].find('search') > -1:
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey + '&search_section=1&sort=alphabet&page='
            else:
                letter = self.value[0]
                url = 'http://www.primewire.ag/index.php?letter=' + letter + '&sort=alphabet&page='
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range(pages):
                page = int(page_a)
                page_a = int(page_a) + 1
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'
                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                data = data + re.compile(reString, re.DOTALL).findall(htmlDoc)

            x = 0
            for movie in data:
                osdList.append((_(movie[1][6:]), movie[0]))
                x = x + 1

            print x
        if self.action is 'movie2':
            self.value = self.value.split(',')
            if self.value[0].find('search') > -1:
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey + '&search_section=1&sort=alphabet&page='
            else:
                letter = self.value[0]
                url = 'http://www.primewire.ag/index.php?&sort=featured&page='
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range(pages):
                page = int(page_a)
                page_a = int(page_a) + 1
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'
                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                data = data + re.compile(reString, re.DOTALL).findall(htmlDoc)

            x = 0
            for movie in data:
                osdList.append((_(movie[1][6:]), movie[0]))
                x = x + 1

            print x
        if self.action is 'movie3':
            self.value = self.value.split(',')
            if self.value[0].find('search') > -1:
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey + '&search_section=1&sort=alphabet&page='
            else:
                letter = self.value[0]
                url = 'http://www.primewire.ag/index.php?&page='
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range(pages):
                page = int(page_a)
                page_a = int(page_a) + 1
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'
                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                data = data + re.compile(reString, re.DOTALL).findall(htmlDoc)

            x = 0
            for movie in data:
                osdList.append((_(movie[1][6:]), movie[0]))
                x = x + 1

            print x
        if self.action is 'genre':
            self.value = self.value.split(',')
            if self.value[0].find('search') > -1:
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey + '&search_section=1&sort=alphabet&page='
            else:
                letter = self.value[0]
                url = 'http://www.primewire.ag/index.php?genre=' + letter + '&sort=featured&page='
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range(pages):
                page = int(page_a)
                page_a = int(page_a) + 1
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'
                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                data = data + re.compile(reString, re.DOTALL).findall(htmlDoc)

            x = 0
            for movie in data:
                osdList.append((_(movie[1][6:]), movie[0]))
                x = x + 1

            print x
        if self.action is 'tvshow':
            self.value = self.value.split(',')
            if self.value[0].find('search') > -1:
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey + '&search_section=2&sort=alphabet&page='
            else:
                letter = self.value[0]
                url = 'http://www.primewire.ag/index.php?letter=' + letter + '&tv=&sort=alphabet&page='
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range(pages):
                page = int(page_a)
                page_a = int(page_a) + 1
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'
                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                data = data + re.compile(reString, re.DOTALL).findall(htmlDoc)

            x = 0
            for movie in data:
                osdList.append((_(movie[1][6:]), movie[0]))
                x = x + 1

            print x
        if self.action is 'tvshow2':
            self.value = self.value.split(',')
            if self.value[0].find('search') > -1:
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey + '&search_section=2&sort=alphabet&page='
            else:
                letter = self.value[0]
                url = 'http://www.primewire.ag/index.php?tv=&page='
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range(pages):
                page = int(page_a)
                page_a = int(page_a) + 1
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'
                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                data = data + re.compile(reString, re.DOTALL).findall(htmlDoc)

            x = 0
            for movie in data:
                osdList.append((_(movie[1][6:]), movie[0]))
                x = x + 1

            print x
        if self.action is 'tvshow3':
            self.value = self.value.split(',')
            if self.value[0].find('search') > -1:
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey + '&search_section=1&sort=alphabet&page='
            else:
                letter = self.value[0]
                url = 'http://www.primewire.ag/index.php?tv=&sort=featured&page='
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range(pages):
                page = int(page_a)
                page_a = int(page_a) + 1
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'
                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                data = data + re.compile(reString, re.DOTALL).findall(htmlDoc)

            x = 0
            for movie in data:
                osdList.append((_(movie[1][6:]), movie[0]))
                x = x + 1

            print x
        if self.action is 'genre2':
            self.value = self.value.split(',')
            if self.value[0].find('search') > -1:
                search = self.value[0].split('-')
                value = search[1]
                searchkey = search[2]
                url = 'http://www.primewire.ag/index.php?search_keywords=' + value + '&key=' + searchkey + '&search_section=1&sort=alphabet&page='
            else:
                letter = self.value[0]
                url = 'http://www.primewire.ag/index.php?tv=&genre=' + letter + '&sort=featured&page='
            pages = self.value[1].split(' - ')
            page_a = pages[0]
            page_b = pages[1]
            pages = int(page_b) - int(page_a) + 1
            data = []
            for x in range(pages):
                page = int(page_a)
                page_a = int(page_a) + 1
                pageurl = url + str(page)
                print url
                reString = '<div class="index_item index_item_ie"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" width="150" height="225" alt=".+?"><h2>(.+?)</h2>'
                req = urllib2.Request(pageurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                htmlDoc = str(response.read())
                response.close()
                data = data + re.compile(reString, re.DOTALL).findall(htmlDoc)

            x = 0
            for movie in data:
                osdList.append((_(movie[1][6:]), movie[0]))
                x = x + 1

            print x
        if not osdList:
            osdList.append((_('Sorry nothing found!'), 'exit'))
        osdList.append((_('Help & About'), 'help'))
        osdList.append((_('Exit'), 'exit'))
        Screen.__init__(self, session)
        self['myMenu'] = MenuList(osdList)
        self['myActionMap'] = ActionMap(['SetupActions', 'ColorActions'], {'cancel': self.cancel,
         'ok': self.go,
         'green': self.ddsubtitle}, -1)

    def ddsubtitle(self):
        returnValue = self['myMenu'].l.getCurrentSelection()[0]
        fp = open('/tmp/zasp', 'w')
        fp.write(str(returnValue))
        fp.close()
        try:
            from Plugins.Extensions.DD_Subt.plugin import Mojtitle
            ref = self.session.nav.getCurrentlyPlayingServiceReference()
            self.session.open(Mojtitle, ref)
        except:
            print 'no ddsubtitleplayer???'

    def go(self):
        returnValue = self['myMenu'].l.getCurrentSelection()[1]
        if returnValue is 'help':
            self.session.open(ShowHelp)
        elif returnValue is 'exit':
            self.close(None)
        else:
            value = returnValue + ',' + self['myMenu'].l.getCurrentSelection()[0]
            print value
            if self.action is 'movie':
                self.session.open(MovieSource, 'moviesource', value)
            if self.action is 'movie2':
                self.session.open(MovieSource, 'moviesource', value)
            if self.action is 'movie3':
                self.session.open(MovieSource, 'moviesource', value)
            if self.action is 'genre':
                self.session.open(MovieSource, 'moviesource', value)
            if self.action is 'tvshow':
                self.session.open(TvEpisode, 'tvepisode', value)
            if self.action is 'tvshow2':
                self.session.open(TvEpisode, 'tvepisode', value)
            if self.action is 'tvshow3':
                self.session.open(TvEpisode, 'tvepisode', value)
            if self.action is 'genre2':
                self.session.open(TvEpisode, 'tvepisode', value)
        return

    def cancel(self):
        self.close(None)
        return


class TvEpisode(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    skin = '\n        <screen position="100,150" size="' + str(wsize) + ',' + str(hsize) + '" title="1channel" >\n        <widget name="myMenu" position="10,10" size="' + str(wsize - 20) + ',' + str(hsize - 20) + '" scrollbarMode="showOnDemand" />\n        </screen>'

    def __init__(self, session, action, value):
        self.session = session
        self.action = action
        self.value = value
        osdList = []
        print self.value
        url = 'http://www.primewire.ag' + self.value.split(',')[0]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        htmlDoc = str(response.read())
        response.close()
        links = re.compile(' <div class="tv_episode_item">(.+?)</a> </div>', re.DOTALL).findall(htmlDoc)
        for link in links:
            linkurl = re.compile('<a href="(.+?)">', re.DOTALL).findall(link)[0]
            try:
                epname = re.compile('class="tv_episode_name">(.+?)</span>', re.DOTALL).findall(link)[0]
            except:
                epname = ' - Unknown title'

            epnumb = str(linkurl.split('/')[2]).replace('-', ' ')
            epnumb = epnumb.replace('season ', 'S')
            epnumb = epnumb.replace('episode ', 'E')
            print str(linkurl) + ' - ' + epnumb + epname + '\n'
            osdList.append((_(epnumb + epname), linkurl))

        osdList.append((_('Help & About'), 'help'))
        osdList.append((_('Exit'), 'exit'))
        Screen.__init__(self, session)
        self['myMenu'] = MenuList(osdList)
        self['myActionMap'] = ActionMap(['SetupActions'], {'cancel': self.cancel,
         'ok': self.go}, -1)

    def go(self):
        returnValue = self['myMenu'].l.getCurrentSelection()[1]
        returnSelection = self['myMenu'].l.getCurrentSelection()[0]
        if returnValue is 'help':
            self.session.open(ShowHelp)
        elif returnValue is 'exit':
            self.close(None)
        else:
            value = returnValue + ',' + self.value.split(',')[1] + ' ' + returnSelection
            print value
            self.session.open(MovieSource, 'moviesource', value)
        return

    def cancel(self):
        self.close(None)
        return


class MovieSource(Screen):
    wsize = getDesktop(0).size().width() - 200
    hsize = getDesktop(0).size().height() - 300
    skin = '\n        <screen position="100,150" size="' + str(wsize) + ',' + str(hsize) + '" title="1channel" >\n        <widget name="myMenu" position="10,10" size="' + str(wsize - 20) + ',' + str(hsize - 20) + '" scrollbarMode="showOnDemand" />\n        </screen>'

    def __init__(self, session, action, value):
        self.session = session
        self.action = action
        self.value = value
        osdList = []
        resolved = []
        print self.value
        if self.value.split(',')[0].find('http://') > -1:
            osdList.append((_('Uservideo '), self.value.split(',')[0]))
            linksfound = 1
        else:
            url = 'http://www.primewire.ag' + self.value.split(',')[0]
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            htmlDoc = str(response.read())
            response.close()
            links = re.compile('<a href="(.+?)" onClick="return').findall(htmlDoc)
            hosts = ['putlocker', 'sockshare', 'gorillavid', 'filenuke', 'daclips', "movpod", 'uploadc', 'vidxden', 'vidbux', 'nowvideo', 'divixstage', 'novamov', 'zalaa', 'firedrive']
            print resolved
            linksfound = 0
            for link in links:
                try:
                    domain = re.compile('&domain=(.+?)&').findall(link)[0].decode('base-64')
                    for host in hosts:
                        if domain.find(host) > -1:
                            osdList.append((_('Video hosted at: ' + host.upper()), link))
                            linksfound = linksfound + 1
                            continue

                except:
                    print 'nebitno'
                    continue

                continue

        if linksfound is 0:
            osdList.append((_('Sorry no usable links found!'), 'exit'))
        osdList.append((_('Help & About'), 'help'))
        osdList.append((_('Exit'), 'exit'))
        Screen.__init__(self, session)
        self['myMenu'] = MenuList(osdList)
        self['myActionMap'] = ActionMap(['SetupActions'], {'cancel': self.cancel,
         'ok': self.go}, -1)

    def go(self):
        returnValue = self['myMenu'].l.getCurrentSelection()[1]
        print returnValue
        if returnValue is 'help':
            self.session.open(ShowHelp)
        elif returnValue is 'exit':
            self.close(None)
        elif returnValue.find('/external.php') > -1:
            url = 'http://www.primewire.ag' + returnValue
            if returnValue.find('&domain=') > -1:
                returnValue = re.compile('&url=(.+?)&domain').findall(returnValue)[0].decode('base-64')
                req = urllib2.Request(returnValue)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                returnValue = response.geturl()
                response.close()
            print returnValue
        if returnValue.find('sockshare.com/file/') > -1:
            returnValue = returnValue + ',' + self.value.split(',')[1]
            self.Putlocker(returnValue)
        if returnValue.find('putlocker.com/file/') > -1 or returnValue.find('firedrive.com/file/') > -1:
            returnValue = returnValue + ',' + self.value.split(',')[1]
            self.Firedrive(returnValue)    
        elif returnValue.find('novamov.com/video/') > -1 or returnValue.find('divxstage.eu/video/') > -1 or returnValue.find('nowvideo.eu/video/') > -1:
            returnValue = returnValue + ',' + self.value.split(',')[1]
            self.Novamov(returnValue)
        elif returnValue.find('zalaa.com/') > -1 or returnValue.find('uploadc.com/') > -1:
            returnValue = returnValue + ',' + self.value.split(',')[1]
            self.Uploadc(returnValue)
        elif returnValue.find('vidbux.com/') > -1 or returnValue.find('vidxden.com/') > -1:
            returnValue = returnValue + ',' + self.value.split(',')[1]
            self.Vidbux(returnValue)
        elif returnValue.find('filenuke.com/') > -1:
            returnValue = returnValue + ',' + self.value.split(',')[1]
            self.Filenuke(returnValue)
        elif returnValue.find('gorillavid') > -1 or returnValue.find('movpod') > -1 or returnValue.find('daclips') > -1:
            returnValue = returnValue + ',' + self.value.split(',')[1]
            self.Gorillavid(returnValue)
        return

    def cancel(self):
        self.close(None)
        return

    def Putlocker(self, fileUrl):
        self.title = fileUrl.split(',')[1]
        fileUrl = fileUrl.split(',')[0]
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        try:
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
        except:
            print 'jebiga'

        if html_doc is not '':
            plhash = re.compile('<input type="hidden" value="([0-9a-f]+?)" name="hash">').findall(html_doc)
        if plhash:
            time.sleep(7)
            data = {'hash': plhash[0],
             'confirm': 'Continue as Free User'}
            data = urllib.urlencode(data)
            req = urllib2.Request(fileUrl, data)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
            plplaylist = re.compile("playlist: '/get_file.php\\?stream=(.+?)'").findall(html_doc)
            if plplaylist:
                print fileUrl
                if fileUrl.find('http://www.putlocker.com/file/') > -1:
                    url = 'http://www.putlocker.com/get_file.php?stream=' + plplaylist[0]
                elif fileUrl.find('http://www.sockshare.com/file/') > -1:
                    url = 'http://www.sockshare.com/get_file.php?stream=' + plplaylist[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                html_doc = str(response.read())
                response.close()
                plurl = re.compile('<media:content url="(.+?)" type="video/x-flv"').findall(html_doc)
                if plurl:
                    try:
                        url = plurl[0].replace('&amp;', '&')
                        url = url.replace("'", '')
                    except:
                        url = plurl[0]

                    print '### ' + url + ' ###'
                    try:
                        import usb
                        url = usb.storage(url)
                    except:
                        print 'No usb support!!!'

                    fileRef = eServiceReference(4097, 0, url)
                    fileRef.setName(self.title)
                    self.session.open(MoviePlayer, fileRef)
                else:
                    self.session.open(MessageBox, _('Host Resolver > Unable to resolve:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)
            else:
                self.session.open(MessageBox, _('Host Resolver > Unable to resolve:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)
        else:
            self.session.open(MessageBox, _('Host Resolver > File not found error:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)

    #firedrive
    def Firedrive(self, fileUrl):
        self.title = fileUrl.split(',')[1]
        fileUrl = fileUrl.split(',')[0]
        try:
            import res_firedrive
            url = res_firedrive.resolve(fileUrl)
            print '### ' + url + ' ###'
            try:
                import usb
                url = usb.storage(url)
            except:
                print 'No usb support!!!'

            fileRef = eServiceReference(4097, 0, url)
            fileRef.setName(self.title)
            self.session.open(MoviePlayer, fileRef)
        except:
            self.session.open(MessageBox, _('Host Resolver > File not found error or unable to resolve:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)
    
    
    def Novamov(self, fileUrl):
        self.title = fileUrl.split(',')[1]
        fileUrl = fileUrl.split(',')[0]
        try:
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
            r = re.search('flashvars.domain="(.+?)".+?flashvars.file="(.+?)".+?flashvars.filekey="(.+?)"', html_doc, re.DOTALL)
            if r:
                print r.groups()
                domain, filename, filekey = r.groups()
                print domain
                url = domain + '/api/player.api.php?key=' + filekey + '&file=' + filename
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                html_doc = str(response.read())
                response.close()
                print html_doc
                html_doc = html_doc.split('&')
                url = str(html_doc[0][4:])
                try:
                    import usb
                    url = usb.storage(url)
                    self.session.open(MessageBox, _('Usb storage found: ' + str(dev[0]) + '! Please wait for temp file...'), MessageBox.TYPE_ERROR, timeout=30)
                except:
                    print 'No usb support!!!'

                fileRef = eServiceReference(4097, 0, url)
                fileRef.setName(self.title)
                self.session.open(MoviePlayer, fileRef)
        except:
            self.session.open(MessageBox, _('Host Resolver > Unable to resolve:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)

    def Uploadc(self, fileUrl):
        self.title = fileUrl.split(',')[1]
        fileUrl = fileUrl.split(',')[0]
        try:
            import jsunpack
        except:
            print 'no jsunpack.py'

        try:
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
            post = re.compile('<input type="hidden" name="(.+?)".+?value="(.+?)">').findall(html_doc)
            data = urllib.urlencode(post)
            response = urllib2.urlopen(req, data)
            html_doc = str(response.read())
            response.close()
            try:
                jspack = re.compile("<script type='text/javascript'>eval(.+?)script>", re.DOTALL).findall(html_doc)[1]
                js = jsunpack.unpack(jspack)
                url = re.compile('<param name="src"0="(.+?)"/>', re.DOTALL).findall(js)[0]
            except:
                url = re.compile("'file','(.+?)'", re.DOTALL).findall(html_doc)[0]

            print url
            try:
                import usb
                url = usb.storage(url)
                self.session.open(MessageBox, _('Usb storage found: ' + str(dev[0]) + '! Please wait for temp file...'), MessageBox.TYPE_ERROR, timeout=30)
            except:
                print 'No usb support!!!'

            print self.title
            fileRef = eServiceReference(4097, 0, url)
            fileRef.setName(self.title)
            self.session.open(MoviePlayer, fileRef)
        except:
            print 'jebiga'
            self.session.open(MessageBox, _('Host Resolver > Unable to resolve:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)

    def Vidbux(self, fileUrl):
        self.title = fileUrl.split(',')[1]
        fileUrl = fileUrl.split(',')[0]
        try:
            import jsunpack
        except:
            print 'no jsunpack.py'

        try:
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
            post = re.compile('<input name="(.+?)".+?value="(.+?)"').findall(html_doc)
            data = urllib.urlencode(post)
            response = urllib2.urlopen(req, data)
            html_doc = str(response.read())
            response.close()
            jspack = re.compile("<script type='text/javascript'>eval(.+?)script>", re.DOTALL).findall(html_doc)[0]
            js = jsunpack.unpack(jspack)
            url = re.compile("'file','(.+?)'", re.DOTALL).findall(js)[0]
            print url
            try:
                import usb
                url = usb.storage(url)
                self.session.open(MessageBox, _('Usb storage found: ' + str(dev[0]) + '! Please wait for temp file...'), MessageBox.TYPE_ERROR, timeout=30)
            except:
                print 'No usb support!!!'

            print self.title
            fileRef = eServiceReference(4097, 0, url)
            fileRef.setName(self.title)
            self.session.open(MoviePlayer, fileRef)
        except:
            print 'jebiga'
            self.session.open(MessageBox, _('Host Resolver > Unable to resolve:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)

    def Filenuke(self, fileUrl):
        self.title = fileUrl.split(',')[1]
        fileUrl = fileUrl.split(',')[0]
        try:
            import jsunpack
        except:
            print 'no jsunpack.py'

        try:
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
            post = re.compile('<form method="POST" action=\'\'>(.+?)</form>', re.DOTALL).findall(html_doc)[0]
            post_data = re.compile('<input type="hidden" name="(.+?)" value="(.+?)">').findall(post)
            post_data.append(('method_free', 'Free'))
            data = urllib.urlencode(post_data)
            response = urllib2.urlopen(req, data)
            html_doc = str(response.read())
            response.close()
            jspack = re.compile("<script type='text/javascript'>eval(.+?)script>", re.DOTALL).findall(html_doc)[1]
            js = jsunpack.unpack(jspack)
            url = re.compile("'file','(.+?)'", re.DOTALL).findall(js)[0]
            try:
                import usb
                url = usb.storage(url)
                self.session.open(MessageBox, _('Usb storage found: ' + str(dev[0]) + '! Please wait for temp file...'), MessageBox.TYPE_ERROR, timeout=30)
            except:
                print 'No usb support!!!'

            print self.title
            fileRef = eServiceReference(4097, 0, url)
            fileRef.setName(self.title)
            self.session.open(MoviePlayer, fileRef)
        except:
            print 'jebiga'
            self.session.open(MessageBox, _('Host Resolver > Unable to resolve:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)

    def Gorillavid(self, fileUrl):
        self.title = fileUrl.split(',')[1]
        fileUrl = fileUrl.split(',')[0]
        try:
            req = urllib2.Request(fileUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html_doc = str(response.read())
            response.close()
            post = re.compile('<input type="hidden" name="(.+?)" value="(.+?)">').findall(html_doc)
            data = urllib.urlencode(post)
            response = urllib2.urlopen(req, data)
            html_doc = str(response.read())
            response.close()
            url = re.compile('file: "(.+?)"').findall(html_doc)[0]
            print url
            try:
                import usb
                url = usb.storage(url)
            except:
                print 'No usb support!!!'

            print self.title
            fileRef = eServiceReference(4097, 0, url)
            fileRef.setName(self.title)
            self.session.open(MoviePlayer, fileRef)
        except:
            print 'jebiga'
            self.session.open(MessageBox, _('Host Resolver > Unable to resolve:\n' + self['myMenu'].l.getCurrentSelection()[0]), MessageBox.TYPE_ERROR, timeout=5)


def main(session, **kwargs):
    action = 'start'
    value = 0
    burek = session.open(MyMenux, action, value)


class MoviePlayer(MP_parent):

    def __init__(self, session, service):
        self.session = session
        self.WithoutStopClose = False
        MP_parent.__init__(self, self.session, service)

    def leavePlayer(self):
        self.is_closing = True
        self.close()

    def leavePlayerConfirmed(self, answer):
        pass

    def doEofInternal(self, playing):
        if self.execing and playing:
            self.leavePlayer()
            return
        else:
            return

    def showMovies(self):
        self.WithoutStopClose = False
        self.close()

    def movieSelected(self, service):
        self.leavePlayer(self.de_instance)

    def __onClose(self):
        if not self.WithoutStopClose:
            self.session.nav.playService(self.lastservice)


def Plugins(**kwargs):
    return PluginDescriptor(description='PrimeWire', fnc=main, icon='./icon.png', name='PrimeWire', where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU])
