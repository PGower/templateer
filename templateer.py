import jinja2
import click
import os
import yaml

@click.command()
@click.option('--config', '-c', type=click.File(mode='r'), default='./config.yml', help="Location of the config file. Defaults to ./config.yml")
@click.option('--skip-empty/--no-skip-empty', help="When set any template that produces an all whitepace result will not be output to the destination.")
# @click.option('--data-source', default='env', type=click.Choice(['env']), help="Reserved for future expansion. Currently has one possible value, environ.")
def generate(config, skip_empty):
	try:
		config = yaml.load(config)
	except (yaml.scanner.ScannerError, IOError) as e:
		click.secho('An error occured and we were unable to load the config file at {}'.format(config.name), fg='red')
		click.secho('The error message was: {}'.format(str(e)), fg='red')
	if not config.has_key('templates'):
		click.secho('The config file does not have a templates key. This is required.', fg='red')
		raise click.Abort('Invalid config file.')
	else:
		for template_id, template_config in config['templates'].items():
			click.secho('Processing template with ID: {}'.format(template_id), fg='yellow')
			template = jinja2.Template(open(template_config['src']).read())
			content = template.render(os.environ)
			if skip_empty and not content.strip():
				click.secho('Not writing template with ID: {} as the output is empty.', fg='red')
				continue
			with open(template_config['dest'], 'w+') as f:
				f.write(content)
				click.secho('Writing content for template ID: {} to {}'.format(template_id, template_config['dest']))
			uid = template_config.get('uid', -1)
			gid = template_config.get('gid', -1)
			try:
				os.chown(template_config['dest'], uid, gid)
				if uid != -1:
					click.secho('Setting file uid to: {}'.format(uid))
				if gid != -1:
					click.secho('Setting file gid to: {}'.format(gid))
			except OSError as e:
				click.secho('Unable to chown file. Error is: {}'.format(str(e)), fg='red')
			except TypeError as e:
				click.secho('Invalid value for uid or gid given. Error is: {}'.format(str(e)))
			if template_config.has_key('mode'):
				try:
					os.chmod(template_config['dest'], template_config['mode'])
					click.secho('Setting file mode to {}'.format(template_config['mode']))
				except OSError as e:
					click.secho('Unable to chmod file. Error is: {}'.format(str(e)), fg='red')
				except TypeError as e:
					click.secho('{} is not a valid value for chmod. Error is: {}'.format(template_config['mode'], str(e)))

if __name__ == '__main__':
	generate()