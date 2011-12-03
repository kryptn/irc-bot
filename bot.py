#!/usr/bin/env python
import sys, os, random, re, time, pymongo, datetime
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor, task
from string import letters, digits

db = pymongo.Connection().lolbot

class ircBot(irc.IRCClient):
	def __init__(self):
		pass

	@property
	def nickname(self):
		return self.factory.nickname

	@property
	def password(self):
		return self.factory.password
	
	def signedOn(self):
		self.join(self.factory.channel)

	def privmsg(self, user, channel, msg):
		self.msg(channel, "I literally don't do a thing currently.")
	
	def log(self, collection, **args):
		db[collection].insert(args)


class lolBot(ircBot):
	def privmsg(self, user, channel, msg):
		self.log('testlog', user=user, channel=channel, msg=msg, dt=datetime.datetime.utcnow())

		user = user.split('!',1)[0]
		firstword = msg.split()[0]

		toMe = False
		if self.nickname == firstword[:-1]:
			if firstword[-1] in [',',':']:
				toMe = True
				msg = msg.split(' ',1)[1]

		if channel is self.nickname:
			self.msg(user, 'I\'m totally ignoring you')
		
		if toMe:
			self.msg(channel, '%s said %s' % (user, msg))

class r9kBot(ircBot):
   """ mutes user if phrase previously said """

   def normalize(self, msg):


   
class bucketBot(ircBot):
   """ factoid bot """
   pass

class ircBotFactory(protocol.ClientFactory):

   def __init__(self, protocol, channel, nickname='lolbot', password=None):
      self.protocol = protocol
      self.channel = channel
      self.nickname = nickname
      self.password = password
   
   def clientConnectionLost(self, connector, reason):
      connector.connect()

   def clientConnectionFailed(self, connector, reason):
      reactor.stop()

if __name__ == "__main__":
	pcol = lolBot
	reactor.connectTCP('irc.freenode.net', 6667, ircBotFactory(pcol, '#icv'))
	reactor.run()