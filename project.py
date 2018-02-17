import heapq, random, math, queue

# given lambda = .1 = rate
def Negative_Exponential_Distribution(rate):
    u = random.uniform(0,1)
    return ((-1/rate) * math.log(1-u))

class Event:
    def __init__(self, event_type, time_stamp):
        self.event_type = event_type
        self.time_stamp = time_stamp

    def __cmp__(self, other):
        return cmp(self.time_stamp, other.time_stamp)

def Process_A(event_object):
    
def Process_D(event_object):

def main():
    # Initialize 
    number_of_trials = 10000
    global time, MAXBUFFER, length, buffer_queue, GEL 
    time = 0 # Current Time
    length = 0 # Number of packets in queue (BUFFER) including those being transmitted by server
    MAXBUFFER = math.inf # This is a variable to each test case
    buffer_queue = Queue() # buffer Queue
    GEL = [] # Global Event List 

    first_event = Event('a',0)
    heapq.heappush(GEL, first_event)

    for i in range(number_of_trials):
        event_object = heapq.heappop(GEL)
        if event_object.event_type == 'a':
            Process_A(event_object) 
        else:
            Process_D(event_object)

if __name__ == "__main__":
    main()
