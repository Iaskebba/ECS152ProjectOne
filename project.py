import heapq, random, math, random
from queue import *
import matplotlib.pyplot as plt

# given lambda = .1 = rate
def Negative_Exponential_Distribution(rate):
    u = random.uniform(0,1)
    return ((-1/rate) * math.log(1-u))


class Event:
    def __init__(self, event_type, time_stamp, host):
        self.event_type = event_type
        self.time_stamp = time_stamp
        self.host = host

    def __lt__(self, other):
        return (self.time_stamp < other.time_stamp)

    def __eq__(self, other):
        return (self.time_stamp == other.time_stamp)

def get_random_host():
    return random.randint(1, current_host_number)    

def get_next_host(event_object):
    if event_object.host == current_host_number:
        return 1
    else:
        return event_object.host + 1


class Packet:
    def __init__(self, arrival_time):
        self.size = random.randint(64,1518)
        self.destination = get_random_host()
        self.arrival_time = arrival_time

def Process_A(event_object):
    global time, MAXBUFFER, host_buffers, GEL, current_lambda, number_of_hosts, current_host_number, total_queuing_delay, total_transmission_delay, total_propagation_delay, packets_transmitted, total_steps
    time = event_object.time_stamp
    next_arrival_event = Event('a',Negative_Exponential_Distribution(current_lambda) + time, event_object.host)
    heapq.heappush(GEL, next_arrival_event) 
    
    host_buffers[event_object.host].put(Packet(time)) 


def Process_Token(event_object):
    global time, MAXBUFFER, host_buffers, GEL, current_lambda, number_of_hosts, current_host_number, total_queuing_delay, total_transmission_delay, total_propagation_delay, packets_transmitted, total_steps, bytes_transmitted
    time = event_object.time_stamp
    # Hosts buffer is empty
    if host_buffers[event_object.host].empty():
        next_token_event = Event('t', time + 0.00001, get_next_host(event_object))
    # Hosts Buffer is not empty
    else:
        frame_size = 0
        packet_list = []
        for x in range(0, host_buffers[event_object.host].qsize()):
            current_packet = host_buffers[event_object.host].get()
            start_host = event_object.host
            end_host = current_packet.destination
            # will go in cycle
            if start_host > end_host:
                steps_to_hit_end = current_host_number - start_host
                total_steps = steps_to_hit_end + end_host
            else:
                total_steps = end_host - start_host
            packet_list.append(total_steps)
            bytes_transmitted += current_packet.size
            packets_transmitted += 1
            total_queuing_delay += time - current_packet.arrival_time
#            total_transmission_delay += current_packet.size / 100.0 * total_steps
            total_propagation_delay += .00001 * total_steps
            frame_size += current_packet.size
        for step in packet_list:
            total_transmission_delay += (frame_size / 100.0) * step
        next_token_time = (.00001 * current_host_number) + ((frame_size / 100.0) * current_host_number) 
        next_token_event = Event('t', time + next_token_time, get_next_host(event_object))

def main():
    # Initialize 
    number_of_trials = 100000
    global time, MAXBUFFER, host_buffers, GEL, current_lambda, used_server_time,number_of_hosts, current_host_number, total_queuing_delay, total_transmission_delay, total_propagation_delay, packets_transmitted, total_steps, bytes_transmitted
    lambda_trials_infinite_buffer = [.01, .05, .1, .2, .3, .5, .6, .7, .8, .9]
    ring_trials = [10, 25]


    for host_number in ring_trials:
        current_host_number = host_number
        throughput_graph = []
        packet_delay = []
        bytes_transmitted = 0
        packets_transmitted = 0
        total_queuing_delay = 0
        total_transmission_delay = 0
        total_propagation_delay = 0
        for trial in lambda_trials_infinite_buffer:
            time = 0 # Current Time
            MAXBUFFER = math.inf # This is a variable to each test case
            host_buffers = {} # buffer Queues for all hosts
            GEL = [] # Global Event List 
            
            current_lambda = trial
            
            # init
            for x in range(1,host_number):
                host_buffers[x] = Queue()
                init_event = Event('a', 0, x)
                heapq.heappush(GEL, init_event)
            init_event = Event('t', 0, 1)
            heapq.heappush(GEL, init_event)

            for i in range(number_of_trials):
                event_object = heapq.heappop(GEL)
                if event_object.event_type == 'a':
                    Process_A(event_object) 
                else:
                    Process_Token(event_object)
            throughput_graph.append(bytes_transmitted / float(time))
            packet_delay.append((total_queuing_delay / float(packets_transmitted)) + (total_transmission_delay / float(packets_transmitted)) + (total_propagation_delay / float(packets_transmitted)))
            print("lambda: " + str(trial))
            print("Throughput: " + str(bytes_transmitted / float(time)))
            print("Average Packet Delay: " + str((total_queuing_delay / float(packets_transmitted)) + (total_transmission_delay / float(packets_transmitted)) + (total_propagation_delay / float(packets_transmitted)))) 
            print()
        print(lambda_trials_infinite_buffer)
        print(len(lambda_trials_infinite_buffer))
        print(throughput_graph)
        print(len(throughput_graph))
        print(packet_delay)
        print(len(packet_delay))
        plt.plot(lambda_trials_infinite_buffer,throughput_graph)
        plt.ylabel('Throughput')
        plt.xlabel('Lambda Rate Value')
        title = 'Server Throughput for Hosts = ' + str(host_number)
        plt.title(title)
        plt.show()
        plt.plot(lambda_trials_infinite_buffer,packet_delay)
        plt.ylabel('Average Packet Delay')
        plt.xlabel('Lambda Rate Value')
        title = 'Average Packet Delay for Hosts = ' + str(host_number)
        plt.title(title)
        plt.show()


if __name__ == "__main__":
    main()
