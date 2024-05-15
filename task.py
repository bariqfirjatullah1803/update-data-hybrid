import requests
import json
import concurrent.futures


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
            email = futures[future]
            try:
                data = future.result()
                print(f"{count}/{total_emails} - {email}: {json.dumps(data, indent=2)}")
                if data.get('success', False):
                    generate_response = generate(email)
                results.append({"email": email, "response": data})
            except Exception as exc:
                print(f"{count}/{total_emails} - {email}: {json.dumps({'error': str(exc)}, indent=2)}")
                results.append({"email": email, "error": str(exc)})


if __name__ == "__main__":
    main()
