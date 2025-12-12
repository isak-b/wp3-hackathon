import multiprocessing
import time
import atexit
import os

# Set the start method for multiprocessing
# This needs to be done at the top level, before any processes are created.
# 'fork' is generally fine for Linux.
if os.name != 'nt':
    multiprocessing.set_start_method("fork", force=True)


# The user will run this script with `uv run python run_servers.py` from the `group1` directory.
# This means 'agents' package is available to be imported.
from agents.employee_catalog.employee_catalog_mcp.__main__ import main as mcp_employee_main
from agents.service_catalog.service_catalog_mcp.__main__ import main as mcp_service_main
from agents.employee_catalog.__main__ import main as agent_employee_main
from agents.service_catalog.__main__ import main as agent_service_main

processes = []

def cleanup():
    print("Shutting down servers...")
    for p in processes:
        if p.is_alive():
            p.terminate()
            p.join(timeout=5) # wait for 5 seconds
            if p.is_alive():
                p.kill() # force kill if not terminated
                p.join() # wait for kill
    print("Servers shut down.")

atexit.register(cleanup)

def run_server(main_func, name, host, port):
    """Target function to run a server's main() in a process."""
    print(f"Starting server '{name}' on http://{host}:{port}")
    try:
        # The 'main' object is a click.Command. The actual function is 'main.callback'.
        main_func.callback(host, port)
    except Exception as e:
        print(f"Server '{name}' failed: {e}")

def main():
    server_configs = [
        {"name": "employee_mcp", "main": mcp_employee_main, "host": "localhost", "port": 8001},
        {"name": "service_mcp", "main": mcp_service_main, "host": "localhost", "port": 8002},
        {"name": "employee_agent", "main": agent_employee_main, "host": "localhost", "port": 8011},
        {"name": "service_agent", "main": agent_service_main, "host": "localhost", "port": 8012},
    ]

    # Start MCP servers first
    print("Starting MCP servers...")
    for config in server_configs[:2]:
        process = multiprocessing.Process(target=run_server, args=(config["main"], config["name"], config["host"], config["port"]))
        processes.append(process)
        process.start()
        time.sleep(3) # Give it a moment to initialize

    # Then start agent servers
    print("\nStarting agent servers...")
    for config in server_configs[2:]:
        process = multiprocessing.Process(target=run_server, args=(config["main"], config["name"], config["host"], config["port"]))
        processes.append(process)
        process.start()
        time.sleep(3) # Give it a moment to initialize

    print("\nAll servers are running in the background.")
    print("Press Ctrl+C to stop all servers.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCtrl+C received.")

if __name__ == "__main__":
    main()