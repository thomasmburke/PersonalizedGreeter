#import redis
import logging
import datetime
import os
import holidays
from dateutil.easter import easter
import random

# Set logger
logger = logging.getLogger(__name__)

class GreetingOps:
    """
    GreetingOps: This module is responsible for creating a connection with the redis
        cache hosted on Google compute engine. From there it will randomly select
        a greeting based of a few redis sets that exist.
    """

    def __init__(self):
        #self.redisClient = redis.Redis(host=os.getenv('REDIS_INSTANCE_IP'), port=6379, db=0)
        self.defaultGreetings = 'defaultGreetings'
        self.seasonalGreetingDict = {'12-24':'christmasGreetings', '12-25': 'christmasGreetings',
            '04-01': 'aprilFoolsGreetings', "01-01": "newYearsGreetings",
            "Thanksgiving": "thanksgivingGreetings", "Easter": "easterGreetings",
            "03-17": "saintpatricksdayGreetings"}
        # Didnt want to pay for Redis on the cloud so just going to use a dictionary...
        self.greetings = {"defaultGreetings" : ["<speak>Greetings and Salutations {}!</speak>",
        "<speak>Howdy, Howdy, Howdy {}!</speak>",
        "<speak>Howdy doody {}!</speak>",
        "<speak>{}, Ahoy, Matey</speak>",
        "<speak>What's crackin {}?</speak>",
        "<speak>{}, This may be recorded for training purposes</speak>",
        "<speak>Why, hello there {}</speak>",
        "<speak>Konnichiwa {}</speak>",
        "<speak>Aloha {}</speak>",
        "<speak>Breaker, Breaker {} has arrived <break time='1s'/> Copy that</speak>",
        "<speak>{}, I hope you are having a wonderful day</speak>",
        "<speak>Ciao {}</speak>",
        "<speak>What's cookin {}?</speak>",
        "<speak>Beautiful day outside isn't it {}?</speak>",
        "<speak>Yo, {} its good to see you again</speak>",
        "<speak>Hey there {}, welcome to the Burke household</speak>",
        "<speak>Hi, Welcome to McDonalds my name is {}. How can I help you?</speak>",
        "<speak>Want to hear Victoria's Secret? <break time='1s'/><amazon:effect name='whispered'>She has a crush on {}</amazon:effect></speak>",
        "<speak>Yo ho, yo ho its a pirates life for {}</speak>",
        "<speak>What's happenin {}?</speak>",
        "<speak>Knock, Knock <break time='1s'/> Well, {} why don't you try and find out!</speak>",
        "<speak>{}, you are not allowed please turn back now!</speak>",
        "<speak>{}, I told you never to come back here, for what reason have you shown your face</speak>",
        "<speak>Hello {}, please do not forget to tip the door man</speak>",
        "<speak>Do you {} take this personalized machine learning greeter as you lawfully wedded wife?</speak>",
        "<speak>Welcome {}, please feel free to make yourself at home</speak>"],
        "christmasGreetings" : ["<speak>Hey, {}. Why does Santa Claus have such a big sack? <break time='1s'/> He only comes once a year!</speak>",
        "<speak>Hey, {}. Why does Santa always come through the chimney?<break time='1s'/>Because he knows better than to try the back door.</speak>",
        "<speak>Hey, {}. What’s the difference between snowmen and snowwomen?<break time='1s'/>Snowballs</speak>",
        "<speak>Hey, {}. What’s the difference between Tiger Woods and Santa?<break time='1s'/>Santa was smart enough to stop at three ho's.</speak>",
        "<speak>Hey, {}. Why did the Grinch rob the liquor store?<break time='1s'/>He was desperate for some holiday spirit.</speak>",
        "<speak>Hey, {}. Why does Santa go to strip clubs?<break time='1s'/>To visit all his ho ho ho’s.</speak>",
        "<speak>Hey, {}. Is your name Jingle Bells?<break time='1s'/>Cause you look ready to go all the way.</speak>"],
        "aprilFoolsGreetings" : ["<speak>Hey, {}. Your shoe is untied.<break time='1s'/>April Fools!</speak>",
        "<speak>Hey, {}. Who is that guy behind you?<break time='1s'/>Just kidding, April Fools!</speak>",
        "<speak>Hey, {}. Looks like you dropped something<break time='1s'/>April Fools!</speak>"],
        "thanksgivingGreetings" : ["<speak>Hey, {}. What does Miley Cyrus eat for Thanksgiving?<break time='1s'/>Twerky</speak>",
        "<speak>Hey, {}. What kind of music did the Pilgrims like?<break time='1s'/>Plymouth Rock</speak>",
        "<speak>Hey, {}. Why was the Thanksgiving soup so expensive?<break time='1s'/>It had 24 carrots</speak>",
        "<speak>Hey, {}. What did baby corn say to mama corn?<break time='1s'/>Where's pop corn</speak>",
        "<speak>Hey, {}. What did the turkey say before it was roasted?<break time='1s'/>Boy! I'm stuffed.</speak>",
        "<speak>Hey, {}. What do you call a running turkey?<break time='1s'/>Fast food!</speak>"],
        "easterGreetings" : ["<speak>Hey, {}. What did the Easter egg say to the boiling water?<break time='1s'/>It might take me a while to get hard cause I just got laid by some chick.</speak>",
        "<speak>Hey, {}. Why wouldn't you want to be an Easter egg?<break time='1s'/>You only get laid once.</speak>",
        "<speak>Hey, {}. Why is Easter an Alzheimer patient's favorite holiday?<break time='1s'/>They get to hide their own eggs.</speak>",
        "<speak>Hey, {}. How do you make Easter easier?<break time='1s'/>Replace the t with an i.</speak>",
        "<speak>Hey, {}. Where does the Easter Bunny get his eggs?<break time='1s'/>From egg plants</speak>",
        "<speak>Hey, {}. How should you send a letter to the Easter Bunny?<break time='1s'/>By hare mail</speak>"],
        "saintpatricksdayGreetings" : ["<speak>Hey, {}. break time='1s'/></speak>",
        "<speak>Hey, {}. Why can't you borrow money from a leprechaun?<break time='1s'/>Because they're always a little short</speak>",
        "<speak>Hey, {}. Are you from Ireland?<break time='1s'/>Because when I look at you my penis is Dublin</speak>",
        "<speak>Hey, {}. What do you call a potato that's not Irish?<break time='1s'/>A french fry</speak>"],
        "newYearsGreetings" : ["<speak>Hey, {}. A new years resolution is something that goes in one year and out the other.</speak>",
        "<speak>Hey, {}. hope you popped of this year because tonight will be even crazier.</speak>"],
        "laborDayGreetings" : ["<speak>Did you hear about the Labor Day joke? It doesn't work for me.</speak>"]}

    def get_greeting(self, personName):
        """
        Summary: Check if there is any custom greetings for the specific
            personName. If not check if there are any seasonal greetings for
            the current day. If not - Lastly grab a default greeting and inject
            the person's name.
        Params: personName (STRING) - Name of the guest that is detected
        Return: (STRING) - greeting with name injected
        """
        logger.info('Entering the greeting retrieval method...')
        #personalizedGreeting = self.redisClient.srandmember(personName)
        #if personalizedGreeting:
        if personName in self.greetings:
            # personalizedGreetingWithName = personalizedGreeting.decode('utf-8').format(personName)
            personalizedGreetingWithName = self.get_random_greeting(self.greetings[personName]).format(personName)
            logger.info('Retrieved personalized greeting: {}'.format(personalizedGreetingWithName))
            return personalizedGreetingWithName
        # Check to see if it is thanksgiving or easter
        oddDay = self.is_odd_holiday()
        # seasonalGreeting = self.redisClient.srandmember(datetime.datetime.today().strftime('%m-%d')) if not oddDay else self.redisClient.srandmember(oddDay)
        seasonalGreeting = self.greetings.get(datetime.datetime.today().strftime('%m-%d')) if not oddDay else self.greetings.get(oddDay)

        if seasonalGreeting:
            # seasonalGreetingWithName = seasonalGreeting.decode('utf-8').format(personName)
            seasonalGreetingWithName = self.get_random_greeting(seasonalGreeting).format(personName)
            logger.info('Retrieved seasonal greeting: {}'.format(seasonalGreetingWithName))
            return seasonalGreetingWithName
        else:
            # defaultGreeting = self.redisClient.srandmember(self.defaultGreetings)
            defaultGreeting = self.get_random_greeting(self.greetings[self.defaultGreetings])
            logger.info(defaultGreeting)
            # defaultGreetingWithName = defaultGreeting.decode('utf-8').format(personName)
            defaultGreetingWithName = defaultGreeting.format(personName)
            logger.info('Retrieved default greeting: {}'.format(defaultGreetingWithName))
            return defaultGreetingWithName

    def is_odd_holiday(self):
        if easter(datetime.datetime.today().year) == datetime.datetime.today().date():
            return 'Easter'
        oddDay = holidays.US().get(datetime.datetime.today().strftime("%Y-%m-%d"))
        return oddDay if oddDay == 'Thanksgiving' else None

    def get_random_greeting(self, greetingList):
        return random.choice(greetingList)


if __name__=='__main__':
    obj = GreetingOps()
    print(obj.get_greeting('Tom Burke'))
