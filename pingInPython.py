from scapy.all import *
import time
import argparse

def ping(destination, count=4, ttl=64, packet_size=64, timeout=2):
    try:
        # Validate the inputs
        if count < 1:
            raise ValueError("Count must be greater than 0.")
        if ttl < 1 or ttl > 255:
            raise ValueError("TTL must be between 1 and 255.")
        if packet_size < 28:  # Minimum packet size to accommodate headers
            raise ValueError("Packet size must be at least 28 bytes.")
        
        rtt_list = []
        packet_loss = 0

        for i in range(count):
            pkt = IP(dst=destination, ttl=ttl)/ICMP()/("X" * (packet_size - 28))
            start_time = time.time()
            reply = sr1(pkt, timeout=timeout, verbose=False)
            end_time = time.time()
            
            if reply:
                rtt = (end_time - start_time) * 1000  # RTT in milliseconds
                rtt_list.append(rtt)
                print(f"Reply from {reply.src}: time={rtt:.2f} ms TTL={reply.ttl}")
            else:
                print("Request timed out.")
                packet_loss += 1

        # Calculate statistics
        if rtt_list:
            min_rtt = min(rtt_list)
            max_rtt = max(rtt_list)
            avg_rtt = sum(rtt_list) / len(rtt_list)
        else:
            min_rtt = max_rtt = avg_rtt = 0

        packet_loss_percent = (packet_loss / count) * 100

        print("\nPing statistics:")
        print(f"    Packets: Sent = {count}, Received = {count - packet_loss}, Lost = {packet_loss} ({packet_loss_percent:.2f}% loss)")
        print(f"Approximate round trip times in milli-seconds:")
        print(f"    Minimum = {min_rtt:.2f} ms, Maximum = {max_rtt:.2f} ms, Average = {avg_rtt:.2f} ms")
    
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# The code below is for accepting the 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ping utility using Scapy")
    parser.add_argument("destination", help="Destination IP address")
    parser.add_argument("--count", type=int, default=4, help="Number of ping requests to send")
    parser.add_argument("--ttl", type=int, default=64, help="Time-To-Live value for the packets")
    parser.add_argument("--packet_size", type=int, default=64, help="Size of the packets in bytes")
    parser.add_argument("--timeout", type=int, default=2, help="Timeout for each ping request in seconds")
    
    args = parser.parse_args()
    
    ping(args.destination, count=args.count, ttl=args.ttl, packet_size=args.packet_size, timeout=args.timeout)