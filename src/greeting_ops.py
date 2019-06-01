import redis
import logging
import datetime
import os
import holidays
from dateutil.easter import easter

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
        self.seasonalGreetingDict = {'12-24':'christmasGreetings', '12-25': 'christmasGreetings',
            '04-01': 'aprilFoolsGreetings', "01-01": "newYearsGreetings", 
            "Thanksgiving": "thanksgivingGreetings", "Easter": "easterGreetings",
            "03-17": "saintpatricksdayGreetings"}

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
        # Check to see if it is thanksgiving
        oddDay = self.is_odd_holiday()
        seasonalGreeting = self.redisClient.srandmember(datetime.datetime.today().strftime('%m-%d')) if not oddDay else self.redisClient.srandmember(oddDay)
        if seasonalGreeting: 
            seasonalGreetingWithName = seasonalGreeting.decode('utf-8').format(personName)
            logger.info('Retrieved seasonal greeting: {}'.format(seasonalGreetingWithName))
            return seasonalGreetingWithName
        else: 
            defaultGreeting = self.redisClient.srandmember(self.defaultGreetings)
            logger.info(defaultGreeting)
            defaultGreetingWithName = defaultGreeting.decode('utf-8').format(personName)
            logger.info('Retrieved default greeting: {}'.format(defaultGreetingWithName))
            return defaultGreetingWithName

    def is_odd_holiday(self):
        if easter(datetime.datetime.today().year) == datetime.datetime.today().date():
            return 'Easter'
        oddDay = holidays.US().get(datetime.datetime.today().strftime("%Y-%m-%d")) 
        return oddDay if oddDay == 'Thanksgiving' else None


if __name__=='__main__':
    day = datetime.datetime.today().strftime("%Y-%m-%d")
    us_holidays = holidays.US()
    print(us_holidays.get('2019-04-21'))
    print(easter(datetime.datetime.today().year))
    print(datetime.datetime.strptime('2019-04-21',"%Y-%m-%d").date())
    print(datetime.datetime.today().date())
    print(easter(datetime.datetime.today().year) == datetime.datetime.strptime('2019-04-21',"%Y-%m-%d").date())
