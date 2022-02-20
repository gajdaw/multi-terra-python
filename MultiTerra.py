#!/usr/bin/env python3

import os
import pathlib
import pprint
import re
import subprocess
import yaml


class MultiTerra(object):

    def __init__(self):
        self._dirs = []
        file_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(file_path, "multi-terra.yaml")
        with open(filename, "r") as stream:
            self._config = yaml.safe_load(stream)

    def find(self, dir: str = '.', base_dir: str = '', verbose: bool = True):
        self._find_dirs(dir, base_dir, verbose)
        if (verbose):
            pprint.pprint(self._dirs)

    def _find_dirs(self, dir: str = '.', base_dir: str = '', verbose: bool = True):
        for root, subdirs, files in os.walk(dir):
            if ((not root == dir)):
                if (not self._is_excluded(root)):
                    for filename in files:
                        if (self._is_included(filename)):
                            x = root.replace(base_dir, '')
                            self._dirs.append(x)
        self._dirs.sort()

    def run(self, dir: str = '.', base_dir: str = '', verbose: bool = True):
        self._find_dirs(dir, base_dir, verbose)
        self._run(self._dirs, verbose)

    def _run(self, dirs, verbose: bool = True):
        for dir in dirs:
            self.__run_command__(self._config['command'], dir, verbose)

    def _is_included(self, dir: str):
        for regexp in self._config['include']:
            if (re.match(regexp, dir)):
                return True
        return False

    def _is_excluded(self, dir: str):
        for regexp in self._config['exclude']:
            if (re.search(regexp, dir)):
                return True
        return False

    def __run_command__(self, command, dir, verbose: bool = True):
        if (verbose):
            print(f"ST: {dir}")
        process = subprocess.run(command, cwd=dir, capture_output=True, text=True)
        is_synchronized = self._verify_output(process.stdout)
        if (is_synchronized > 0 or process.returncode > 0):
            print('ER: ' + dir)
        else:
            if (verbose):
                print('OK: ' + dir)

    def _verify_output(self, output: str):
        result = 1

        for message in self._config['synchronized']:
            if (re.search(message, output)):
                result = 0

        for message in self._config['not_synchronized']:
            if (re.search(message, output)):
                result = 2

        return result
