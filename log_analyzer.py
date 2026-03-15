file_path = "./server_logs.txt"
error_count = {}

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()  # Split the line by whitespace

            # Ensure the line is not empty and check if the last token is '500'
            if parts and parts[-1] == "500":
                ip_error = parts[0]

                # .get() returns the current count for the IP, defaulting to 0 if not yet seen
                error_count[ip_error] = error_count.get(ip_error, 0) + 1

    print(error_count)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
