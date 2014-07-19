Track Class Availability
========================

Track Class Availability (trackClassAvailability.py) is a tool written in Python (2.7) that allows a user to track numerous classes through WebTMS. The user can choose whether to be notified when a section opens or closes. Track Class Availability will then check all your classes via WebTMS every hour to see if the sections you are tracking open or close. If the classes you are tracking open or close, you will be notified of the status change via email.

The subject of the aforementioned email will look something like:

![An example of a subject](/readme-images/subject.png)

The body of the aforementioned email will look something like:

![An example of a body](/readme-images/body.png)

##Note

Anyone can help out with this, I wanted to do this myself but I don't have much time to work on it, so I am opening it up to anyone that wants to work on it can. 

##In work

- [ ] Go through and add features that are on the `Planned Features` list

##To-Do

Nothing...as of now...

##Planned Features
	1. Add a configuration file that allows a user to set the frequency that the program checks WebTMS, change the from email address, change the to email address and other configurations I probably can't think of right now.
	2. Check if a professor is added to the section you want and email you when a professor is assigned to a section.
	3. Any other features that I think of or users think of, we can add or remove features from the list as we please.

##Finished
- [x] Delete the class or handle the class in such a way so that multiple emails aren't sent about the same class status. As of now if a class opens or closes, it doesn't delete the class from the txt file, so it will send an email about the class even after it opens or closes. 
- [x] Check if the program works with the major e-mail providers, currently only tested with gmail. (only works with drexel email or gmail.)
- [x] Track multiple classes (heinst)
- [x] When the program doesn't find the txt file, it creates one, it then quits. A nice feature is that if it created the file, then read the newly created file instead of quiting. (Thanks, hassanNS!)
- [x] Sends email if class is opened or closed.
- [x] Can read from text file and get information needed to check the status of the class	
