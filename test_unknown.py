"""Separate client for the required 'unknown service' test case."""
from config import NAME_SERVER
from protocol import tcp_request


def main():
    try:
        response = tcp_request(NAME_SERVER, "LOOKUP unregistered_service")
        if response == "ERROR service_not_found":
            print("Expected error: The requested service is not registered.")
            print("Test passed: The client handled the error correctly.")
            return 0
        print(f"Unexpected response: {response}")
    except (OSError, ValueError) as error:
        print(f"Name server unreachable or invalid response: {error}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())