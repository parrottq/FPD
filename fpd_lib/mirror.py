from .download import download
from . import parse
import tarfile
from io import BytesIO



class Mirror:
    """
    A mirror stored in memory
    """
    arch = "x86_64"
    default_repos = ["core", "extra", "community"] # TODO: better default repos

    def __init__(self, url):
        self.url = url
        self.repos = {}

        self._populate()


    def search(self, package, repo=""):
        """
        Searches for a package in the mirror list

        Keyword arguments:
        package -- package name to search for
        repo -- package repositiory to look in
        """
        search_repos = []
        if repo:
            if repo in self.repos:
                # Add one repos to search
                search_repos.append(repo)
            else:
                # Could not be found
                return None
        else:
            # Add all present repos to search
            search_repos += list(self.repos.keys())

        # Searches each repo
        for term in search_repos:
            if not term in self.repos:
                continue

            # Goes thru all the packages
            for current_package, metadata in self.repos[term].items():
                if package == current_package:
                    return metadata

        # No package was found
        return None


    def _populate(self):
        """
        Fills all the repos with packages
        """

        for repo in self.default_repos:
            # Download package database from a repo
            db = download(f"{self.url}{repo}/os/{self.arch}/{repo}.db.tar.gz")

            # Extract database
            try:
                tar = tarfile.open(mode="r:gz", fileobj=BytesIO(db))

                # Parse the db file structure
                self.repos[repo] = parse.extract_db(tar)
            except tarfile.TarError: pass


class Mirrors:
    """
    A collection of methods related to mirror manipulation
    """

    mirrors = []


    @staticmethod
    def search(package):
        """
        Search for a package in the mirror list

        Note:
        Returns a generator that keeps adding and supplying mirrors

        Keyword arguments:
        package -- a package object
        """
        pass


    @staticmethod
    def find():
        """
        Finds the next highest rated mirror
        """
        pass


    @staticmethod
    def add(url):
        """
        Downloads and decompresses a mirror

        Keyword arguements:
        url -- base mirror url
        """


        Mirrors.mirrors.add(Mirror(url))

