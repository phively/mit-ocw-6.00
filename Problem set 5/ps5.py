# -*- coding: utf-8 -*-
# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import re
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    
    # Initialization
    def __init__(self, guid, title, subject, summary, link):
        """
        Create a NewsStory object
        globally unique identifier (GUID) – a string that serves as a unique name for this entry
        title – a string
        subject – a string
        summary – a string
        link to more content – a string
        """
        # Ensure the passed parameters are strings
#        assert type(guid) == str and type(title) == str and type(subject) == str \
#            and type(summary) == str and type(link) == str, \
#            "All parameters must be strings!"
#            
        # Assignments
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    
    # Get methods
    def get_guid(self):
        return(self.guid)
    def get_title(self):
        return(self.title)
    def get_subject(self):
        return(self.subject)
    def get_summary(self):
        return(self.summary)
    def get_link(self):
        return(self.link)

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self, word):
        # Assignemnt
        self.word = string.lower(word)
        
    def is_word_in(self, text):
        # Separate the text into words according to the possible delimiters
        delims = '|'.join(map(re.escape, string.punctuation + ' '))
        to_parse = re.split(delims, string.lower(text))
        text = string.lower(text)
        
        # Check whether the word is contained
        for p in to_parse:
#            print("Checking " + self.word + " against " + p)
            if self.word == p:
                return True
        return False

## TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    def evaluate(self, news):
        if self.is_word_in(news.get_title()):
            return True
        return False
#    
## TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    def evaluate(self, news):
        if self.is_word_in(news.get_subject()):
            return True
        return False
#
## TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    def evaluate(self, news):
        if self.is_word_in(news.get_summary()):
            return True
        return False

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.t = trigger
    
    def evaluate(self, news):
        return not self.t.evaluate(news)

# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.t1 = trigger1
        self.t2 = trigger2
    
    def evaluate(self, news):
        return self.t1.evaluate(news) and self.t2.evaluate(news)

# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.t1 = trigger1
        self.t2 = trigger2
        
    def evaluate(self, news):
        return self.t1.evaluate(news) or self.t2.evaluate(news)

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
        
    def evaluate(self, news):
        return self.phrase in news.get_subject() \
            or self.phrase in news.get_title() \
            or self.phrase in news.get_summary()

#
##======================
## Part 3
## Filtering
##======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # Create a new list to store matching stories
    filtered_stories = []
    # Iterate through the stories and check whether they match a trigger
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
    # Return all remaining stories
    return filtered_stories

##======================
## Part 4
## User-Specified Triggers
#======================

def createTriggerFromLine(triggerdict, tname, tkeyword, args, debug):
    """
    Creates a trigger based on the parameters passed from the config file.
    triggerdict = dictionary of trigger names/locations
    tname = name of trigger to be created
    tkeyword = keyword of trigger type to be created
    args = trigger arguments
    """
    # Check trigger type
    # Basic triggers use args as-is
    if tkeyword == 'TITLE':
        if debug:
            print('TITLE trigger')
        tmp_trigger = TitleTrigger(args)
    elif tkeyword == 'SUBJECT':
        if debug:
            print('SUBJECT trigger')
        tmp_trigger = SubjectTrigger(args)
    elif tkeyword == 'SUMMARY':
        if debug:
            print('SUMMARY trigger')
        tmp_trigger = SummaryTrigger(args)
    elif tkeyword == 'PHRASE':
        if debug:
            print('PHRASE trigger')
        tmp_trigger = PhraseTrigger(args)
    
    # The other triggers need to treat args as names of triggers
    else:
        targs = string.split(args, ' ')    
        if tkeyword == 'NOT':
            if debug:
                print('NOT trigger using ' + targs[0])
            tmp_trigger = NotTrigger(triggerdict[targs[0]])
        elif tkeyword == 'AND':
            if debug:
                print('AND trigger using ' + targs[0] + ', ' + targs[1])
            tmp_trigger = AndTrigger(triggerdict[targs[0]], triggerdict[targs[1]])
        elif tkeyword == 'OR':
            if debug:
                print('OR trigger using ' + targs[0] + ', ' + targs[1])
            tmp_trigger = OrTrigger(triggerdict[targs[0]], triggerdict[targs[1]])
        else:
            return None
        
    # Update trigger name pointer
    triggerdict[tname] = tmp_trigger

def readTriggerConfig(filename, debug = False):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    
    # Create variables to be used
    triggerdict = {}
    triggerlist = []
    
    # Iterate through the lines
    for line in lines:
        # Split the parsed line into parameters
        # Definitely an opportunity to clean this up some more but it works...            
        tmpline = string.split(line, ' ', maxsplit = 2)
        tname = tmpline[0]
        tkeyword = tmpline[1]
        args = tmpline[2]
        # Debug output
        if debug:
            print('=== Current config file line ===')
            print('name = ' + tname)
            print('keyword = ' + tkeyword)
            print('args = ' + args)
        
        # Check if it's an ADD line
        if tname == 'ADD':
            # Debug output
            if debug:
                print('ADD line')
            triggerlist.append(triggerdict[tkeyword])
            if debug:
                print('Adding trigger ' + tkeyword)
            for arg in string.split(args):
                if debug:
                    print('Adding trigger ' + arg)
                triggerlist.append(triggerdict[arg])
        # Create a trigger for this line
        else:
            tmp_trigger = createTriggerFromLine(triggerdict, tname, tkeyword, args, debug)
            # Debug output
            if debug:
                print('=== Current trigger dictionary ===')
                for key in triggerdict:
                    print(str(key) + ' = ' + str(triggerdict.get(key)))
                print('=== Current trigger list ===')
                for t in triggerlist:
                    print(str(t))
    
    return triggerlist
    
# Run this for debugging output
# readTriggerConfig("triggers.txt", debug = True)
            
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
#    t1 = SubjectTrigger("Trump")
#    t2 = SummaryTrigger("MIT")
#    t3 = PhraseTrigger("White House")
#    t4 = OrTrigger(t2, t3)
#    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

