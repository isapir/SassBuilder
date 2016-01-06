import sublime, sublime_plugin

import codecs
import json
import os
import re

from functools import partial
from threading import Thread
from subprocess import PIPE, Popen


SASS_EXTENSIONS = ('.scss', '.sass')


def which(executable):
    for path in os.environ['PATH'].split(os.pathsep):
        path = path.strip('"')

        fpath = os.path.join(path, executable)

        if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
            return fpath

    if os.name == 'nt' and not executable.endswith('.exe'):
        return which('{}.exe'.format(executable))

    return None


def path_info(path):
    root = os.path.dirname(path)
    name = os.path.splitext(os.path.basename(path))[0]
    extn = os.path.splitext(path)[1]

    return {'root': root, 'name': name, 'extn': extn, 'path': path}


def find_files(pattern, path):
    pattern = re.compile(pattern)
    found = []
    path = os.path.realpath(path)

    for root, dirnames, files in os.walk(path):
        for fname in files:
            if fname.endswith(SASS_EXTENSIONS):
                with codecs.open(os.path.join(root, fname), 'r', "utf-8") as f:
                    if any(pattern.search(line) for line in f):
                        found.append(os.path.join(root, fname))
                        break
    
    return found


def grep_files(pattern, path):
    path = os.path.realpath(path)
    grep = '''grep -E "{}" * -lr'''.format(pattern)

    proc = Popen(grep, shell=True, cwd=path, stdout=PIPE, stderr=PIPE)

    out, err = proc.communicate()

    if err:
        print(err)
        sublime.error_message('SassBuilder: Hit \'ctrl+`\' to see errors.')

    if not out:
        return None

    out = out.decode('utf8')
    found = []
    for f in out.split():
        if f.endswith(SASS_EXTENSIONS):
            found.append(os.path.join(path, f))

    return found


def get_partial_files(info, project_path):
    pattern = '''@import.*{}'''.format(info['name'][1:])

    if which('grep'):
        return grep_files(pattern, project_path)

    return find_files(pattern, project_path)


def get_files(info, project_path):
    if info['name'].startswith('_'):
        return get_partial_files(info, project_path)
    return [info['path']]


def load_settings(project_path):
    try:
        with open(os.sep.join([project_path, '.sassbuilder-config.json']), 'r') as f:
            data = f.read()
        return json.loads(data)
    except:
        return None


def compile_sass(files, settings):
    compiled_files = []
    for f in files:
        info = path_info(f)

        srcp = os.path.join(info['root'], settings['output_path'])
        name = '.'.join([info['name'], 'css'])

        path = os.path.join(srcp, name)

        sass = 'sass --update \'{0}\':\'{1}\' --stop-on-error --trace {2} ' \
               '--style {3}'

        rules = []

        if not settings['options']['cache']:
            rules.append('--no-cache')

        if settings['options']['debug']:
            rules.append('--debug-info')

        if settings['options']['line-comments']:
            rules.append('--line-comments')

        if settings['options']['line-numbers']:
            rules.append('--line-numbers')

        rules = ' '.join(rules)

        sass = sass.format(info['path'], path, rules,
                           settings['options']['style'])

        sass = Popen(sass, shell=True, cwd=info['root'], stdout=PIPE, stderr=PIPE)

        out, err = sass.communicate()
        if out:
            compiled_files.append(name)

        if err:
            print(err)
            sublime.error_message('SassBuilder: Hit \'ctrl+`\' to see errors.')
            return

    print('{0} has been compiled.'.format(', '.join(compiled_files)))


class SassBuilderCommand(sublime_plugin.EventListener):

    def on_post_save(self, view):
        info = path_info(view.file_name())
        settings = load_settings(info['root'])

        if not settings:
            return None

        if info['extn'] in SASS_EXTENSIONS:
            print('SassBuilder started.')
            files = get_files(info, settings['project_path'])

            #t = Thread(target=compile_sass, args=(files, settings))
            #t.start()
            compile_sass(files, settings)
