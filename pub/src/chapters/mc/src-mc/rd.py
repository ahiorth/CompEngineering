from datetime import date
import random

def get_date():
    """ return a random date in the current year """
    start_dt = date.today().replace(day=1, month=1).toordinal()
    end_dt = date.today().replace(day=31, month=12).toordinal()
    random_day = date.fromordinal(random.randint(start_dt, end_dt))
    return random_day

def get_day():
    """ return a random day in a year """
    return random.randint(1,365)

def NoPeople(p):
    """ pick random dates in a year, return 1 if two
        is in the same date before p is reached """
    dates=[]
    for n in range(p):
        date=get_day()
        if date in dates:
            return 1
        else:
            dates.append(date)
    return 0
        
def BP(p, N):
    prob=0.;
    for i in range(1,N):
        prob += NoPeople(p)
    return prob/N

print(BP(23,100000))

