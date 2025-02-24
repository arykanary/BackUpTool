"""

Refs:
    https://pypi.org/project/GitPython/
    https://docs.python.org/3/library/cmd.html
    https://docs.python.org/3/library/shutil.html
"""
import os
from cmd import Cmd
from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError, NoSuchPathError
from json import dump, load
from warnings import warn
from shutil import copytree, rmtree
from pathlib import Path


class BackUpTool(Cmd):
    def __init__(self):
        super().__init__()
        self.settings_path = os.path.join(Path.home(), '.backup', 'settings.json')

        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r') as sf:
                settings = load(sf)
                self.source_backup_directory = settings['source_backup_directory']
                self.primary_backup_directory = settings['primary_backup_directory']
                self.secondary_backup_directory = settings['secondary_backup_directory']

        else:
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            self.source_backup_directory = None
            self.primary_backup_directory = None
            self.secondary_backup_directory = None

    # 
    def do_quit(self, _):
        """Goodbye!"""
        print('Saving settings, goodbye!')
        with open(self.settings_path, 'w') as sf:
            sets = {
                'source_backup_directory':     self.source_backup_directory,
                'primary_backup_directory':    self.primary_backup_directory,
                'secondary_backup_directory':  self.secondary_backup_directory,
            }
            dump(sets, sf)
        return True

    def emptyline(self):
        pass
    # 
    def do_info(self, _):
        print(
            f'source_backup_directory:    {self.source_backup_directory}',
            f'primary_backup_directory:   {self.primary_backup_directory}',
            # f'secondary_backup_directory: {self.secondary_backup_directory}',
            sep='\n',
        )

    def do_source_backup_directory(self, arg):
        """Set source_backup_directory"""
        self.source_backup_directory = arg

    def do_primary_backup_directory(self, arg):
        """Set primary backup directory"""
        self.primary_backup_directory = arg

    def do_init(self, _):
        # Init remote
        if os.path.exists(self.primary_backup_directory):
            print('Directory already exists, not attempting to create backup repository.')
        else:
            Repo.init(
                self.primary_backup_directory,
                mkdir=True,
                bare=True,
            )

        # Init local
        try:
            self.repo = Repo(self.source_backup_directory)
        except InvalidGitRepositoryError:
            try:
                Repo.clone_from(self.primary_backup_directory,
                                self.source_backup_directory)
            except GitCommandError as e:
                if e.status == 128:
                    tmp = os.path.join(self.source_backup_directory, '__tmp')
                    while os.path.exists(tmp):
                        tmp += '_'

                    Repo.clone_from(self.primary_backup_directory, tmp)
                    copytree(os.path.join(tmp, '.git'),
                             os.path.join(self.source_backup_directory, '.git'))
                    rmtree(tmp, ignore_errors=True)
                else:
                    print(e)

            self.repo = Repo(self.source_backup_directory)
        except NoSuchPathError:
            warn(f'source_backup_directory ({self.source_backup_directory}) does not exist.')

    def do_status(self, _):
        """Get status"""
        if hasattr(self, 'repo') and os.path.exists(self.primary_backup_directory):
            self.repo.git.fetch(all=True)
            print(self.repo.git.status())
        else:
            print('Backup repository not available or not existing.')

    def do_backup(self, _):
        """Do backup"""
        print('Adding files...')
        self.repo.git.add('.', force=True)
        print('Committing files...')
        self.repo.git.commit(m='Some')
        print('Pushing files...')
        self.repo.git.push()

    def do_restore(self, _):
        """Restore backup (specific or latest)"""
        self.repo = Repo.clone_from(
            self.primary_backup_directory,
            self.source_backup_directory
        )

    def do_delete(self, arg):
        """Delete backup (before date, specific, between interval)"""
        print('NotImplemented')

    # This wishlist stuff
    def do_set_secondary_backup(self, arg):
        """Set secondary backup paths"""
        print('NotImplemented')

    def do_delete_secondary(self, arg):
        """Delete secondary backup paths"""
        print('NotImplemented')

    def do_set_auto_interval(self, arg):
        """Set auto interval (0 is off, spawn deamon process?)"""
        print('NotImplemented')

    def do_installs_dependencies(self, arg):
        """Install/update requirements (git, ...)"""
        print('NotImplemented')

    def do_auto_start(self, arg):
        """Start at computer startup"""
        print('NotImplemented')


if __name__ == "__main__":
    but = BackUpTool()
    but.cmdloop(
        f"{80*'=':^80}\n"
        f"{'Welcome to this ultra simple GIT based backup tool.':^80}\n"
        f"{'It helps with a few things that otherwise would take a bit more time.':^80}\n"
        f"{'And saves some stuff (in your home directory) for you.':^80}\n"
        f"{80*'=':^80}"
        
    )
