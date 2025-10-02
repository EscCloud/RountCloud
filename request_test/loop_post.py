import requests
import json
import time
import datetime


def get_url():
    """Prompt user to select local or cloud and get application URL."""
    while True:
        ans = input("Is this a local test? [Y/n]: ").strip().lower()
        if ans in ('y', ''):
            url = 'http://localhost:8080/'
            print(f"Using local application at: {url}")
            return url, 'local'
        elif ans == 'n':
            while True:
                url = input("Enter application address (e.g., https://appml.run.app/): ").strip()
                if url:
                    if not url.endswith('/'):
                        url += '/'
                    print(f"Using cloud application at: {url}")
                    return url, 'cloud'
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


def load_data(filepath='example.json'):
    """Load JSON data from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("\nLoaded input data successfully.\n")
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        exit(1)


def send_requests(url, data, kind, report_every=50):
    """Send repeated POST requests and print average response time."""
    i = 0
    total_time = datetime.timedelta(0)
    print_interval = 50 if kind == 'local' else 1

    print(f"Sending requests to {url}predict ...\nPress Ctrl+C to stop.\n")

    try:
        while True:
            i += 1
            try:
                response = requests.post(url + 'predict', json=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"\nRequest failed: {e}")
                break

            total_time += response.elapsed

            if i % print_interval == 0:
                avg_time = total_time / print_interval
                try:
                    result = response.json()
                except json.JSONDecodeError:
                    result = response.text
                print(f"[{i}] Avg time: {avg_time} | Last result: {result}")
                total_time = datetime.timedelta(0)

    except KeyboardInterrupt:
        print("\n\nStopped by user.")


def main():
    url, kind = get_url()
    data = load_data('example.json')
    send_requests(url, data, kind)


if __name__ == '__main__':
    main()

