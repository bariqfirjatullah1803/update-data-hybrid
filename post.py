import requests
import json
import concurrent.futures
import time


def check(email):
    url = "https://api.karismagarudamulia.com/api/v1/dev/update-post"

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
    r1 = open('result.txt', 'a')

    # Use ThreadPoolExecutor to send requests concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        start_time = time.time()
        futures = {executor.submit(check, email): email for email in emails}
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            email = futures[future]
            try:
                data = future.result()
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"{count}/{total_emails} - {email}: {execution_time:.2f} seconds")
                r1.write(f"{email}: {data['message']}\n")
            except requests.RequestException as e:
                print(f"{count}/{total_emails} - {email} 'error': RequestException: {e}")
            except json.JSONDecodeError as e:
                print(f"{count}/{total_emails} - {email} 'error': Invalid JSON response: {e}")
            except Exception as e:
                print(f"{count}/{total_emails} - {email} 'error': ", e)

    r1.close()


if __name__ == "__main__":
    main()
