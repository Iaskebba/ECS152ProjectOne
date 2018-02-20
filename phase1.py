import heapq, random, math
from queue import *

# given lambda = .1 = rate
def Negative_Exponential_Distribution(rate):
    u = random.uniform(0,1)
    return ((-1/rate) * math.log(1-u))

class Event:
    def __init__(self, event_type, time_stamp):
        self.event_type = event_type
        self.time_stamp = time_stamp

    def __lt__(self, other):
        return (self.time_stamp < other.time_stamp)

    def __eq__(self, other):
        return (self.time_stamp == other.time_stamp)

def Process_A(event_object):
    global time, MAXBUFFER, buffer_queue, GEL, current_lambda, packet_drop, packet_length_array,used_server_time
    packet_length_array.append( (event_object.time_stamp- time)* (buffer_queue.qsize()) )
    time = event_object.time_stamp
    next_arrival_event = Event('a',Negative_Exponential_Distribution(current_lambda) + time)
    heapq.heappush(GEL, next_arrival_event)



    # Test for space
    if buffer_queue.qsize() == 0:
        service_time = Negative_Exponential_Distribution(1)
        buffer_queue.put(service_time) # 1 is mu
        departure_event = Event('d', service_time + time)
        heapq.heappush(GEL, departure_event)
        tmp = used_server_time + service_time
        used_server_time = tmp
    elif buffer_queue.qsize() <= MAXBUFFER:
        service_time = Negative_Exponential_Distribution(1)
        buffer_queue.put(service_time) # 1 is mu
        used_server_time += service_time
    else:
        packet_drop += 1

def Process_D(event_object):
    global time, MAXBUFFER, buffer_queue, GEL, current_lambda, packet_drop, packet_length_array,used_server_time
    packet_length_array.append( (event_object.time_stamp- time)* (buffer_queue.qsize()) )
    time = event_object.time_stamp
    service_time = buffer_queue.get()

    if buffer_queue.qsize() == 0:
        pass
    else:
        departure_event = Event('d', service_time + time)
        heapq.heappush(GEL, departure_event)



def main():
    # Initialize
    number_of_trials = 10000
    global time, MAXBUFFER, buffer_queue, GEL, current_lambda, packet_drop, packet_length_array,used_server_time
    lambda_trials_infinite_buffer = [.1, .25, .4, .55, .65, .8, .9]
    for trial in lambda_trials_infinite_buffer:
        time = 0 # Current Time
        #length = 0 # Number of packets in queue (BUFFER) including those being transmitted by server
        MAXBUFFER = math.inf # This is a variable to each test case
        buffer_queue = Queue() # buffer Queue
        GEL = [] # Global Event List

        #statistics
        packet_length_array = []
        used_server_time = 0
        packet_drop = 0

        current_lambda = trial

        first_event = Event('a',0)
        heapq.heappush(GEL, first_event)

        for i in range(number_of_trials):
            event_object = heapq.heappop(GEL)
            if event_object.event_type == 'a':
                Process_A(event_object)
            else:
                Process_D(event_object)

        print("lambda: " + str(trial) + " buffer: infinite")
        print("Utilization: " + str(used_server_time / time))
        print("Mean Queue Length: " + str(sum(packet_length_array) / time))
        print("Packet Drop: " + str(packet_drop))
        print()
    buffer_sizes = [1,20,50]
    lambda_trials = [.2,.4,.6,.8,.9]
    for trial in lambda_trials:
        for buffer_size in buffer_sizes:
            time = 0 # Current Time
            #length = 0 # Number of packets in queue (BUFFER) including those being transmitted by server
            MAXBUFFER = buffer_size # This is a variable to each test case
            buffer_queue = Queue() # buffer Queue
            GEL = [] # Global Event List

            #statistics
            packet_length_array = []
            used_server_time = 0
            packet_drop = 0

            current_lambda = trial

            first_event = Event('a',0)
            heapq.heappush(GEL, first_event)

            for i in range(number_of_trials):
                event_object = heapq.heappop(GEL)
                if event_object.event_type == 'a':
                    Process_A(event_object)
                else:
                    Process_D(event_object)
            print("lambda: " + str(trial) + " buffer: " + str(buffer_size))
            print("Utilization: " + str(used_server_time / time))
            print("Mean Queue Length: " + str(sum(packet_length_array) / time))
            print("Packet Drop: " + str(packet_drop))
            print()


if __name__ == "__main__":
    main()
