# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Version bumber.

.. versionadded:: 1.0.0

"""

from nptyping import NDArray as Array
from typing import Sequence, Tuple, Type

import re

import deal
import numpy
import typic

from mantic.infra import repo

from ..domain import VersionInt

weights: Array[int]
weights = numpy.array([10, 10e5, 10e10], int)


@typic.klass(always = True, slots = True, strict = True)
class BumpVersion:
    """Determines the required version bump.

    Attributes:
        this: The actual version.
        that: The last tagged version.
        what: An ``event`` and the associated bump requirement.
        required: The required version bump.

    Examples:
        >>> bumper = BumpVersion()

        >>> bumper.required
        <VersionInt.NONE: 0>

        >>> bumper.what(3)
        <VersionInt.MAJOR: 3>

        >>> bumper(3)
        >>> bumper.required
        <VersionInt.MAJOR: 3>

    .. versionchanged:: 1.2.0
        Added default values for ``this``, ``that``, ``what``, and
        ``required``.

    .. versionadded:: 1.0.0

    """

    this: str = repo.versions.this()
    that: str = repo.versions.last()
    what: Type[VersionInt] = VersionInt
    required: VersionInt = VersionInt.NONE

    @deal.pure
    def __call__(self, bump: int) -> None:
        """Bumps the required version."""

        index = max(self.required.value, VersionInt(bump).value)
        self.required = VersionInt(index)

    @deal.pure
    def is_acceptable(self) -> bool:
        """Determines if the current version is acceptable or not.

        Returns:
            bool:
            True when it is acceptable.
            False otherwise.

        Examples:
            >>> bumper = BumpVersion()
            >>> bumper.is_acceptable()
            True

            >>> bumper(3)
            >>> bumper.this = "1.2.3"
            >>> bumper.that = "1.2.3"
            >>> bumper.is_acceptable()
            False

            >>> bumper.this = "2.0.0"
            >>> bumper.is_acceptable()
            True

            >>> bumper.this = "2.0.0-rc.1+1234"
            >>> bumper.is_acceptable()
            True

            >>> bumper.that = "2.0.0-asdf+1234"
            >>> bumper.is_acceptable()
            True

        .. versionchanged:: 1.2.0
            Added weights to calculate de minimum acceptable version bump.
            For example, if a patch is required, a minor or a major bump are
            also acceptable.

        .. versionadded:: 1.0.0

        """

        actual_is_rel: bool
        actual_version: Array[int]
        required_fragment: int
        required_is_rel: bool
        required_version: Array[int]

        # If there's no required bump, we just do not check.
        if self.required == VersionInt.NONE:
            return True

        # We get the actual number and whether it is a release or not.
        actual_version, actual_is_rel = self._extract(self.this)

        # We get the last tagged number and whether it is a release or not.
        required_version, required_is_rel = self._extract(self.that)

        # If both are releases, next version has to be major/minor/patch +1.
        if actual_is_rel and required_is_rel:
            for index in range(0, self.required):
                if index == self.required - 1:
                    required_version[index] += 1
                else:
                    required_version[index] = 0

        # We add weights to each version fragment before comparing them.
        actual_version *= weights
        required_version *= weights

        # Otherwise we just do not check.
        # It is way too anecdotic for the complexity that the check requires.
        return sum(actual_version - required_version) >= 0

    @deal.pure
    def _extract(self, version: str) -> Tuple[Array[int], bool]:
        """Extract a major/minor/patch number from a version string."""

        is_release: bool
        parsed_version: Array[int]
        release: str
        rest: Sequence[str]

        # We separate the non-release par, ex: ``-pre+1``.
        release, *rest = re.split("\\+|\\-", version)

        # We reverse and cast the version to int.
        parsed_version = numpy.array(release.split(".")[::-1], int)

        # Finally we determine if this is a release or not.
        is_release = len(rest) == 0

        return parsed_version, is_release
