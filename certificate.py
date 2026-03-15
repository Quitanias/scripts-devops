import ssl
import socket
import datetime

def check_ssl_expiry(hostname, port=443):
    """Checks the SSL certificate expiration date for a given domain."""
    context = ssl.create_default_context()

    try:
        # Connect to the server and extract the certificate
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

                # Parse the expiration date from the certificate format into a datetime object
                expire_date_str = cert['notAfter']
                expire_date = datetime.datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z')

                # Calculate the difference between the expiration date and today
                days_remaining = (expire_date - datetime.datetime.utcnow()).days
                return days_remaining, expire_date.strftime("%Y-%m-%d")

    except Exception as e:
        return None, str(e)

if __name__ == '__main__':
    # List of domains to monitor
    domains_to_monitor = ['google.com', 'github.com', 'youtube.com']

    print("=== SSL Monitoring Report ===")
    for domain in domains_to_monitor:
        days, details = check_ssl_expiry(domain)

        if days is not None:
            # Set status based on days remaining (alert if less than 30 days)
            status = "🔴 CRITICAL" if days < 30 else "🟢 OK"
            print(f"{status} | {domain}: Expires in {days} days (Date: {details})")
        else:
            print(f"🟡 ERROR | {domain}: Verification failed ({details})")