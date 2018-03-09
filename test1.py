import heapq, random, math
from queue import *
import matplotlib.pyplot as plt
import numpy as np

# given lambda = .1 = rate
def Negative_Exponential_Distribution(rate):
    u = random.uniform(0,1)
    return ((-1/rate) * math.log(1-u))

def Pareto_Distribution(rate):
    return np.random.pareto(rate)
    #u = random.uniform(0,1)
    #return ((1*rate)/u)

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
    next_arrival_event = Event('a',Pareto_Distribution(current_lambda) + time)
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

def Process_D(event_object):
    global time, MAXBUFFER, buffer_queue, GEL, current_lambda, packet_drop, packet_length_array,used_server_time
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
    utilization_graph = []
    queue_length_graph = []
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
    buffer_sizes = [1,20,50]
    lambda_trials = [.2,.4,.6,.8,.9]
    for buffer_size in buffer_sizes:
        packet_drop_graph = []
        for trial in lambda_trials:
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
            packet_drop_graph.append(packet_drop)
            print("lambda: " + str(trial) + " buffer: " + str(buffer_size))
            print("Utilization: " + str(used_server_time / time))
            print("Mean Queue Length: " + str(sum(packet_length_array) / len(packet_length_array)))
            print("Packet Drop: " + str(packet_drop))
            print()
        plt.plot(lambda_trials,packet_drop_graph)
        plt.ylabel('Packets Dropped')
        plt.xlabel('Lambda Rate Value')
        plt.title('Packets Dropped for Buffer Size ' + str(buffer_size))
        plt.show()

if __name__ == "__main__":
    main()
