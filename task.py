import requests
import json
import concurrent.futures
import time

dev = True

if dev:
    baseUrl = 'https://api.karismagarudamulia.com/api/v1/dev/'
else:
    baseUrl = 'http://127.0.0.1:8000/api/v1/'


def update(email):
    url = baseUrl + "update"
    payload = json.dumps({"email": email})
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    try:
        response_json = response.json()
        return response_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def complete(email):
    url = baseUrl + "complete"

    payload = json.dumps({"email": email})
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    try:
        response_json = response.json()
        return response_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def task_pdf(email):
    url = baseUrl + "task-pdf"

    payload = json.dumps({
        "email": email
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # Parse the response as JSON
    try:
        response_json = response.json()
        return response_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def score(email):
    url = baseUrl + "score"

    payload = json.dumps({
        "email": email
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # Parse the response as JSON
    try:
        response_json = response.json()
        return response_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def progress(email):
    url = baseUrl + "progress"

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


def check_status(email):
    url = baseUrl + "progress"

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
    filename = input("Please enter the filename: ")

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
        start_time = time.time()
        futures = {executor.submit(score, email): email for email in emails}
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            email = futures[future]
            try:
                print('Update data')
                data = future.result()
                if data.get('success'):
                    task_pdf(email)
                results.append({"email": email, "response": data})
                end_time = time.time()
                execution_time = end_time - start_time
                print(json.dumps(data, indent=2))
                print(f"{count}/{total_emails} - {email}: {execution_time:.2f} seconds")
                emails.remove(email)
                with open(filename, 'w') as file:
                    for email in emails:
                        file.write(f"{email}\n")
            except requests.RequestException as e:
                print(f"{count}/{total_emails} - {email} 'error': RequestException: {e}")
            except json.JSONDecodeError as e:
                print(f"{count}/{total_emails} - {email} 'error': Invalid JSON response: {e}")
            except Exception as e:
                print(f"{count}/{total_emails} - {email} 'error': ", e)


if __name__ == "__main__":
    main()
