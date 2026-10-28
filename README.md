# Schere, Stein, Papier mit TCP und UDP

Ein Konsolenprojekt fuer die Netzwerkaufgabe. Python 3.9 oder neuer, nur
Standardbibliothek: keine Installation mit pip erforderlich.

## In dein Repository uebernehmen

ZIP entpacken und den INHALT des Ordners schere-stein-papier in deinen bereits
geklonten Repository-Ordner kopieren. Vorhandene eigene Dateien vorher vergleichen.
Diesen Repository-Ordner in VS Code oeffnen. Alle Befehle dort ausfuehren.
Je nach Installation python durch python3 (macOS/Linux) oder py (Windows) ersetzen.

## Starten: vier Terminals in VS Code

Terminal > Neues Terminal; mit dem Plus weitere Terminals anlegen.
Die ersten drei Prozesse bleiben waehrend aller Tests aktiv.

1. Terminal: `python nameserver.py`
2. Terminal, sobald der Namensserver bereit ist: `python tcp_server.py`
3. Terminal, sobald der Namensserver bereit ist: `python udp_server.py`
4. Terminal: `python tcp_client.py`

Im Spiel schere, stein oder papier eingeben. q beendet den Client.
Danach im vierten Terminal: `python udp_client.py`.
Alle Server zum Schluss jeweils mit Strg+C beenden.

Einzelne Runde:

```bash
python tcp_client.py stein
python udp_client.py papier
python test_unknown.py
```

Der letzte Befehl soll den fehlenden Dienst melden und mit 'Test erfolgreich'
enden. Er erfindet keinen Ersatzdienst und stuerzt nicht ab.

## Vergleichsmessungen (ohne Wireshark moeglich)

```bash
python tcp_client.py stein --repeat 100 --csv docs/tcp_results.csv
python udp_client.py stein --repeat 100 --csv docs/udp_results.csv
```

Die CSV-Zieldateien werden ueberschrieben. Jede Runde erzeugt eine neue Verbindung
beziehungsweise einen neuen UDP-Socket und fragt zuvor erneut den Namensserver.
- request_ms: direkt vor dem Senden der Spielanfrage bis zur kompletten Antwort;
  ohne Namenssuche und TCP-Verbindungsaufbau.
- total_ms: Namenssuche, Verbindungsaufbau und Anfrage/Antwort zusammen.

Vergleiche jeweils dieselbe Spalte, gleiche Rundenzahl und gleiche Bedingungen.
Die Ausgabe nennt den Mittelwert von request_ms. Ein lokaler Test allein beweist
nicht, dass ein Protokoll allgemein schneller ist. UDP hat keine Zustellgarantie;
es gibt einen Timeout von 3 Sekunden und keine automatische Wiederholung.
Es werden keine realen Messergebnisse mitgeliefert: eigene Messungen erstellen.

## Dateien und Aufbau

| Datei | Aufgabe |
|---|---|
| config.py | Feste Serveradressen, Dienstnamen, Timeout |
| protocol.py | Textnachrichten, TCP-Empfang bis Zeilenende, Registrierung/Suche |
| game.py | Zufaellige Serverwahl und Spielregeln |
| nameserver.py | Adressbuch mit Lock und einem Thread pro TCP-Verbindung |
| tcp_server.py | TCP-Spielserver mit einem Thread pro Verbindung |
| udp_server.py | UDP-Spielserver mit acht Worker-Threads |
| client.py | Gemeinsame Bedienung, Dienstsuche, Zeitmessung, CSV-Export |
| tcp_client.py / udp_client.py | Startpunkte der Clients |
| test_unknown.py | Pflichtfall: unbekannter Dienst |
| test_game.py | Automatischer Test aller neun Kombinationen |
| docs/screenshots/ | Platz fuer eigene Screenshots |

127.0.0.1 bedeutet: alle Programme laufen auf demselben Computer.
Namensserver: TCP 5000, Spieldienst TCP 5001, Spieldienst UDP 5002.
Falls ein Port belegt ist, die betreffende Konstante in config.py aendern.
Clients verwenden fuer die Spielverbindung ausschliesslich die Adresse aus der
Namensserverantwort, nicht TCP_ADDRESS oder UDP_ADDRESS.

Der Server bindet zuerst seinen Port und registriert sich dann. Der Namensserver
speichert sein Adressbuch nur im Arbeitsspeicher. Nach einem Neustart des
Namensservers auch beide Spielserver neu starten. Gestoppte Spielserver werden
nicht automatisch ausgetragen; die Clients behandeln Verbindungsfehler/Timeouts.
Dieses einfache lokale Lehrprojekt hat keine Authentifizierung oder Verschluesselung.

## Protokoll

UTF-8-Text mit abschliessendem Zeilenumbruch. TCP wird bis zu diesem Zeilenumbruch
eingelesen; ein einzelnes recv muss nicht die gesamte Nachricht liefern.
Eine Anfrage pro TCP-Verbindung beziehungsweise UDP-Datagramm.
Registrierung und Suche laufen fuer BEIDE Spielvarianten ueber TCP.

```text
REGISTER rps_tcp 127.0.0.1 5001
OK

REGISTER rps_udp 127.0.0.1 5002
OK

LOOKUP rps_tcp
OK 127.0.0.1 5001

LOOKUP nicht_registrierter_dienst
ERROR service_not_found

PLAY stein
OK stein schere gewonnen
```

Spielantwort: OK Spielerwahl Serverwahl Ergebnis. Ergebnisse: gewonnen,
verloren, unentschieden. Fehler beginnen mit ERROR. Registrierung mit bestehendem
Namen aktualisiert den Eintrag; ungueltige IPs, Ports oder Namen werden abgelehnt.

## Tests

`python -m unittest test_game -v` benoetigt keine laufenden Server.
Danach mit laufenden Servern beide Clients und test_unknown.py ausfuehren.
Mehrere Client-Terminals gleichzeitig starten, um parallele Anfragen zu zeigen.

## Wireshark spaeter

Auf demselben Computer das Loopback-Interface verwenden. Die Aufzeichnung schon
vor dem Start der Spielserver beginnen, damit ihre Registrierung sichtbar ist.
Anschliessend beide Clients und den unbekannten Dienst testen.
Anzeigefilter: `tcp.port == 5000 || tcp.port == 5001 || udp.port == 5002`
Screenshots zu Registrierung, Dienstsuche, TCP-Spiel und UDP-Spiel erstellen.
Bei TCP Verbindungsaufbau und Daten vergleichen; UDP besitzt keinen Handshake.
Zu jedem Bild Ports, Ablauf und beobachtete Unterschiede erklaeren.

## Noch fuer die Abgabe erledigen

- Namen aller Gruppenmitglieder angeben (maximal drei).
- Eigene Messungen, App-Screenshots und Wireshark-Aufnahmen erstellen.
- Bericht nach der Kursvorlage verfassen: Beschreibung, Startanleitung,
  Loesungsweg, Codeerklaerung, Screenshots, TCP/UDP-Vergleich und Fazit.
- Eigenleistung/KI-Unterstuetzung ehrlich in eigenen Worten erklaeren.
  Dieser Ausgangscode wurde mit KI erstellt. Jedes Gruppenmitglied sollte
  den verwendeten Code verstehen und erklaeren koennen.
- Repository-Link und Bericht abgeben; bei privatem Repository Lehrenden
  und Tutoren Zugriff geben.

Das Paket enthaelt die Anwendung, aber keinen fertigen Abgabebericht.
