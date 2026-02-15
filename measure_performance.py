import requests
import time
import statistics
import sys
import shutil

# --- CONFIGURATION ---
TARGET_URL = "http://localhost:5000/"
TIMEOUT_LIMIT = 4  # Seconds before we consider the server "Unresponsive"

# --- COLORS FOR TERMINAL ---
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_RED = "\033[41m"

# --- GLOBAL STATS ---
history = []
success_count = 0
fail_count = 0

def get_status_icon(latency, is_error=False):
    if is_error:
        return f"{Colors.BG_RED}{Colors.WHITE} 💀 DOWN {Colors.RESET}"
    if latency > 3.0:
        return f"{Colors.RED}🔥 CRITICAL{Colors.RESET}"
    if latency > 1.0:
        return f"{Colors.YELLOW}⚠️  SLOW   {Colors.RESET}"
    return f"{Colors.GREEN}✅ NORMAL  {Colors.RESET}"

def draw_bar(latency):
    """Draws a visual bar chart for latency"""
    max_bar = 20
    # Cap latency at 4s for the bar visual
    filled = int(min(latency, 4.0) / 4.0 * max_bar)
    bar = "█" * filled + "░" * (max_bar - filled)
    return f"[{bar}]"

print(f"{Colors.CYAN}{Colors.BOLD}--- 🛡️  ADVANCED DDoS MONITORING SYSTEM 🛡️  ---{Colors.RESET}")
print(f"Target: {TARGET_URL}")
print(f"Timeout Limit: {TIMEOUT_LIMIT}s")
print("-" * 60)
print(f"{'TIMESTAMP':<10} | {'STATUS':<12} | {'LATENCY':<10} | {'VISUAL':<22} | {'DETAILS'}")
print("-" * 60)

try:
    while True:
        start_time = time.time()
        error_msg = ""
        is_down = False
        latency = 0.0
        
        try:
            # Try to reach the server
            response = requests.get(TARGET_URL, timeout=TIMEOUT_LIMIT)
            end_time = time.time()
            latency = end_time - start_time
            
            # Record Success
            history.append(latency)
            success_count += 1
            if len(history) > 50: history.pop(0) # Keep last 50
            
            # Status Code Check
            if response.status_code == 503:
                error_msg = "Service Unavailable (503)"
                is_down = True
            elif response.status_code == 429:
                error_msg = "Rate Limited (429)"
            else:
                error_msg = f"Code: {response.status_code}"

        except requests.exceptions.Timeout:
            latency = TIMEOUT_LIMIT
            is_down = True
            fail_count += 1
            error_msg = "⏱️  TIMED OUT (Server Overloaded)"
            
        except requests.exceptions.ConnectionError:
            latency = 0.0
            is_down = True
            fail_count += 1
            error_msg = "🚫 CONNECTION REFUSED (Server Crashed?)"
            
        except Exception as e:
            is_down = True
            fail_count += 1
            error_msg = f"Error: {str(e)[:20]}"

        # --- CALCULATE STATISTICS ---
        avg_lat = statistics.mean(history) if history else 0.0
        success_rate = (success_count / (success_count + fail_count)) * 100 if (success_count + fail_count) > 0 else 0

        # --- PRINT ROW ---
        status_text = get_status_icon(latency, is_down)
        latency_text = f"{latency:.4f}s"
        bar_text = draw_bar(latency)
        
        # Format the output line
        # Uses carriage return logic or just standard print
        current_time = time.strftime("%H:%M:%S")
        
        print(f"{current_time} | {status_text} | {latency_text} | {bar_text} | {error_msg}")
        
        # Optional: Print a "Live Dashboard" summary line at the bottom
        # print(f"   ↳ Success Rate: {success_rate:.1f}% | Avg Latency: {avg_lat:.4f}s", end="\r")

        time.sleep(1) # Wait 1 second before next ping

except KeyboardInterrupt:
    print(f"\n\n{Colors.BOLD}--- 📊 FINAL REPORT ---{Colors.RESET}")
    print(f"Total Requests: {success_count + fail_count}")
    print(f"Successful:     {Colors.GREEN}{success_count}{Colors.RESET}")
    print(f"Failed:         {Colors.RED}{fail_count}{Colors.RESET}")
    print(f"Success Rate:   {success_rate:.2f}%")
    print("-----------------------")
