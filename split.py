import os


def split_email_file(input_file, chunk_size=1000):
    with open(input_file, 'r') as file:
        emails = [line.strip() for line in file]

    total_chunks = (len(emails) + chunk_size - 1) // chunk_size

    for i in range(total_chunks):
        chunk_emails = emails[i * chunk_size:(i + 1) * chunk_size]
        with open(f'part_{i + 1}.txt', 'w') as chunk_file:
            for email in chunk_emails:
                chunk_file.write(f"{email}\n")


if __name__ == "__main__":
    split_email_file('email.txt')
# Run the split function
