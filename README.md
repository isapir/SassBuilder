Sass Builder
============

Sass Builder is a SASS compiler that reads a config file (.sassbuilder-config) stored
in a sass/scss source folder. It is a JSON file that sets .css output folder and SASS
flags [cache, style, debug, line numbers, line comments].

The plugin works on post save of a .sass/.scss file in Sublime Text.

UPDATED!
========
This has been resting on the side burner for quite some time and it has finally
received the attention it needed! This has finally been updated to support Sublime
Text 3 and it also works with Python 3.

There was an issue with the `grep` command being called if the system didn't have it
available. This has been corrected to search for `grep` first and run a pure pythonic
method if it's not found in the system's `PATH`.

I have a small method for this [which.py][w] that mimics the Linux command `which`.

The `.sassbuilder-config` has been changed to `.sassbuilder-config.json` to remove
the error Sublime Text 3 generates. `project_path` has be added to this to allow for
scanning in the entire project path when partials are saved.


* Automatically runs on save.
* Create .sassbuilder-config files with ease
  * Tools->Sass Builder Config
  * Ctrl+B + Ctrl+S keystroke
  * Right-click a folder or folders in the side bar.

The .sassbuilder-config file
============================
```json
{
    "project_path": "/project/path",
    "output_path": "/project/path/css",
    "options": {
        "cache":         true,
        "debug":         false,
        "line-comments": true,
        "line-numbers":  true,
        "style":         "nested"
    }
}
```

[w]: https://gist.github.com/bnlucas/a23105c69132ab9e5fe9

Install with Sublime Package Control
============================
1. Add this repo using "Package Control: Add Repository" https://github.com/bnlucas/SassBuilder
2. You can then add this package using Package Control as usual. Find "Package Control: Install Package" and search for "SassBuilder"


Known Issues on Mac
============================
For some users, you may receive this error:
```
b'/bin/sh: sass: command not found\n'
```
This is because:
> 'There is a breakage or removal of environment variable functionality in launchd.conf for users of OS X 10.10 (Yosemite) and above.'

-Source https://support.enthought.com/hc/en-us/articles/204469160-How-do-I-set-PYTHONPATH-and-other-environment-variables-for-Canopy-

You can either follow the instructions to add the path to your executable to your PYTHONPATH as detailed in the link above or follow these steps:

1. Install the "PackageResourceViewer" package to sublime using Package Control, then open this plugin within sublime.
2. Edit SassBuilder.py line 113 changing
```
sass = 'sass --update \'{0}\':\'{1}\' --stop-on-error --trace {2} ' \
               '--style {3}'
```
to
```
sass = '/usr/local/bin/sass --update \'{0}\':\'{1}\' --stop-on-error --trace {2} ' \
               '--style {3}'
```
