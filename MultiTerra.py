#!/usr/bin/env python3

import asyncio
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
        if verbose:
            pprint.pprint(self._dirs)

    def _find_dirs(self, dir: str = '.', base_dir: str = '', verbose: bool = True):
        for root, subdirs, files in os.walk(dir):
            if not root == dir:
                if not self._is_excluded(root):
                    for filename in files:
                        if self._is_included(filename):
                            x = root.replace(base_dir, '')
                            self._dirs.append(x)
        self._dirs.sort()

    def _is_included(self, dir: str):
        for regexp in self._config['include']:
            if re.match(regexp, dir):
                return True
        return False

    def _is_excluded(self, dir: str):
        for regexp in self._config['exclude']:
            if re.search(regexp, dir):
                return True
        return False

    def plan(self, dir: str = '.', base_dir: str = '', verbose: bool = True):
        asyncio.run(self._concurrent_run(dir, base_dir, verbose))

    async def _concurrent_run(self, dir: str = '.', base_dir: str = '', verbose: bool = True):
        self._find_dirs(dir, base_dir, verbose)

        dissected = self._dissect(self._dirs, 12)

        await asyncio.gather(
            self._run(dissected[0], verbose),
            self._run(dissected[1], verbose),
            self._run(dissected[2], verbose),
            self._run(dissected[3], verbose),
            self._run(dissected[4], verbose),
            self._run(dissected[5], verbose),
            self._run(dissected[6], verbose),
            self._run(dissected[7], verbose),
            self._run(dissected[8], verbose),
            self._run(dissected[9], verbose),
            self._run(dissected[10], verbose),
            self._run(dissected[11], verbose)
        )

    def _dissect(self, a, number):
        result = []

        for i in range(0, number):
            result.append([])

        for index, value in enumerate(a):
            a_index = index % number
            result[a_index].append(a[index])

        return result

    async def _run(self, dirs, verbose: bool = True):
        for dir in dirs:
            await self._run_command(self._config['command'], dir, verbose)

    async def _run_command(self, command, dir, verbose: bool = True):
        if verbose:
            print(f"ST: {dir}")

        proc = await asyncio.create_subprocess_shell(
            command,
            cwd=dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        is_synchronized = self._verify_output(stdout.decode())
        if is_synchronized > 0 or proc.returncode > 0:
            print('ER: ' + dir)
        else:
            if verbose:
                print('OK: ' + dir)

    def _verify_output(self, output: str):
        result = 1

        for message in self._config['synchronized']:
            if re.search(message, output):
                result = 0

        for message in self._config['not_synchronized']:
            if re.search(message, output):
                result = 2

        return result
