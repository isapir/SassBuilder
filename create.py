import os

import sublime, sublime_plugin

class SassBuilderCreateCommand(sublime_plugin.WindowCommand):

	def run(self, paths=[]):

		skeleton = """{
	"output": "/path/to/compiled/css",
	"options": [
		{
			"cache"         : true
		},{
			"style"         : "nested"
		},{
			"debug"         : true
		},{
			"line-numbers"  : true
		},{
			"line-comments" : true
		}
	]
}"""

		if len(paths) != 0:
			for path in paths:
				if os.path.isdir(path):
					filename = os.path.join(path, ".sassbuilder-config")
					f = open(filename, "w+")
					f.write(skeleton)
					f.close()
					view = self.window.open_file(filename)
		else:
			view = self.window.new_file()
			view.settings().set("default_dir", self.window.folders()[0])
			view.set_syntax_file("Packages/Javascript/JSON.tmLanguage")
			view.set_name(".sassbuilder-config")

			skeleton = skeleton.replace("/path/to/compiled/css",
				"${0:/path/to/compiled/css}")

			view.run_command("insert_snippet", {"contents": skeleton})