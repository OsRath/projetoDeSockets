# Rock Paper Scissors with TCP and UDP

A command-line game using Python sockets. Run all programs on the same computer.

## Requirements

- Python 3.13.7 or newer.
- No additional packages are needed.

Open the project folder in VS Code. Run all commands from this folder. If `python3` does not work, try `python` or `py`.

## Start the application

Open four terminals using **Terminal → New Terminal**.

Start the servers in this order and keep them running:

**Terminal 1 — Name server**

```bash
python3 nameserver.py
```

**Terminal 2 — TCP game server**

```bash
python3 tcp_server.py
```

**Terminal 3 — UDP game server**

```bash
python3 udp_server.py
```

Wait for each server to confirm that it is ready.

**Terminal 4 — Play using TCP**

```bash
python3 tcp_client.py
```

Enter `rock`, `paper`, or `scissors`. The client displays the result and response time. Enter `q` to quit.

Then try UDP:

```bash
python3 udp_client.py
```

To stop the application, quit the client and press **Ctrl+C** in each server terminal.

If you restart the name server, restart both game servers too.

## Run a single round

With all three servers running:

```bash
python3 tcp_client.py rock
python3 udp_client.py paper
```

## Test an unknown service

With the name server running:

```bash
python3 test_unknown.py
```

The client should report that the service is not registered and display `Test passed`.

## Run the game tests

No servers are needed for this command:

```bash
python3 -m unittest test_game -v
```

## Measure response times

Keep all three servers running. Make sure a folder named `docs` exists in the project folder.

Run 100 rounds for each protocol:

```bash
python3 tcp_client.py rock --repeat 100 --csv docs/tcp_results.csv
python3 udp_client.py rock --repeat 100 --csv docs/udp_results.csv
```

The client displays the average request time and saves the measurements to CSV. Existing files with the same names are overwritten.

- `request_ms`: time from sending the game request to receiving the response.
- `total_ms`: also includes the service lookup and connection setup.