import redis
import logging
import datetime

# Set logger
logger = logging.getLogger(__name__)

class GreetingOps:

    def __init__(self):
        self.redisClient = redis.Redis(host=os.getenv('REDIS_INSTANCE_IP'), port=6379, db=0)
        self.defaultGreetings = 'defaultGreetings'

    def get_greeting(self, personName):
        logger.info('Entering the greeting retrieval method...')
        personalizedGreeting = self.redisClient.srandmember(personName)
        if personalizedGreeting: return personalizedGreeting
        seasonalGreeting = self.redisClient.srandmember(datetime.datetime.today().strftime('%Y-%m-%d'))
        if seasonalGreeting: return seasonalGreeting
        else: return self.redisClient.srandmember(self.defaultGreetings)


if __name__=='__main__':
    print(datetime.datetime.today().strftime("%Y-%m-%d"))
    print(type(datetime.datetime.today().strftime("%Y-%m-%d")))
