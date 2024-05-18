import requests
import json
import concurrent.futures
import time


def check(invoice):
    url = "https://api.karismagarudamulia.com/api/v1/dev/invoice"

    payload = json.dumps({
        "invoice_code": invoice
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
        # Read invoices from the file
        with open(filename, 'r') as file:
            invoices = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return

    total_invoices = len(invoices)
    results = []
    r1 = open('result.txt', 'a')
    with open('invoice-result.csv', 'w') as log:
        log.write(
            f'invoice,email,name,voucher,redeem_code,redeem_date,progress,completion_date,student_id,course_id,uk,pre_test,post_test,certificate\n')
    # Use ThreadPoolExecutor to send requests concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        start_time = time.time()
        futures = {executor.submit(check, invoice): invoice for invoice in invoices}
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            invoice = futures[future]
            try:
                data = future.result()
                print(data)
                if data['success']:
                    response_data = data['data']
                    invoice_code = response_data['invoice_code']
                    email = response_data['email']
                    name = response_data['name']
                    voucher = response_data['voucher']
                    redeem_code = response_data['redeem_code']
                    redeem_date = response_data['redeem_date']
                    progress = response_data['progress']
                    completion_date = response_data['completion_date']
                    student_id = response_data['student_id']
                    course_id = response_data['course_id']
                    uk = response_data['uk']
                    pre_test = response_data['pre_test']
                    post_test = response_data['post_test']
                    slug = response_data['slug']
                    certificate = '-'
                    if int(progress) >= 100:
                        certificate = "https://api.karismagarudamulia.com/api/v1/certificate/" + slug + "/" + student_id
                    with open('invoice-result.csv', 'a') as log:
                        log.write(
                            f'{invoice_code},{email},{name},{voucher},{redeem_code},{redeem_date},{progress},{completion_date},{student_id},{course_id},{uk},{pre_test},{post_test},{certificate}\n')
                # if data['success'] and data['code'] == 200:
                #     invoices.remove(invoice)
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"{count}/{total_invoices} - {invoice}: {execution_time:.2f} seconds")
                # print(json.dumps(data, indent=2))
                # r1.write(f"{invoice}: {data['message']}\n")
                # with open(filename, 'w') as file:
                #     for invoice in invoices:
                #         file.write(f"{invoice}\n")
            except requests.RequestException as e:
                print(f"{count}/{total_invoices} - {invoice} 'error': RequestException: {e}")
            except json.JSONDecodeError as e:
                print(f"{count}/{total_invoices} - {invoice} 'error': Invalid JSON response: {e}")
            except Exception as e:
                print(f"{count}/{total_invoices} - {invoice} 'error': ", e)

    r1.close()


if __name__ == "__main__":
    main()
