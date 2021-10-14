# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

class Version:
    """Retrieves version/change information.

    .. versionadded:: 36.1.0

    """

    @staticmethod
    @deal.pure
    # @typic.al(strict = True)
    def this() -> str:
        """Retrives the actual version.

        Returns:
            str: Representing the version.

        Examples:
            >>> version = Repo.Version.this()
            >>> major, minor, patch, *rest = version.split(".")
            >>> major.isdecimal()
            True

        .. versionadded:: 36.1.0

        """

        # TODO: This needs to go to a config, or something.

        return (
            pkg_resources
            .get_distribution("pysemver")
            .version
            )

    @staticmethod
    @deal.pure
    # @typic.al(strict = True)
    def last() -> str:
        """Retrives the last tagged version.

        Returns:
            str: Representing the version.

        Examples:
            >>> version = Repo.Version.last()
            >>> major, minor, patch, *rest = version.split(".")
            >>> major.isdecimal()
            True

        .. versionadded:: 36.1.0

        """

        cmd: Sequence[str]
        cmd = ["git", "describe", "--tags", "--abbrev=0", "--first-parent"]
        return Repo.run(cmd).split()[0]
