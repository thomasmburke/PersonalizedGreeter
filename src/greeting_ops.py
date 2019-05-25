import redis
import logging
import datetime
import os

# Set logger
logger = logging.getLogger(__name__)

class GreetingOps:

    def __init__(self):
        self.redisClient = redis.Redis(host=os.getenv('REDIS_INSTANCE_IP'), port=6379, db=0)
        self.defaultGreetings = 'defaultGreetings'

    def get_greeting(self, personName):
        logger.info('Entering the greeting retrieval method...')
        personalizedGreeting = self.redisClient.srandmember(personName)
        if personalizedGreeting:
            personalizedGreetingWithName = personalizedGreeting.format(personName)
            logger.info('Retrieved personalized greeting: {}'.format(personalizedGreetingWithName))
            return personalizedGreetingWithName
        seasonalGreeting = self.redisClient.srandmember(datetime.datetime.today().strftime('%Y-%m-%d'))
        if seasonalGreeting: 
            seasonalGreetingWithName = seasonalGreeting.format(personName)
            logger.info('Retrieved seasonal greeting: {}'.format(seasonalGreetingWithName))
            return seasonalGreetingWithName
        else: 
            defaultGreeting = self.redisClient.srandmember(self.defaultGreetings)
            defaultGreetingWithName = defaultGreeting.format(personName)
            logger.info('Retrieved default greeting: {}'.format(defaultGreetingWithName))
            return defaultGreetingWithName


if __name__=='__main__':
    print(datetime.datetime.today().strftime("%Y-%m-%d"))
    print(type(datetime.datetime.today().strftime("%Y-%m-%d")))
