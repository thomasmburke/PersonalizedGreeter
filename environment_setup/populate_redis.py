import redis
import os
import pickle

defaultGreetings = {'<speak>Greetings and Salutations {}!</speak>', 
        '<speak>Howdy, Howdy, Howdy {}!</speak>',
        '<speak>Howdy doody {}!</speak>',
        '<speak>{}, Ahoy, Matey</speak>',
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
        "<speak>Hi, Welcome to McDonalds my name is {}. How can I help you?</speak>"
        "<speak>Want to hear Victoria's Secret? <break time='1s'/><amazon:effect name='whispered'>She has a crush on {}</amazon:effect></speak>",
        "<speak>Yo ho, yo ho its a pirates life for {}</speak>",
        "<speak>What's happenin {}?</speak>",
        "<speak>Knock, Knock <break time='1s'/> Well, {} why don't you try and find out!</speak>",
        "<speak>{}, you are not allowed please turn back now!</speak>",
        "<speak>{}, I told you never to come back here, for what reason have you shown your face</speak>",
        "<speak>Hello {}, please do not forget to tip the door man</speak>",
        "<speak>Do you {} take this personalized machine learning greeter as you lawfully wedded wife?</speak>",
        "<speak>Welcome {}, please feel free to make yourself at home</speak>"}
christmasGreetings = {"<speak>Hey, {}. Why does Santa Claus have such a big sack? <break time='1s'/> He only comes once a year!</speak>"}
with open('./greetings/defaultGreetings.pkl', 'wb') as defaultPickleFile:
    pickle.dump(defaultGreetings, defaultPickleFile)
redisClient = redis.Redis(host=os.getenv('REDIS_INSTANCE_IP'), port=6379, db=0)
redisClient.delete('defaultGreetings')
redisClient.sadd('defaultGreetings', *defaultGreetings)
mems = redisClient.smembers(name='defaultGreetings')
rand = redisClient.srandmember('defaultGreetings')
print(rand)
