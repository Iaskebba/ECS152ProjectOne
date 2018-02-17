import heapq, random, math, queue


double negative-exponentially-distributed-time(double rate)
{
        double u;
        u = drand48();
        return ((-1/rate) * log(1-u));
}

# given lambda = .1 = rate
def negative_exponential_distibution(rate):
    u = random.uniform(0,1)
    return ((-1/rate) * math.log(1-u))

class Event:
    def __init__(self, event_type, time_stamp):
        self.event_type = event_type
        self.time_stamp = time_stamp

    def __cmp__(self, other):
        return cmp(self.time_stamp, other.time_stamp)

def main():
    MAXBUFFER = math.inf # This is a variable to each test case
    random.expovariate()# THIS WILL BE LAMBDA
    number_of_trials = 10000
    length = 0 # Number of packets in queue (BUFFER) including those being transmitted by server
    time = 0 # Current time
    queue = Queue()
    GEL = []
    first_event = Event('a',0)
    heapq.heappush(GEL, first_event)

    # SET THE SERVICE RATE AND ARRIVAL RATE OF PACKETS
    # Create first arrival event and insert into GEL.
    # Event time of first arrival is obtained by adding random generated inter-arrival time to current time (0)
    # u = 0 - 1 random
    # lambda = 
    for i in range(number_of_trials):






if __name__ == "__main__":
    main()
