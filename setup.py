#!/usr/bin/env python

import os
import shlex
import site
import subprocess
import sys
from distutils.dir_util import copy_tree
from glob import glob

from setuptools import Command, setup
from setuptools.command.easy_install import easy_install as EZInstallCommand
from setuptools.command.install import install as InstallCommand
from setuptools.dist import Distribution


project_dir = os.path.dirname(os.path.realpath(__file__))
name = "resurfemg"
try:
    tag = subprocess.check_output(
        [
            "git",
            "--no-pager",
            "describe",
            "--abbrev=0",
            "--tags",
        ],
        stderr=subprocess.DEVNULL,
    ).strip().decode()
except subprocess.CalledProcessError as e:
    tag = "v0.0.0"

version = tag[1:]

with open(os.path.join(project_dir, "README.md"), "r") as f:
    readme = f.read()


class TestCommand(Command):

    user_options = [
        ("fast", "f", (
            "Don\"t install dependencies, test in the current environment"
        )),
    ]

    def initialize_options(self):
        self.fast = False

    def finalize_options(self):
        self.test_args = []
        self.test_suite = True

    def prepare(self):
        recs = self.distribution.tests_require

        test_dist = Distribution()
        test_dist.install_requires = recs
        ezcmd = EZInstallCommand(test_dist)
        ezcmd.initialize_options()
        ezcmd.args = recs
        ezcmd.always_copy = True
        ezcmd.finalize_options()
        ezcmd.run()
        site.main()

    def run(self):
        if not self.fast:
            self.prepare()
        self.run_tests()


class PyTest(TestCommand):

    user_options = TestCommand.user_options + [
        ("pytest-args=", "a", "Arguments to pass into py.test"),
    ]

    description = "run unit tests"

    def initialize_options(self):
        self.pytest_args = "--color no --tb native"
        super().initialize_options()

    def run_tests(self):
        import pytest

        if self.fast:
            here = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, here)
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


class Pep8(TestCommand):

    description = "validate sources against PEP8"

    def run_tests(self):
        from pycodestyle import StyleGuide

        package_dir = os.path.dirname(os.path.abspath(__file__))
        sources = glob(
            os.path.join(package_dir, "resurfemg", "**/*.py"),
            recursive=True,
        ) + [os.path.join(package_dir, "setup.py")]
        style_guide = StyleGuide(paths=sources)
        options = style_guide.options

        report = style_guide.check_files()
        report.print_statistics()

        if report.total_errors:
            if options.count:
                sys.stderr.write(str(report.total_errors) + "\n")
            sys.exit(1)


class Isort(TestCommand):

    description = "validate imports"

    def run_tests(self):
        from isort.main import main as imain

        package_dir = os.path.dirname(os.path.abspath(__file__))
        sources = glob(
            os.path.join(package_dir, "resurfemg", "**/*.py"),
            recursive=True,
        ) + [os.path.join(package_dir, "setup.py")]

        if imain(["-c", "--lai", "2", "-m" "3"] + sources):
            sys.exit(1)


class SphinxApiDoc(Command):

    description = "run apidoc to generate documentation"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from sphinx.ext.apidoc import main

        src = os.path.join(project_dir, "docs")
        special = (
            "index.rst",
        )

        for f in glob(os.path.join(src, "*.rst")):
            for end in special:
                if f.endswith(end):
                    os.utime(f, None)
                    break
            else:
                os.unlink(f)

        sys.exit(main([
            "-o", src,
            "-f",
            os.path.join(project_dir, "resurfemg"),
            "--separate",
        ]))


class InstallDev(InstallCommand):

    def run(self):
        self.distribution.install_requires.extend(
            self.distribution.extras_require["dev"],
        )
        super().do_egg_install()


if __name__ == "__main__":
    setup(
        name=name,
        version=version,
        author='An Awesome Team from the Netherlands eScience Center!',
        author_email='c.moore@esciencecenter.nl',
        packages=['ReSurfEMG', 'ReSurfEMG.test'],
        url='https://github.com/ReSurfEMG/ReSurfEMG',
        license='LICENSE.md',
        description='A package that helps with analysis of respiratory EMG data',
        long_description=open('README.md').read(),
        package_data={"": ("README.md",)},
        cmdclass={
            "test": PyTest,
            "lint": Pep8,
            "isort": Isort,
            "apidoc": SphinxApiDoc,
            "install_dev": InstallDev,
        },
        tests_require=["pytest", "pycodestyle", "isort", "wheel"],
        command_options={
            "build_sphinx": {
                "project": ("setup.py", name),
                "version": ("setup.py", version),
                "source_dir": ("setup.py", "./docs"),
                "config_dir": ("setup.py", "./docs"),
            },
        },
        setup_requires=["sphinx", "wheel"],
        install_requires=["lark"],
        extras_require={
            "dev": ["pytest", "codestyle", "isort", "wheel"],
        },
        zip_safe=False,
    )
