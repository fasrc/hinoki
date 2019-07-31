"""
command-line interface for hinoki
"""

import click
import os
import hinoki.import_definitions
import hinoki.assets
import hinoki.validate

@click.group()
@click.version_option()
def main():
    pass

@main.command()
def imports():
    hinoki.import_definitions.import_defs()

@main.command()
def build_assets():
    hinoki.assets.build_assets()

@main.command()
def validate():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(ROOT_DIR)
    hinoki.validate.main()

@main.command()
def inits():
    hinoki.initialize_cluster.init()

if __name__ == "__main__":
    main()