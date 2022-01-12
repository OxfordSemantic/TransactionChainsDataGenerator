import datetime
import random
import uuid
from faker import Faker

fake = Faker(locale='en-US')

# Data generation basis (configurable)
amountStep = 1000
amountMinMultiplier = 1
amountMaxMultiplier = 10000
extraMultipliers = [1, 10, 100]

chainLowerBound = 0.5
chainUpperBound = 1.1
chainStepBound = 1.1

# Helper functions

def generateFileName(core, type, number, extension):
    return core + "/" + type + "-" + str(number) + "." + extension

def generateFirstName():
    return fake.first_name()

def generateLastName():
    return fake.last_name()

def generateCompanyName():
    return fake.company()

def generateAmount():
    return amountStep*random.randint(amountMinMultiplier, amountMaxMultiplier)*random.choice(extraMultipliers)

def generateDatetime(start, maxDaysBefore):
    return (start - random.random() * datetime.timedelta(days=maxDaysBefore)).replace(microsecond=0)

def generateParty():
    return {
        'exited': 'N',
        'internal': 'Y',
        'id': uuid.uuid4().hex,
        'firstName': generateFirstName(),
        'lastName': generateLastName()
    }

def generatePartyPair(parties):
    originator = random.choice(parties)
    beneficiary = random.choice(parties)

    while(originator['id'] == beneficiary['id']):
        beneficiary = random.choice(parties)

    return (originator, beneficiary)
