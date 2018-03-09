import heapq, random, math
from queue import *
import matplotlib.pyplot as plt

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
    time = event_object.time_stamp
    next_arrival_event = Event('a',Negative_Exponential_Distribution(current_lambda) + time)
    heapq.heappush(GEL, next_arrival_event) 
    packet_length_array.append(buffer_queue.qsize())

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


def append_one_to_all_hosts(event_object):
    host_one_buffer.append(Packet which will contain random byte size and random destination and time it got added event_object.time_stamp)
    host_two_buffer.append(Packet which will contain byte size and destination)
    ``
    ``
    ``
    ``
    ``
    ``
    ``
    ``
    ``
    ``
    ``

def Process_Token(event_object):
    depending on what node we are on
    If node == 1:
        check host_one_buffer if it has things then we need to send, else make new event for next time we need to check token

def Process_D(event_object):
    global time, MAXBUFFER, buffer_queue, GEL, current_lambda, packet_drop, packet_length_array,used_server_time
    append_one_to_all_hosts(event_object)
    time = event_object.time_stamp
    service_time = buffer_queue.get()

    if buffer_queue.qsize() == 0:
        pass
    else:
        departure_event = Event('d', service_time + time)
        heapq.heappush(GEL, departure_event)

        

def main():
    # Initialize 
    number_of_trials = 100000
    global time, MAXBUFFER, buffer_queue, GEL, current_lambda, packet_drop, packet_length_array,used_server_time,number_of_hosts
    lambda_trials_infinite_buffer = [.01, .05, .1, .2, .3, .5, .6, .7, .8, .9]
    utilization_graph = []
    queue_length_graph = []
    for trial in lambda_trials_infinite_buffer:
        time = 0 # Current Time
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
            else if event = 'd':
                Process_D(event_object)
            else:
                Process_Token(event_object)

        utilization_graph.append(used_server_time/time)
        queue_length_graph.append(sum(packet_length_array) / len(packet_length_array))
        print("lambda: " + str(trial) + " buffer: infinite")
        print("Utilization: " + str(used_server_time / time))
        print("Mean Queue Length: " + str(sum(packet_length_array) / len(packet_length_array)))
        print("Packet Drop: " + str(packet_drop)) 
        print()
    plt.plot(lambda_trials_infinite_buffer,utilization_graph)
    plt.ylabel('Server Utilization')
    plt.xlabel('Lambda Rate Value')
    plt.title('Server Utilization for Infinite Buffer')
    plt.show()
    plt.plot(lambda_trials_infinite_buffer,queue_length_graph)
    plt.ylabel('Average Queue Length')
    plt.xlabel('Lambda Rate Value')
    plt.title('Average Queue Length for Infinite Buffer')
    plt.show()


if __name__ == "__main__":
    main()
