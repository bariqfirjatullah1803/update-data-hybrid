import requests
import json
import concurrent.futures
import time


def check(email):
    url = "https://api.karismagarudamulia.com/api/v1/dev/check-report-pmo"
    payload = json.dumps({"email": email})
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    try:
        response_json = response.json()
        return response_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def generate(email):
    print('GENERATE TASK')
    url = "https://api.karismagarudamulia.com/api/v1/dev/task/pdf"
    payload = json.dumps({"email": email})
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    try:
        response_json = response.json()
        return response_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def main():
    with open('email.txt', 'r') as file:
        emails = [line.strip() for line in file]

    total_emails = len(emails)
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(check, email): email for email in emails}
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            start_time = time.time()
            email = futures[future]
            try:
                data = future.result()
                if data.get('success', False):
                    generate(email)
                results.append({"email": email, "response": data})
            except Exception as exc:
                results.append({"email": email, "error": str(exc)})

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"{count}/{total_emails} - {email}: {execution_time:.2f} seconds")


if __name__ == "__main__":
    main()
