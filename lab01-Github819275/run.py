#!/usr/bin/env python3
"""University Course Management System entry point.

**Important**: It's an example of how to run the application. You can remove it if you want.
"""
import os

from src import DependencyContainer
from src.cli import CLI

DATA_DIR = 'data'

def main() -> None:
    """Main entry point for the University Course Management System."""
    # Initialize data directory
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Create dependency container to manage storage instances and services
    container = DependencyContainer(DATA_DIR)
    
    # Start the CLI
    cli = CLI(container)
    cli.start()

if __name__ == "__main__":
    main()