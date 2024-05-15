import requests
import json
import concurrent.futures


def update(email):
    url = "https://api.karismagarudamulia.com/api/v1/update-data/complete"
    # url = "http://127.0.0.1:8000/api/v1/update-data/complete"

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

    # Use ThreadPoolExecutor to send requests concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(update, email): email for email in emails}
        for future in concurrent.futures.as_completed(futures):
            email = futures[future]
            try:
                data = future.result()
                print(f"{email}: {json.dumps(data, indent=2)}")
            except Exception as exc:
                print(f"{email} generated an exception: {exc}")


if __name__ == "__main__":
    main()
