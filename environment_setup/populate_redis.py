import redis
import os
import pickle

greetings = {"defaultGreetings" : {"<speak>Greetings and Salutations {}!</speak>", 
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
        "<speak>Welcome {}, please feel free to make yourself at home</speak>"},
        "christmasGreetings" : {"<speak>Hey, {}. Why does Santa Claus have such a big sack? <break time='1s'/> He only comes once a year!</speak>",
        "<speak>Hey, {}. Why does Santa always come through the chimney?<break time='1s'/>Because he knows better than to try the back door.</speak>",
        "<speak>Hey, {}. What’s the difference between snowmen and snowwomen?<break time='1s'/>Snowballs</speak>",
        "<speak>Hey, {}. What’s the difference between Tiger Woods and Santa?<break time='1s'/>Santa was smart enough to stop at three ho's.</speak>",
        "<speak>Hey, {}. Why did the Grinch rob the liquor store?<break time='1s'/>He was desperate for some holiday spirit.</speak>",
        "<speak>Hey, {}. Why does Santa go to strip clubs?<break time='1s'/>To visit all his ho ho ho’s.</speak>",
        "<speak>Hey, {}. Is your name Jingle Bells?<break time='1s'/>Cause you look ready to go all the way.</speak>"},
        "aprilFoolsGreetings" : {"<speak>Hey, {}. Your shoe is untied.<break time='1s'/>April Fools!</speak>",
        "<speak>Hey, {}. Who is that guy behind you?<break time='1s'/>Just kidding, April Fools!</speak>",
        "<speak>Hey, {}. Looks like you dropped something<break time='1s'/>April Fools!</speak>"},
        "thanksgivingGreetings" : {"<speak>Hey, {}. What does Miley Cyrus eat for Thanksgiving?<break time='1s'/>Twerky</speak>",
        "<speak>Hey, {}. What kind of music did the Pilgrims like?<break time='1s'/>Plymouth Rock</speak>",
        "<speak>Hey, {}. Why was the Thanksgiving soup so expensive?<break time='1s'/>It had 24 carrots</speak>",
        "<speak>Hey, {}. What did baby corn say to mama corn?<break time='1s'/>Where's pop corn</speak>",
        "<speak>Hey, {}. What did the turkey say before it was roasted?<break time='1s'/>Boy! I'm stuffed.</speak>",
        "<speak>Hey, {}. What do you call a running turkey?<break time='1s'/>Fast food!</speak>"},
        "easterGreetings" : {"<speak>Hey, {}. What did the Easter egg say to the boiling water?<break time='1s'/>It might take me a while to get hard cause I just got laid by some chick.</speak>",
        "<speak>Hey, {}. Why wouldn't you want to be an Easter egg?<break time='1s'/>You only get laid once.</speak>",
        "<speak>Hey, {}. Why is Easter an Alzheimer patient's favorite holiday?<break time='1s'/>They get to hide their own eggs.</speak>",
        "<speak>Hey, {}. How do you make Easter easier?<break time='1s'/>Replace the t with an i.</speak>",
        "<speak>Hey, {}. Where does the Easter Bunny get his eggs?<break time='1s'/>From egg plants</speak>",
        "<speak>Hey, {}. How should you send a letter to the Easter Bunny?<break time='1s'/>By hare mail</speak>"},
        "saintpatricksdayGreetings" : {"<speak>Hey, {}. break time='1s'/></speak>",
        "<speak>Hey, {}. Why can't you borrow money from a leprechaun?<break time='1s'/>Because they're always a little short</speak>",
        "<speak>Hey, {}. Are you from Ireland?<break time='1s'/>Because when I look at you my penis is Dublin</speak>",
        "<speak>Hey, {}. What do you call a potato that's not Irish?<break time='1s'/>A french fry</speak>"},
        "newYearsGreetings" : {"<speak>Hey, {}. A new years resolution is something that goes in one year and out the other.</speak>",
        "<speak>Hey, {}. hope you popped of this year because tonight will be even crazier.</speak>"},
        "laborDayGreetings" : {"<speak>Did you hear about the Labor Day joke? It doesn't work for me.</speak>"}}

"""
memorial day
presidents day
MLK day
Columbus day
independence day / 4th of july
Ghandis bday  october 2
Diwali
"""


with open('./greetings/greetings.pkl', 'wb') as defaultPickleFile:
    pickle.dump(greetings, defaultPickleFile)
redisClient = redis.Redis(host=os.getenv('REDIS_INSTANCE_IP'), port=6379, db=0)
for key, greeting in greetings.items():
    redisClient.sadd(key, *greeting)
    mems = redisClient.smembers(name=key)
    rand = redisClient.srandmember(key)
    print(mems)
    print(rand)
