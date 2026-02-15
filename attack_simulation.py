import threading
import requests
import time

TARGET_URL = "http://localhost:5000/"
NUM_THREADS = 500  # Simulate 50 concurrent users

def attack_worker(thread_id):
    while True:
        try:
            start = time.time()
            response = requests.get(TARGET_URL)
            end = time.time()
            
            # Log successful hits and response time (latency)
            print(f"Thread-{thread_id}: Status {response.status_code} | Latency: {end - start:.4f}s")
        except requests.exceptions.RequestException as e:
            print(f"Thread-{thread_id}: Connection Failed! (Server might be down)")
            # Sleep briefly to avoid freezing your own PC if server dies
            time.sleep(1)

# Launch the threads
print(f"Starting Simulation with {NUM_THREADS} threads targeting {TARGET_URL}...")
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=attack_worker, args=(i,))
    t.daemon = True # Kills threads when main script stops
    t.start()
    threads.append(t)

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSimulation stopped.")
