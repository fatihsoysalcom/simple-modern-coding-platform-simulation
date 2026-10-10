import os
import time
import threading

# Simulating a Modern Coding Platform (MCP)
# This example demonstrates core concepts like:
# 1. Centralized code repository (simulated by a shared dictionary)
# 2. Collaborative editing (simulated by multiple threads accessing the repo)
# 3. Automated builds/deployments (simulated by a background thread)

class CodeRepository:
    def __init__(self):
        self.code = {"main.py": "print('Hello, MCP!')"}
        self.lock = threading.Lock()

    def get_code(self, filename):
        with self.lock:
            return self.code.get(filename, "File not found.")

    def update_code(self, filename, new_content):
        with self.lock:
            self.code[filename] = new_content
            print(f"[Repo] Updated '{filename}'.")
            return True

    def list_files(self):
        with self.lock:
            return list(self.code.keys())

class Developer:
    def __init__(self, name, repo):
        self.name = name
        self.repo = repo

    def edit_file(self, filename, new_content):
        print(f"[{self.name}] Editing '{filename}'...")
        time.sleep(0.5) # Simulate editing time
        if self.repo.update_code(filename, new_content):
            print(f"[{self.name}] Successfully updated '{filename}'.")
        else:
            print(f"[{self.name}] Failed to update '{filename}'.")

class CI_CD_Pipeline:
    def __init__(self, repo):
        self.repo = repo
        self._stop_event = threading.Event()

    def run(self):
        print("[CI/CD] Pipeline started.")
        while not self._stop_event.is_set():
            time.sleep(5) # Check for changes every 5 seconds
            files = self.repo.list_files()
            # In a real MCP, this would trigger a build/test/deploy
            print(f"[CI/CD] Checking for updates in: {files}")
            # Simulate a successful build if main.py exists
            if "main.py" in files:
                print("[CI/CD] Build successful for main.py.")

    def stop(self):
        self._stop_event.set()

if __name__ == "__main__":
    # Initialize the core components of our MCP simulation
    repository = CodeRepository()
    ci_cd = CI_CD_Pipeline(repository)

    # Start the CI/CD pipeline in a separate thread
    ci_cd_thread = threading.Thread(target=ci_cd.run)
    ci_cd_thread.daemon = True # Allow program to exit even if thread is running
    ci_cd_thread.start()

    # Simulate developers working on the code
    dev1 = Developer("Alice", repository)
    dev2 = Developer("Bob", repository)

    print("\n--- Initial State ---")
    print(f"main.py content: {repository.get_code('main.py')}")

    print("\n--- Developer Actions ---")
    # Alice updates the main file
    dev1.edit_file("main.py", "print('Hello from MCP!')")
    time.sleep(2) # Give CI/CD a moment to react

    # Bob adds a new file
    dev2.edit_file("utils.py", "def helper(): pass")
    time.sleep(2)

    # Alice modifies main.py again
    dev1.edit_file("main.py", "print('MCP is evolving!')")
    time.sleep(2)

    print("\n--- Final State ---")
    print(f"main.py content: {repository.get_code('main.py')}")
    print(f"utils.py content: {repository.get_code('utils.py')}")

    print("\nSimulation finished. CI/CD pipeline will stop when program exits.")
    # In a real scenario, you'd have a way to gracefully stop the CI/CD pipeline.
    # For this example, daemon threads will exit with the main thread.
