#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SYNPOPSIS:    This bot parses the RC feed for CentralAuth using regex, and reports to a freenode channel
# LICENSE:      GPL
# CREDITS:      Mike.lifeguard, Erwin, Dungodung (Filip Maljkovic)
#

import sys, os, re, time, string, threading, thread, urllib, math
import ConfigParser
# needs python-irclib
from ircbot import SingleServerIRCBot
from ircbot import IRCDict
from ircbot import Channel
from irclib import nm_to_n

class FreenodeBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, password, opernick, operpass, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.server = server
        self.channel = channel
        self.nickname = nickname
        self.password = password
        self.opernick = opernick
        self.operpass = operpass
        
    def on_error(self, c, e):
        print 'Error:\nArguments: %s\nTarget: %s' % (e.arguments(), e.target())
        self.die()
        sys.exit()
    
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
        c.privmsg("NickServ",'GHOST %s %s' % (self.nickname, self.password))
        c.nick(self.nickname) # FIX -- what is broken? 0_o
        c.privmsg("NickServ",'IDENTIFY %s' % self.password)

    def on_welcome(self, c, e):
        c.privmsg("NickServ",'GHOST %s %s' % (self.nickname, self.password))
        c.privmsg("NickServ",'IDENTIFY %s' % self.password)
        c.oper(self.opernick,self.operpass)
        print "c.oper(%s,%s)" % (self.opernick,self.operpass)li
        time.sleep(5) # let identification succeed before joining channels
        c.join(self.channel)

    def on_ctcp(self, c, e):
        if e.arguments()[0] == "VERSION":
            c.ctcp_reply(nm_to_n(e.source()),"Bot for watching stuff in " + self.channel)
        elif e.arguments()[0] == "PING":
            if len(e.arguments()) > 1: c.ctcp_reply(nm_to_n(e.source()),"PING " + e.arguments()[1])

    def on_action(self, c, e):
        #timestamp = '[%s] ' % time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(time.time()))
        nick = nm_to_n(e.source())
        who = '<%s/%s>' % (e.target(), nick)
        a = e.arguments()[0]
        #print timestamp+" * "+who+a
        
    def on_privmsg(self, c, e):
        #timestamp = '[%s] ' % time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(time.time()))
        nick = nm_to_n(e.source())
        target = nick
        who = '<%s/%s>' % (e.target(), nick)
        a = e.arguments()[0].split(":", 1)
        if a[0] == self.nickname:
            if len(a) == 2:
                command = a[1].strip()
                if self.getCloak(e.source()) in config.get('Setup', 'privileged').split('<|>'):
                    try:
                        self.do_command(e, command, target)
                    except:
                        print 'Error: %s' % sys.exc_info()[1]
                        self.msg('You have to follow the proper syntax. See \x0302http://toolserver.org/~stewardbots/SULWatcher\x03', nick)

    def on_pubmsg(self, c, e):
        #timestamp = '[%s] ' % time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(time.time()))
        nick = nm_to_n(e.source())
        target = e.target()
        who = '<%s/%s>' % (e.target(), nick)
        a = e.arguments()[0].split(":", 1)
        if a[0] == self.nickname:
            if len(a) == 2:
                command = a[1].strip()
                if self.getCloak(e.source()) in config.get('Setup', 'privileged').split('<|>'):
                    try:
                        self.do_command(e, command, target)
                    except:
                        print 'Error: %s' % sys.exc_info()[1]
                        self.msg('You have to follow the proper syntax. See \x0302http://toolserver.org/~stewardbots/SULWatcher\x03', target)

    def do_command(self, e, cmd, target):
        nick = nm_to_n(e.source())
        c = self.connection
        args = cmd.split(' ')
        if args[0] == '_':
            args.remove('_')

        if args[0] == 'help':
            self.msg(config.get('Setup', 'help'), nick)
        elif args[0] == 'test': # Notifications
            if len(args)>=4:
                try:
                    i = args.index('regex')
                    string = ' '.join(args[1:i])
                    probe = ' '.join(args[i+1:])
                    if (re.search(probe, string, re.IGNORECASE)):
                        self.msg('\'%s\' matches regex \'%s\'.' % (string, probe) , target)
                    else:
                        self.msg('\'%s\' does not match regex \'%s\'.' % (string, probe) , target)
                except:
                    self.msg(r'Please use the format "SULWatcher test string to test regex \bregular ?expression\b".', target)
            else:
                self.msg(r"Yes, I'm alive. You can test a string against a regex by saying 'SULWatcher: test string to test regex \bregular ?expression\b'.", target)
        elif args[0] == 'find' or args[0] == 'search':
            if args[1] == 'regex' or args[1] == 'badword':
                badword = ' '.join(args[2:])
                for section in config.sections():
                    if section != 'Setup':
                        if config.get(section, 'regex') == badword:
                            adder = config.get(section, 'adder')
                            try:
                                self.msg('The regex %s (#%s) was added by %s with the note: "%s".' % (badword, self.getIndex('regex', badword), adder, config.get(section, 'reason')), target)
                            except:
                                self.msg('The regex %s (#%s) was added by %s with no reason.' % (badword, self.getIndex('regex', badword), adder), target)
                            return
                self.msg(r'%s is not listed. You can add it by saying "SULWatcher: add regex %s"' % (badword, badword), target)
            elif args[1] == 'match' or args[1] == 'matches':
                string = ' '.join(args[2:])
                probes = []
                for section in config.sections():
                    if section != 'Setup':
                        probes.append(config.get(section, 'regex'))
                matches = []
                for p in probes:
                    if re.search(p, string, re.IGNORECASE):
                        matches.append(p)
                if len(matches) == 0:
                    self.msg('There is no regex which matches that string.', target)
                else:
                    self.msg('\'%s\' matches \'%s\'.' % (string, '\', \''.join(matches)) , target)
            elif args[1] == 'adder':
                adder = args[2]
                regexes = []
                for section in config.sections():
                    if section != 'Setup':
                        if config.get(section, 'adder') == adder:
                            regexes.append(config.get(section, 'regex'))
                if len(regexes) == 0:
                    self.msg('%s has added no regexes.' % adder, target)
                else:
                    shortlists = []
                    maxlen = 20
                    iters = int(math.ceil(float(len(regexes))/maxlen))
                    for x in range(0, iters):
                        lower = x*maxlen
                        upper = (x+1)*maxlen
                        shortlists.append(regexes[lower:upper])
                    for l in range(0, len(shortlists)):
                        self.msg(r'%s added (%s/%s): %s.' % (adder, l+1, len(shortlists), ", ".join(shortlists[l])), target)
                        time.sleep(2) # sleep a bit to avoid flooding?
            elif args[1] == 'number':
                index = args[2]
                if config.has_section(index):
                    try:
                        self.msg('%s: \'%s\' was added by %s with the reason: "%s"' % (index, config.get(index, 'regex'), config.get(index, 'adder'), config.get(index, 'reason')), target)
                    except:
                        self.msg('%s: \'%s\' was added by %s.' % (index, config.get(index, 'regex'), config.get(index, 'adder')), target)
                else:
                    self.msg(r'%s doesn\'t exist. You can search for the regex itself using "SULWatcher: find regex \bregex\b".' % index, target)
            else:
                self.msg('You can search for info on a regex by saying "SULWatcher: find regex \bregex\b", or you can find the regex matching a string by saying "SULWatcher: find match String to test".', target)
        elif args[0] == 'edit' or args[0] == 'change':
            if config.has_section(args[1]):
                section = args[1]
                if args[2] == 'regex' or args[2] == 'badword':
                    newregex = ' '.join(args[3:])
                    if config.has_option(section, 'reason'):
                        oldreason = config.get(section, 'reason')
                    adder = self.getCloak(e.source())
                    oldregex = config.get(section, 'regex')
                    try:
                        self.removeRegex(oldregex, target)
                        self.addRegex(newregex, adder, target)
                        try:
                            self.setConfig(section, 'reason', oldreason)
                            self.saveConfig()
                            self.msg('I kept the old reason ("%s"), but you can change it with "SULWatcher: edit %s reason Whatever".' % (oldreason, section), target)
                        except:
                            self.msg('There was no reason provided previously - you should add one with "SULWatcher: add reason %s Whatever".' % section, target)
                    except:
                        self.msg('Something bad happened - you\'ll have to change %s to %s manually: %s' % (oldregex, newregex, sys.exc_info()[1]), target)
                elif args[2] == 'note' or args[2] == 'reason':
                    cloak = self.getCloak(e.source())
                    if args[3] == '!':
                        newreason = ' '.join(args[4:])
                        self.setConfig(section, 'reason', newreason)
                        self.setConfig(section, 'adder', cloak)
                        self.saveConfig()
                        self.msg('OK, I\'ve changed the note on %s to "%s", re-attributing it to %s.' % (config.get(section, 'regex'), newreason, cloak), target)
                    else:
                        newreason = ' '.join(args[3:])
                        adder = config.get(section, 'adder')
                        regex = config.get(section, 'regex')
                        if cloak == adder:
                            self.setConfig(section, 'reason', newreason)
                            self.saveConfig()
                            self.msg('OK, changed the note for %s to "%s".' % (regex, newreason), target)
                        else:
                            try:
                                self.msg('The regex %s was added by %s with the note: "%s". To re-attribute it to you and change the note, say "SULWatcher: edit %s reason ! %s".' % (regex, adder, config.get(section, 'reason'), section, newreason), target)
                            except:
                                self.msg('The regex %s was added by %s. To re-attribute it to you and change the note, say "SULWatcher: edit %s reason ! %s".' % (regex, adder, section, newreason), target)
            else:
                self.msg('Entry #%s doesn\'t exist. Go fish.' % args[2], target)
        elif args[0] == 'list': # Lists: modify and show
            if args[1] == 'owner' or args[1] == 'owners':
                self.msg('Owners can issue restricted commands: %s' % ', '.join(config.get('Setup', 'owner').split('<|>')), nick)
            if args[1] == 'privileged':
                self.msg('Privileged cloaks: %s' % ', '.join(config.get('Setup', 'privileged').split('<|>')), nick)
            elif args[1] == 'badword' or args[1] == 'badwords' or args[1] == 'regex' or args[1] == 'regexes':
                longlist = []
                for section in config.sections():
                    if section != 'Setup':
                        longlist.append(config.get(section, 'regex'))
                shortlists = []
                maxlen = 20
                iters = int(math.ceil(float(len(longlist))/maxlen))
                for x in range(0, iters):
                    lower = x*maxlen
                    upper = (x+1)*maxlen
                    shortlists.append(longlist[lower:upper])
                for l in range(0, len(shortlists)):
                    self.msg('Regex list (%s/%s): %s' % (l+1, len(shortlists), ", ".join(shortlists[l])), target)
                    time.sleep(2) # sleep a bit to avoid flooding?
            elif args[1] == 'whitelist':
                self.msg('Whitelisted users: %s' % ', '.join(config.get('Setup', 'whitelist').split('<|>')), target)
        elif args[0] == 'add':
            if args[1] == 'owner':
                if self.getCloak(e.source()) != 'wikimedia/mikelifeguard':
                    self.msg('You can\'t add owners unless you are Mike_lifeguard!', target)
                else:
                    who = ' '.join(args[2:])
                    self.addToList(who, 'Setup', 'owner', target)
            if args[1] == 'privileged':
                who = ' '.join(args[2:])
                self.addToList(who, 'Setup', 'privileged', target)
            elif args[1] == 'badword' or args[1] == 'regex':
                badword = ' '.join(args[2:])
                adder = self.getCloak(e.source())
                self.addRegex(badword, adder, target)
            elif args[1] == 'reason':
                if args[2]:
                    section = args[2]
                    if config.has_section(section):
                        adder = config.get(section, 'adder')
                        if args[3]:
                            if args[3] == '!':
                                reason = ' '.join(args[4:])
                                config.set(section, 'reason', reason)
                                adder = self.getCloak(e.source())
                                self.setConfig(section, 'adder', adder)
                                self.saveConfig()
                                self.msg('OK, I re-attributed %s to you and added the reason "%s"' % (config.get(section, 'regex'), reason), target)
                            else:
                                reason = ' '.join(args[3:])
                                if self.getCloak(e.source()) != adder:
                                    self.msg('You\'re about to add a reason to %s, which was added by %s. If you do this, the regex will be re-attributed to you. Say "SULWatcher: add reason %s ! %s" to do so.' % (section, adder, section, reason), target)
                                else:
                                    self.setConfig(section, 'reason', reason)
                                    self.saveConfig()
                                    self.msg('OK, I added "%s" as the reason for %s' % (reason, config.get(section, 'regex')), target)
                    else:
                        self.msg('%s isn\'t listed. Say "SULWatcher: add regex \bregex\b" to add to the list.' % section, target)
            elif args[1] == 'whitelist':
                who = ' '.join(args[2:])
                self.addToList(who, 'Setup', 'whitelist', target)
        elif args[0] == 'remove':
            if args[1] == 'privileged':
                who = ' '.join(args[2:])
                self.removeFromList(who, 'Setup', 'privileged', target)
            elif args[1] == 'badword' or args[1] == 'regex':
                badword = ' '.join(args[2:])
                self.removeRegex(badword, target)
            elif args[1] == 'whitelist':
                whitelist = ' '.join(args[2:])
                self.removeFromList(whitelist, 'Setup', 'whitelist', target)
            elif args[1] == 'owner':
                owner = ' '.join(args[2:])
                self.removeFromList(owner, 'Setup', 'owner', nick)
        elif args[0] == 'huggle': # Huggle
            try:
                who = args[1]
                self.connection.action(self.channel, 'huggles ' + who)
            except:
                self.msg('lolfail', channel)
        elif args[0] == 'die': # Die
            if self.getCloak(e.source()) not in config.get('Setup', 'owner').split('<|>'):
                self.msg('You can\'t kill me; you\'re not my owner!', target)
            else:
                print 'Yes, you\'re my owner.'
                if len(args)>=2:
                    quitmsg = ' '.join(args[1:])
                else:
                    quitmsg = config.get('Setup', 'quitmsg')
                self.saveConfig()
                print 'Saved config. Now killing all bots with message: "' + quitmsg + '"...'
                try:
                    rawquitmsg = ':'+quitmsg
                    rcreader.connection.part(rcreader.rcfeed)
                    rcreader.connection.quit()
                    rcreader.disconnect()
                except:
                    print 'rc reader didn\'t disconnect'
                try:
                    bot1.connection.part(bot1.channel, rawquitmsg)
                    bot1.connection.quit(rawquitmsg)
                    bot1.disconnect()
                except:
                    print 'bot1 didn\'t disconnect'
                try:
                    bot2.connection.part(bot2.channel, rawquitmsg)
                    bot2.connection.quit(rawquitmsg)
                    bot2.disconnect()
                except:
                    print 'bot2 didn\'t disconnect'
                print 'Killed. Now exiting...'
                sys.exit(0)
        elif args[0] == 'restart': # Restart
            if self.getCloak(e.source()) not in config.get('Setup', 'owner').split('<|>'):
                self.msg('You can\'t restart me; you\'re not my owner!', target)
            else:
                print 'Yes, you\'re my owner'
                self.saveConfig()
                print 'Saved config for paranoia.'
                if len(args) == 1:
                    quitmsg = config.get('Setup', 'quitmsg')
                    print 'Restarting all bots with message: '+quitmsg
                    rawquitmsg = ':'+quitmsg
                    try:
                        rcreader.connection.part(rcfeed)
                        rcreader.connection.quit()
                        rcreader.disconnect()
                        BotThread(rcreader).start()
                    except:
                        print 'rcreader didn\'t recover: %s' % sys.exc_info()[1]
                    try:
                        bot1.connection.part(mainchannel, rawquitmsg)
                        bot1.connection.quit()
                        bot1.disconnect()
                        BotThread(bot1).start()
                    except:
                        print 'bot1 didn\'t recover: %s' % sys.exc_info()[1]
                    try:
                        bot2.connection.part(mainchannel, rawquitmsg)
                        bot2.connection.quit()
                        bot2.disconnect()
                        BotThread(bot2).start()
                    except:
                        print 'bot2 didn\'t recover: %s' % sys.exc_info()[1]
                elif len(args) > 1 and args[1] == 'rc':
                    self.msg('Restarting rc reader', target)
                    try:
                        rcreader.connection.part(rcfeed)
                        rcreader.connection.quit()
                        rcreader.disconnect()
                        BotThread(rcreader).start()
                    except:
                        print 'rcreader didn\'t recover: %s' % sys.exc_info()[1]
                else:
                    print 'This shouldn\'t happen'

##    def integrityCheck(self):
##        sectionlist = config.sections()
##        sectionlist = sectionlist.remove('Setup').sort()
##        for i in range(0,len(sectionlist)):
##            if i != sectionlist[i]:
##                tempregex = config.get(sectionlist[i+1], 'regex')
##                tempadder = config.get(sectionlist[i+1], 'adder')
##                if config.get(sectionlist[i], 'reason'):
##                    tempreason = config.get(sectionlist[i+1], 'reason')
##                self.setConfig(i, 'regex', tempregex)
##                self.setConfig(i, 'adder', tempadder)
##                if tempreason:
##                    self.setConfig(i, 'reason', tempreason)
##                config.remove_section(sectionlist[i+1])
##                self.saveConfig()

    def saveConfig(self):
        print 'saveConfig(self)'
        configFile = open(os.path.expanduser('~/SULWatcher/SULWatcher.ini'), 'w')
        config.write(configFile)
        configFile.close()
        print 'done!'

    def getIndex(self, option, value):
        print 'getIndex(self, \'%s\', \'%s\')' % (option, value)
        for section in config.sections():
            if section != 'Setup':
                if config.get(section, option) == value:
                    return section

    def addRegex(self, regex, cloak, target):
        print 'addRegex(self, \'%s\', \'%s\', \'%s\')' % (regex, cloak, target)
        for section in config.sections():
            if section != 'Setup':
                if config.get(section, 'regex') == regex:
                    adder = config.get(section, 'adder')
                    if config.has_option(section, 'reason'):
                        reason = config.get(section, 'reason')
                    try:
                        self.msg('%s is already listed as a regex. It was added by %s with a note: "%s".' % (regex, adder, reason), target)
                    except:
                        self.msg('%s is already listed as a regex. It was added by %s.' % (regex, adder), target)
                    break
        for i in range(0,len(config.sections())):
            if not config.has_section(str(i)):
                config.add_section(str(i))
                self.setConfig(str(i), 'regex', regex)
                self.setConfig(str(i), 'adder', cloak)
                break # leave only the the smallest for loop
        self.saveConfig()
        self.msg('%s added %s to the list of regexes. If you would like to set a reason, say "SULWatcher: add reason %s reason for adding the regex".' % (cloak, regex, self.getIndex('regex', regex)), target)

    def removeRegex(self, regex, target):
        print 'removeRegex(self, \'%s\', \'%s\')' % (regex, target)
        found = False
        for section in config.sections():
            if section != 'Setup':
                if config.get(section, 'regex') == regex:
                    config.remove_section(section)
                    self.saveConfig()
                    found = True
        if found == True:
            self.msg('Removed %s from regex list.' % regex, target)
        else:
            self.msg('%s isn\'t in the regex list.' % regex, target)
            
    def setConfig(self, section, option, value):
        print 'setConfig(self, \'%s\', \'%s\', \'%s\')' % (section, option, value)
        config.set(section, option, value)

    def addToList(self, who, section, groupname, target):
        print 'addToLost(self, \'%s\', \'%s\', \'%s\', \'%s\')' % (who, section, groupname, target)
        list = config.get(section, groupname).split('<|>')
        if not who in list:
            list.append(who)
            list = '<|>'.join(list)
            self.setConfig(section, groupname, list)
            self.saveConfig()
            self.msg('%s added to %s.' % (who, groupname), target)
        else:
            self.msg('%s already in %s.' % (who, groupname), target)

    def removeFromList(self, who, section, groupname, target):
        print 'removeFromList(self, \'%s\', \'%s\', \'%s\', \'%s\')' % (who, section, groupname, target)
        list = config.get(section, groupname).split('<|>')
        if who in list:
            list.remove(who)
            list = '<|>'.join(list)
            self.setConfig(section, groupname, list)
            self.saveConfig()
            self.msg('%s removed from %s.' % (who, groupname), target)
        else:
            self.msg('%s not in %s.' % (who, groupname), target)

    def msg(self, message, target=None):
        #print 'msg(self, \'%s\', \'%s\')' % (message, target)
        if not target:
            target = self.channel
        self.connection.privmsg(target, message)

    def getCloak(self, doer):
        print 'getCloak(self, \'%s\')' % doer
        if re.search('@', doer):
            return doer.split('@')[1]

class WikimediaBot(SingleServerIRCBot):
    def __init__(self, rcfeed, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.server = server
        self.rcfeed = rcfeed
        self.nickname = nickname
        globals()['lastsulname'] = None
        globals()['lastbot'] = 1

    def on_error(self, c, e):
        print e.target()
        #self.die()
    
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + '_')

    def on_welcome(self, c, e):
        c.join(self.rcfeed)

    def on_ctcp(self, c, e):
        if e.arguments()[0] == 'VERSION':
            c.ctcp_reply(nm_to_n(e.source()), 'Bot for watching stuff in ' + channel)
        elif e.arguments()[0] == 'PING':
            if len(e.arguments()) > 1: c.ctcp_reply(nm_to_n(e.source()),"PING " + e.arguments()[1])
        
    def on_pubmsg(self, c, e):
        a = e.arguments()[0]
        #bot1.msg(a)
        # Parsing the rcbot output: \x0314[[\x0307Usu\xc3\xa1rio:Liliaan\x0314]]\x034@ptwiki\x0310 \x0302http://pt.wikipedia.org/wiki/Usu%C3%A1rio:Liliaan\x03 \x035*\x03 \x0303Liliaan\x03 \x035*\x03
        parse = re.compile("\\x0314\[\[\\x0307(?P<localname>.*)\\x0314\]\]\\x034@(?P<sulwiki>.*)\\x0310.*\\x0303(?P<sulname>.*)\\x03 \\x035\*\\x03",re.UNICODE)
        try:
            localname = parse.search(a).group('localname')
            sulwiki = parse.search(a).group('sulwiki')
            sulname = parse.search(a).group('sulname')
            if not globals()['lastsulname'] or globals()['lastsulname'] != sulname:
                bad = False
                good = False
                #print sulname + "@" + sulwiki
                badwords = []
                for section in config.sections():
                    if section != 'Setup':
                        badwords.append(re.compile(config.get(section, 'regex'), re.IGNORECASE))
                matches = []
                for bw in badwords:
                    if (bw.search(sulname)):#regex!
                        bad = True
                        matches.append(bw.pattern)
                for wl in config.get('Setup', 'whitelist').split('<|>'):
                    if sulname == wl:
                        print '(skipped ' + sulname + '; user is whitelisted)'
                        good = True
                if not bad and not good:
                    if globals()['lastbot'] != 1:
                        bot1.msg("\x0303%s\x03@%s: \x0302https://secure.wikimedia.org/wikipedia/meta/wiki/Special:CentralAuth/%s\x03" % (sulname, sulwiki, urllib.quote(sulname)))
                        globals()['lastbot'] = 1
                    else:
                        bot2.msg("\x0303%s\x03@%s: \x0302https://secure.wikimedia.org/wikipedia/meta/wiki/Special:CentralAuth/%s\x03" % (sulname, sulwiki, urllib.quote(sulname)))
                        globals()['lastbot'] = 2
                elif bad and not good:
                    if globals()['lastbot'] != 1:
                        bot1.msg("\x0303%s\x03@%s \x0305\x02matches badword %s\017: \x0302https://secure.wikimedia.org/wikipedia/meta/wiki/Special:CentralAuth/%s\x03" % (sulname, sulwiki, '; '.join(matches), urllib.quote(sulname)))
                        globals()['lastbot'] = 1
                    else:
                        bot2.msg("\x0303%s\x03@%s \x0305\x02matches badword %s\017: \x0302https://secure.wikimedia.org/wikipedia/meta/wiki/Special:CentralAuth/%s\x03" % (sulname, sulwiki, '; '.join(matches), urllib.quote(sulname)))
                        globals()['lastbot'] = 2
            globals()['lastsulname'] = sulname
        except:
            print 'RC reader error: %s' % sys.exc_info()[1]

class BotThread(threading.Thread):
    def __init__ (self, bot):
        self.b=bot
        threading.Thread.__init__ (self)

    def run (self):
        self.startbot(self.b)

    def startbot(self, bot):
        bot.start()

def main():
    global bot1, rcreader, bot2, config, nickname, alias, password, mainchannel, mainserver, wmserver, rcfeed, opernick, operpass
    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser('~/SULWatcher/SULWatcher.ini'))
    nickname = config.get('Setup', 'nickname')
    opernick = config.get('Setup', 'opernick')
    operpass = config.get('Setup', 'operpass')
    alias = config.get('Setup', 'alias')
    password = config.get('Setup', 'password')
    mainchannel = config.get('Setup', 'channel')
    mainserver = config.get('Setup', 'server')
    wmserver = config.get('Setup', 'wmserver')
    rcfeed = config.get('Setup', 'rcfeed')
    bot1 = FreenodeBot(mainchannel, nickname, mainserver, password, opernick, operpass, 8001)
    BotThread(bot1).start()
    bot2 = FreenodeBot(mainchannel, alias, mainserver, password, opernick, operpass, 8001)
    BotThread(bot2).start()
    time.sleep(6) # The Freenode bots connect comparatively slowly & have a 5s delay to identify to services before joining channels
    rcreader = WikimediaBot(rcfeed, nickname, wmserver, 6667)
    BotThread(rcreader).start() # Can cause ServerNotConnectedError

if __name__ == "__main__":
    global bot1, rcreader, bot2, config
    #main()
    try:
        main()
    except:
        print '\nUnexpected error: %s' % sys.exc_info()[1]
        bot1.die()
        rcreader.die()
        bot2.die()
        sys.exit()
