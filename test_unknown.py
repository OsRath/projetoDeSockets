"""Separater Client fuer den Pflichtfall 'unbekannter Dienst'."""
from config import NAME_SERVER
from protocol import tcp_request


def main():
    try:
        response = tcp_request(NAME_SERVER, "LOOKUP nicht_registrierter_dienst")
        if response == "ERROR service_not_found":
            print("Erwarteter Fehler: Der angefragte Dienst ist nicht registriert.")
            print("Test erfolgreich: Client hat den Fehler korrekt behandelt.")
            return 0
        print(f"Unerwartete Antwort: {response}")
    except (OSError, ValueError) as error:
        print(f"Namensserver nicht erreichbar oder ungueltige Antwort: {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())