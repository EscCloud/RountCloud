import requests
import time
import datetime
import sys


def get_url():
    """Prompt user to choose local or cloud and return the target URL."""
    while True:
        ans = input("Is this a local test? [Y/n]: ").strip().lower()
        if ans in ('y', ''):
            url = 'http://localhost:8080/'
            print(f"Using local application at: {url}")
            return url, 'local'
        elif ans == 'n':
            while True:
                url = input("Enter the application URL (e.g., https://appml.run.app/): ").strip()
                if url:
                    if not url.startswith('http://') and not url.startswith('https://'):
                        print("URL must start with http:// or https://")
                        continue
                    if not url.endswith('/'):
                        url += '/'
                    print(f"Using cloud application at: {url}")
                    return url, 'cloud'
        else:
            print("Invalid input. Please enter 'Y', 'N', or press Enter.")


def benchmark_get(url, kind, report_interval_local=50, report_interval_cloud=1):
    """Send repeated GET requests and print average response time."""
    print("\nStarting benchmark. Press Ctrl+C to stop.\n")
    
    i = 0
    total_time = datetime.timedelta(0)
    interval = report_interval_local if kind == 'local' else report_interval_cloud

    try:
        while True:
            i += 1
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"\nRequest failed: {e}")
                continue  # skip this request but continue the loop

            total_time += response.elapsed

            if i % interval == 0:
                avg_time = total_time / interval
                print(f"[{i}] Avg Response Time: {avg_time} | Last Response: {response.text.strip()[:100]}")  # Truncate long output
                total_time = datetime.timedelta(0)

    except KeyboardInterrupt:
        print("\nBenchmark stopped by user.")


def main():
    url, kind = get_url()
    benchmark_get(url, kind)


if __name__ == "__main__":
    main()

