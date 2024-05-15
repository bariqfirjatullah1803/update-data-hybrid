import requests
import json
import concurrent.futures
import time

dev = True

if dev:
    baseUrl = 'https://api.karismagarudamulia.com/api/v1/'
else:
    baseUrl = 'http://127.0.0.1:8000/api/v1/'


def check(email):
    url = baseUrl + "dev/check-report-pmo"
    payload = json.dumps({"email": email})
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    try:
        response_json = response.json()
        return response_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def check_status(email):
    url = baseUrl + "dev/check-status"

    payload = json.dumps({
        "email": email
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        response_json = response.json()
        return response_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def main():
    # Prompt the user for the filename
    filename = 'email.txt'

    try:
        # Read emails from the file
        with open(filename, 'r') as file:
            emails = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return

    total_emails = len(emails)
    results = []

    # Use ThreadPoolExecutor to send requests concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_status, email): email for email in emails}
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            start_time = time.time()
            email = futures[future]
            try:
                data = future.result()
                progress_data = data['data']['progress']
                if progress_data == 100:
                    emails.remove(email)
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"{count}/{total_emails} - {email}: {progress_data} {execution_time:.2f} seconds")
            except requests.RequestException as e:
                print(f"{count}/{total_emails} - {email} 'error': RequestException: {e}")
            except json.JSONDecodeError as e:
                print(f"{count}/{total_emails} - {email} 'error': Invalid JSON response: {e}")
            except Exception as e:
                print(f"{count}/{total_emails} - {email} 'error': {str(e)}")
            with open(filename, 'w') as file:
                for email in emails:
                    file.write(f"{email}\n")


if __name__ == "__main__":
    main()
