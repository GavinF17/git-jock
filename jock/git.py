
import subprocess
import sys

import click

from jock.config import get_repository_path


def git_common(command, config_repositories, selected_repositories, git_args=()):
    for repository_name in selected_repositories:
        repository_path = get_repository_path(config_repositories[repository_name]['location'])
        click.echo('Executing [{}] in [{}]'.format(command, repository_path))
        subprocess.run(('git', '-C', repository_path, command) + git_args)


def git_clone(config_repositories, selected_repositories, git_args=()):
    for repository_name in selected_repositories:
        config_repository = config_repositories[repository_name]
        repository_path = get_repository_path(config_repository['location'])
        click.echo(
            'Cloning [{}] in [{}]'.format(repository_name, repository_path)
        )
        subprocess.run(('git', 'clone', config_repository['address'], repository_path) + git_args)


GIT_COMMANDS = {
    'clone': lambda _, cr, sr, a: git_clone(cr, sr, a),
    'add': git_common,
    'restore': git_common,
    'rm': git_common,
    'branch': git_common,
    'commit': git_common,
    'reset': git_common,
    'switch': git_common,
    'tag': git_common,
    'fetch': git_common,
    'pull': git_common,
    'push': git_common,
    'checkout': git_common,
}


def git_command(command, config_repositories, selected_repositories, git_args):
    release_func = GIT_COMMANDS.get(command)

    if release_func is None:
        print('Unsupported command ' + command)
        sys.exit(1)

    release_func(command, config_repositories, selected_repositories, git_args)
