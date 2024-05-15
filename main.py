import requests
import json
import concurrent.futures

dev = True

if dev:
    baseUrl = 'https://api.karismagarudamulia.com/api/v1/'
else:
    baseUrl = 'http://127.0.0.1:8000/api/v1/'


def update(email):
    url = baseUrl + "update-data/complete"

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
    url = baseUrl + "dev/progress"

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


def main():
    # Read emails from the file
    with open('email.txt', 'r') as file:
        emails = [line.strip() for line in file]

    total_emails = len(emails)
    results = []

    # Use ThreadPoolExecutor to send requests concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(update, email): email for email in emails}
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            email = futures[future]
            try:
                data = future.result()
                if data['success']:
                    progress(email)
                print(f"{count}/{total_emails} - {email}")
                results.append({"email": email, "response": data})
            except Exception as exc:
                print(f"{count}/{total_emails} - {email}")
                results.append({"email": email, "error": str(exc)})


if __name__ == "__main__":
    main()
