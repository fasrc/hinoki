"""
command-line interface for hinoki
"""

import click
import os
import hinoki.import_definitions
import hinoki.initialize_cluster
import hinoki.assets
import hinoki.validate

@click.group()
@click.version_option()
def main():
    pass

@main.command('import', help="Imports all definitions via the Sensu API")
def imports():
    hinoki.import_definitions.import_defs()

@main.command('build_assets', help="Packages scripts into tars for use as Sensu assets")
def build_assets():
    hinoki.assets.build_assets()

@main.command('validate', help="Validates JSON and naming for definitions")
def validate():
    hinoki.validate.main()

@main.command('init', help="Configures an empty Sensu install")
def inits():
    hinoki.initialize_cluster.init_cluster()

if __name__ == "__main__":
    main()