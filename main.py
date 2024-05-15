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

    results = []

    # Use ThreadPoolExecutor to send requests concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(update, email): email for email in emails}
        for future in concurrent.futures.as_completed(futures):
            email = futures[future]
            try:
                data = future.result()
                results.append({"email": email, "response": data})
            except Exception as exc:
                results.append({"email": email, "error": str(exc)})

    # Write the results to a text file
    with open('response.txt', 'w') as file:
        for result in results:
            file.write(json.dumps(result, indent=2) + '\n')


if __name__ == "__main__":
    main()
