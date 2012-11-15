import json
import os
import subprocess
import sys
from threading import Thread

if sys.version_info > (2, 7, 0):
	import json
	from collections import OrderedDict
else:
	import simplejson as json
	from simplejson import OrderedDict

import sublime, sublime_plugin

def fileInfo(filename):
	path      = os.path.dirname(filename)
	fileinfo  = os.path.splitext(filename)
	filename  = fileinfo[0].split(os.sep)[-1] + fileinfo[1]
	extension = fileinfo[1]
	return {"path": path, "filename": filename, "extension": extension}

def builderSettings(fileinfo):
	try:
		fh = open(fileinfo["path"] + os.sep + ".sassbuilder-config")
		settings = json.loads(fh.read())
		fh.close()
		return settings
	except IOError as e:
		sublime.error_message("Your directory is missing a .sassbuilder-config"
			+ "file. Please create one with Tools->Create SASS Builder.")
		return

def compile(fileinfo, outputpath, options):

	output = os.path.join(outputpath,
		fileinfo['filename'].replace(fileinfo['extension'], ".css"))

	cmd  = "sass --update '{0}':'{1}' --stop-on-error{2} --style {3} --trace"

	sass = ""
	if options[0]["cache"] == False:
		sass += " --no-cache"
	if options[2]['debug'] == True:
		sass += " --debug-info"
	if options[3]['line-numbers'] == True:
		sass += " --line-numbers"
	if options[4]['line-comments'] == True:
		sass += " --line-comments"

	cmd = cmd.format(fileinfo['filename'], output, sass, options[1]['style'])

	proc = subprocess.Popen(cmd, shell=True, cwd=fileinfo['path'],
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	outs, errs = proc.communicate()
	if outs:
		sublime.message_dialog(output + " has been compiled.")
	if errs:
		print errs
		sublime.error_message("There was an error compiling your file.\n" +
			"Please refer to the command console, Ctrl+`.")

class SassBuilderCommand(sublime_plugin.EventListener):

	def on_post_save(self, view):

		fileinfo = fileInfo(view.file_name())
		scope    = "source" + fileinfo['extension']

		if scope == "source.scss" or scope == "source.sass":
			settings   = builderSettings(fileinfo)
			outputpath = os.path.normpath(fileinfo['path'] + settings['output'])
			view.run_command("show_panel", {"panel": "test_panel"})
			t = Thread(target=compile,
				args=(fileinfo, outputpath, settings['options']))
			t.start()