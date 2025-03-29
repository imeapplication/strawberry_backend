#!/usr/bin/env python
"""
Custom script to run Strawberry server with Django initialized.
"""
import os
import sys
import django

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Now that Django is initialized, run the Strawberry server
from strawberry.cli.commands.server import server as strawberry_server
import typer

app = typer.Typer()
app.command()(strawberry_server)

if __name__ == "__main__":
    app()
    
    