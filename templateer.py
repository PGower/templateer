import jinja2
import click
import os
import yaml

@click.command()
@click.option('--config', '-c', help="Location of the config file. Defaults to ./config.yml")
@click.option('--skip-empty|--no-skip-empty', help="When set any template that produces an all whitepace result will not be output to the destination.")
@click.option('--data-source', help="Reserved for future expansion. Currently has one possible value, environ.")
def generate():
	load config from --config or ./config.yml
	if no config print an error message and fail.

	for each entry in the config file render the template entry to the output entry using os.environ as the context.
	if skip empty is true then any template file that results in an empty file (all whitespace) is logged and then skipped.


if __name__ == '__main__':
	tool()