from pip._vendor.resolvelib.providers import AbstractProvider

from pip._internal.utils.typing import MYPY_CHECK_RUNNING

from .requirements import make_requirement

if MYPY_CHECK_RUNNING:
    from typing import Any, Optional, Sequence, Tuple, Union

    from pip._internal.index.package_finder import PackageFinder
    from pip._internal.operations.prepare import RequirementPreparer
    from pip._internal.req.req_install import InstallRequirement
    from pip._internal.resolution.base import InstallRequirementProvider

    from .base import Requirement, Candidate


class PipProvider(AbstractProvider):
    def __init__(
        self,
        finder,    # type: PackageFinder
        preparer,  # type: RequirementPreparer
        make_install_req  # type: InstallRequirementProvider
    ):
        # type: (...) -> None
        self._finder = finder
        self._preparer = preparer
        self._make_install_req = make_install_req

    def make_requirement(self, ireq):
        # type: (InstallRequirement) -> Requirement
        return make_requirement(
            ireq,
            self._finder,
            self._preparer,
            self._make_install_req
        )

    def get_install_requirement(self, c):
        # type: (Candidate) -> InstallRequirement
        return getattr(c, "_ireq", None)

    def identify(self, dependency):
        # type: (Union[Requirement, Candidate]) -> str
        return dependency.name

    def get_preference(
        self,
        resolution,  # type: Optional[Candidate]
        candidates,  # type: Sequence[Candidate]
        information  # type: Sequence[Tuple[Requirement, Candidate]]
    ):
        # type: (...) -> Any
        # Use the "usual" value for now
        return len(candidates)

    def find_matches(self, requirement):
        # type: (Requirement) -> Sequence[Candidate]
        return requirement.find_matches()

    def is_satisfied_by(self, requirement, candidate):
        # type: (Requirement, Candidate) -> bool
        return requirement.is_satisfied_by(candidate)

    def get_dependencies(self, candidate):
        # type: (Candidate) -> Sequence[Requirement]
        return [
            make_requirement(
                r,
                self._finder,
                self._preparer,
                self._make_install_req
            )
            for r in candidate.get_dependencies()
        ]
