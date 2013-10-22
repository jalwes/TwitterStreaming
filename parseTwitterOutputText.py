#!usr/local/bin/python
#Written by Jon Alwes
#August 29th, 2013

######################################################################################################################
###This block will open the output file from the TwitterStreaming.py script and parse it, looking for tweets  ######## 
###that are just ads and thus should  not be included in any sort of trend predictions. I have added a list of #######
###ad_identifiers which can easily be updated should we discover another word that is indicative of an ad.  ##########
######################################################################################################################


###Set up lists that contain words most likely to mean tweet is an advertisement
ad_identifiers = ["win", "Win", "WIN", "Order", "EGO-T", "Deal", "Deals", "deal", "deals", "click here", "Click here", "Click Here"]
###List that contains keywords we're looking for
keywords = ["e-cigarette", "E-cigarette", "e-Cigarette", "E-Cigarette", "e cigarette", "E cigarette", "E Cigarette", "E cig", "E Cig", "e cig", "e Cig", "e-cig", "E-cig", "e-Cig", "E-Cig", "E-CIG", "E-CIGARETTE"]

raw_output = open('out.txt', 'r')
edited_output = open('edited_output.txt', 'w')


for line in raw_output:
	valid_tweet=0
	
	#if one of our keywords is in the line, the tweet is valid
	for keyword in keywords:
		if keyword in line:
			valid_tweet=1
	
	#if the tweet is valid so far, screen it against our ad_identifiers.
	#If one of our ad_identifer keywords is found, it's not a valid_tweet.	
	if (valid_tweet==1):
		for word in ad_identifiers:
			if word in line:
				valid_tweet=0
			
	#We don't want to keep the blank lines otherwise we could have huge gaps in 
	#our final output if successive tweets aren't valid. 
	if line in ['\n', '\r\n']:
		valid_tweet = 0
		
	#If valid_tweet, write to final_output
	if (valid_tweet == 1):
		edited_output.write(line+"\n")
		
#for line in raw_output:
#	#data = line.encode('ascii','ignore')
#	ad = 0
#	for word in ad_identifiers:
#		if word in line:
#			ad=1
#		if line in ['\n', '\r\n']:
#			ad=1
#	if(ad==0):
#	  edited_output.write(line+"\n")
		
raw_output.close()
edited_output.close()

######################################################################################################################
###This next block is to remove duplicates for the final_output.txt file. This opens up the previously created   ##### 
### "edited_output.txt", goes through each line, and if the line hasn't been seen yet it adds the line to the    ##### 
### list named "lines" and adds this string to the set "seen." Finally, it writes the list to final_output.txt.  #####                               
######################################################################################################################


lines = []
seen = set()

edited_output = open('edited_output.txt', 'r')
for line in edited_output:
	if line not in seen:
		lines.append(line)
		seen.add(line)
	
edited_output.close()


final_output = open('final_output.txt', 'w')
for line in lines:
	final_output.write(line+"\n")
	

	
	
#######################################################################################################################
###  Print some stats to the file #####################################################################################
#######################################################################################################################

###write to file how many tweets there are in the file
final_output.write("\n\n\n")
final_output.write("There are " + str(len(lines)) + " tweets in final_output.txt")
print(len(lines))
final_output.close()