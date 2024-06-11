#!/usr/bin/env python3

import os
import subprocess
import signal
import sys

# if python version lower than 3.11, use tomli instead of tomllib
if sys.version_info[0] == 3 and sys.version_info[1] < 11:
    import tomli as tomllib
else:
    import tomllib

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
HOOP_CONFIG_DIR = os.path.expanduser("~/.hoop")


def check_hoop():
    print("Checking hoop installation...", end=" ")
    try:
        subprocess.run(
            ["hoop", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except FileNotFoundError:
        print("hoop is not installed. Please install hoop before running this script.")
        sys.exit(1)
    print("✅")


def check_auth():
    print("Checking hoop authentication...", end=" ")
    try:
        with open(f"{HOOP_CONFIG_DIR}/config.toml", "rb") as f:
            config = tomllib.load(f)
            token = config["token"]
            if not token:
                raise FileNotFoundError
        print("✅")
    except FileNotFoundError:
        p = subprocess.Popen(
            ["hoop", "login"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        p.wait()
        if p.returncode != 0:
            print("Login failed. Please try again.")
            sys.exit(1)


def read_connections_file() -> dict:
    print("Reading connections.toml...", end=" ")
    try:
        with open(f"{SCRIPT_DIR}/connections.toml", "rb") as f:
            data = tomllib.load(f)
            connections = data["connections"]
            if not connections:
                raise FileNotFoundError
        print("✅")
        return connections
    except FileNotFoundError:
        print(
            "connections.toml file not found. Please create one before running this script."
        )
        sys.exit(1)


def make_cleanup_fn(processes):
    def cleanup(signum=None, frame=None):
        print("\nCleaning up...", end=" ")
        for p in processes:
            p.terminate()
        print("✅")
        print("Exiting...")
        sys.exit()

    return cleanup


def register_cleanup_fn_on_signal_handlers(cleanup_fn):
    signal.signal(signal.SIGTERM, cleanup_fn)
    signal.signal(signal.SIGINT, cleanup_fn)
    signal.signal(signal.SIGQUIT, cleanup_fn)
    signal.signal(signal.SIGTSTP, cleanup_fn)
    signal.signal(signal.SIGABRT, cleanup_fn)
    signal.signal(signal.SIGSEGV, cleanup_fn)


def connect_to_all(connections):
    print("Connecting...")
    for connection, port in connections.items():
        p = subprocess.Popen(["hoop", "connect", connection, "-p", str(port)])
        processes.append(p)


def wait_for_eof():
    while True:
        try:
            input()
        except EOFError:
            break


if __name__ == "__main__":
    check_hoop()
    check_auth()
    connections = read_connections_file()
    processes = []
    cleanup_fn = make_cleanup_fn(processes)
    register_cleanup_fn_on_signal_handlers(cleanup_fn)
    connect_to_all(connections)
    wait_for_eof()
    cleanup_fn()
