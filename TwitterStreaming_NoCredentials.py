#!usr/local/bin/python

import time
from twython import Twython
from twython import TwythonStreamer
from datetime import date
from datetime import datetime


APP_KEY = #Add APP_KEY here
APP_SECRET = #Add APP_SECRET here 
OAUTH_TOKEN = #Add OAUTH_TOKEN here
OAUTH_TOKEN_SECRET = #Add OAUTH_TOKEN_SECRET here

first_status_id = 0
last_status_id = 0
count = 1

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

class MyStreamer(TwythonStreamer):
    #Twitter API will not match phrases. So, for example, the keyword "E Cigarette" will return a match 
    #if the tweet contains "Cigarette" or "E". We will process the tweets on our end to 
    #not include those tweets that only contain mentions of "cigarette" and not some form 
    #of "E Cigarette". We will do this by defining an array of differently worded terms 
    #for "E Cigarette" with different casing. We will then not include those tweets that do not 
    #contain any of the keywords in our array. 
    
    def on_success(self, data):
        if 'text' in data:
            #get status_id of first relevant tweet so we can use this 
            #as a starting boundary for a possible search later to backfill in case
            #of a disconnect from Twitter API
            #if count == 1:
            #    first_status_id = data['status_id']
            #    count++
            #everything below works
            try:
                #in case of disconnect get status ID of this tweet so we may backfill 
                #data using the REST API if need be. 
                print(first_status_id)
                f = open('out.txt', 'a')
                f.write(data['text']+"\n\n")
                f.close() 
            except:
                print("error writing tweet to file")
                
    def on_error(self, status_code, data):
        #print(status_code)
        status = open('statusFile.txt', 'a')
        status.write(status_code)
        status.close()
        #self.disconnect()
        
    def on_disconnect(self, data):
        try: 
            today = date.today()
            time = datetime.now().time()
            print(today)
            print (time)            
            d = open('disconnect.txt', 'a')
            d.write("Disconnected due to " +data)
            d.write(today)
            d.write(time)
            d.close()
        except:
            print("Disconnected.")
    
stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='e Cigarette')

#Maybe some method down here to open the output file and go through it line 
#by line. If a line doesn't contain any of the keywords, don't write it to the final 
#output file?

#keywords = ["e-cigarette", "E-cigarette", "e-Cigarette", "E-Cigarette", "e cigarette", "E cigarette", "E Cigarette", "E cig", "E Cig", "e cig", "e Cig", "e-cig", "E-cig", "e-Cig", "E-Cig"]

#Advertisement tweets will have certain keywords in them also
#The "EGO-T" keeps showing up repeatedly in results, it is an advertisement. 
#ads = ["win", "Win", "WIN", "Order", "EGO-T"
#temp = data['text']
            #for keyword in keywords:
             #   if keyword in temp:
                    #this comparison may not work if the tweet is in certain languages 
                    #due to it being non-UTF-8 encoded in which case the tweet will still write to 
                    #the out file if it passes Twitter's track method. (e.g. A tweet that contains #"cigarette" but is otherwise in a non-encoded language)