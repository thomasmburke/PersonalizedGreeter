import redis
import logging
import datetime
import os

# Set logger
logger = logging.getLogger(__name__)

class GreetingOps:
    """
    GreetingOps: This module is responsible for creating a connection with the redis
        cache hosted on Google compute engine. From there it will randomly select 
        a greeting based of a few redis sets that exist.
    """

    def __init__(self):
        self.redisClient = redis.Redis(host=os.getenv('REDIS_INSTANCE_IP'), port=6379, db=0)
        self.defaultGreetings = 'defaultGreetings'

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
        personalizedGreeting = self.redisClient.srandmember(personName)
        if personalizedGreeting:
            personalizedGreetingWithName = personalizedGreeting.decode('utf-8').format(personName)
            logger.info('Retrieved personalized greeting: {}'.format(personalizedGreetingWithName))
            return personalizedGreetingWithName
        seasonalGreeting = self.redisClient.srandmember(datetime.datetime.today().strftime('%Y-%m-%d'))
        if seasonalGreeting: 
            seasonalGreetingWithName = seasonalGreeting.decode('utf-8').format(personName)
            logger.info('Retrieved seasonal greeting: {}'.format(seasonalGreetingWithName))
            return seasonalGreetingWithName
        else: 
            defaultGreeting = self.redisClient.srandmember(self.defaultGreetings)
            defaultGreetingWithName = defaultGreeting.decode('utf-8').format(personName)
            logger.info('Retrieved default greeting: {}'.format(defaultGreetingWithName))
            return defaultGreetingWithName


if __name__=='__main__':
    print(datetime.datetime.today().strftime("%Y-%m-%d"))
    print(type(datetime.datetime.today().strftime("%Y-%m-%d")))
