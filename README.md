# Hoop Multi Connector

This Python script allows you to connect to multiple Hoop.dev protected databases and services at once.

## Prerequisites

- Python 3 with the `toml` package installed. Python 3.11 has it built-in.
- Hoop CLI installed and authenticated

## Setup

1. Clone this repository.
2. Copy the `connections.example.toml` file to `connections.toml`.
3. Edit `connections.toml` to include your Hoop connections and their corresponding ports.

### Python versions lower than 3.11
```sh
pip install tomli
```

## Usage

Run the script with Python:

```sh
python3 hoop-multi-connector.py
```

Or make it executable:
```sh
chmod +x hoop-multi-connector.py
./hoop-multi-connector.py
```

## What it does?

The script will check your Hoop installation and authentication, read the connections from connections.toml, and connect to all of them. It will wait for an EOF signal (Ctrl+D in most systems) to disconnect from all servers.

## Functions
- `check_hoop()`: Checks if Hoop is installed.
- `check_auth()`: Checks if Hoop is authenticated.
- `read_connections_file()`: Reads the connections from connections.toml.
- `connect_to_all(connections)`: Connects to all servers listed in connections.
- `wait_for_eof()`: Waits for an EOF signal to disconnect from all servers.
- `register_cleanup_fn_on_signal_handlers(cleanup_fn)`: Registers a cleanup function to be called when the script receives a termination signal.

## License
This project is licensed under the MIT License.


