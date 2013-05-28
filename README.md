Sass Builder
============

Sass Builder is a SASS compiler that reads a config file (.sassbuilder-config) stored
in a sass/scss source folder. It is a JSON file that sets .css output folder and SASS
flags [cache, style, debug, line numbers, line comments].

The plugin works on post save of a .sass/.scss file in Sublime Text.

* Automatically runs on save.
* Create .sassbuilder-config files with ease
  * Tools->Sass Builder Config
  * Ctrl+B + Ctrl+S keystroke
  * Right-click a folder or folders in the side bar.

The .sassbuilder-config file
============================
```json
{
	"output_path": "/path/to/compiled/css",
	"options": {
		"cache":         true,
		"debug":         true,
		"line-comments": true,
		"line-numbers":  true,
		"style":         "nested"
	}
}
```
