import sublime, sublime_plugin

import json
import os

from threading import Thread
from subprocess import PIPE, Popen

def get_path_info(file):
	path      = os.path.dirname(file)
	fileinfo  = os.path.splitext(file)

	filename  = ''.join([fileinfo[0].split(os.sep)[-1], fileinfo[1]])
	extension = fileinfo[1][1:]

	return {
		'path': path,
		'name':	filename,
		'ext':  extension,
	}

def get_output_path(scss_path, css_path):
	return os.path.normpath(''.join([scss_path, os.sep, css_path]))

def builder(path):
	try:
		with open(os.sep.join([path, '.sassbuilder-config']), 'r') as f:
			content = f.read()
		return json.loads(content)
	except:
		return None

def compile(info, output, options):
	output_path = os.path.join(output, info['name'].replace(info['ext'], 'css'))

	cmd = 'sass --update \'{s}\':\'{o}\' --stop-on-error {r} --style {l} --trace'

	rules = []
	if not options['cache']:
		rules.append('--no-cache')
	if options['debug']:
		rules.append('--debug-info')
	if options['line-comments']:
		rules.append('--line-comments')
	if options['line-numbers']:
		rules.append('--line-numbers')
	rules = ' '.join(rules)

	cmd = cmd.format(s=info['name'], o=output_path, r=rules, l=options['style'])

	proc = Popen(cmd, shell=True, cwd=info['path'], stdout=PIPE, stderr=PIPE)
	out, err = proc.communicate()
	if out:
		sublime.message_dialog('{f} has been compiled.'.format(f=output_path))
	if err:
		print err
		sublime.error_message('Sass Error: Hit \'ctrl+`\' to see errors.')

class SassBuilderCommand(sublime_plugin.EventListener):

	def on_post_save(self, view):

		info  = get_path_info(view.file_name())
		scope = '.'.join(['source', info['ext']])

		if scope == 'source.scss' or scope == 'source.sass':
			settings = builder(info['path'])
			if settings:
				output   = get_output_path(info['path'], settings['output_path'])

				t = Thread(target=compile,
					args=(info, output, settings['options']))
				t.start()