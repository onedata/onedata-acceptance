"""Utilities for parsing shortened, indexed paths displayed in the GUI."""

import re
from dataclasses import dataclass
from itertools import pairwise
from typing import Self

_INDEXED_PATH_PART_PATTERN = re.compile(r"(?P<prefix>.+)_(?P<idx>\d+)")


@dataclass(frozen=True)
class PathSequenceIndices:
    first_idx: int | None
    last_idx: int


@dataclass(frozen=True)
class IndexedPathSequence:
    indices: PathSequenceIndices | None
    prefix: str | None
    file_name: str

    @classmethod
    def from_yaml_dict(cls, config: dict[str, str]) -> Self:
        return cls(
            indices=PathSequenceIndices(
                first_idx=int(config["First directory index"]),
                last_idx=int(config["Last directory index"]),
            ),
            prefix=config["Directory prefix"],
            file_name=config["File name"],
        )

    def matches(self, other: Self) -> bool:
        """Compare paths, treating absent indices as wildcards."""
        if self.file_name != other.file_name:
            return False

        if self.indices is None or other.indices is None:
            return True

        if self.prefix != other.prefix:
            return False

        if self.indices.first_idx is None or other.indices.first_idx is None:
            return self.indices.last_idx == other.indices.last_idx

        return self.indices == other.indices


def _parse_indexed_path_parts(
    path_parts: list[str],
    sequence: str,
) -> tuple[str, PathSequenceIndices] | None:
    if not path_parts:
        return None

    matches = [_INDEXED_PATH_PART_PATTERN.fullmatch(part) for part in path_parts]

    if any(match is None for match in matches):
        raise ValueError(f"Invalid indexed path sequence: {sequence}")

    valid_matches = [match for match in matches if match is not None]

    prefix = valid_matches[0].group("prefix")
    indices = [int(match.group("idx")) for match in valid_matches]

    if any(match.group("prefix") != prefix for match in valid_matches[1:]):
        raise ValueError(f"Invalid indexed path sequence: {sequence}")

    if any(next_idx != idx + 1 for idx, next_idx in pairwise(indices)):
        raise ValueError(f"Invalid indexed path sequence: {sequence}")

    return prefix, PathSequenceIndices(
        first_idx=indices[0],
        last_idx=indices[-1],
    )


def parse_indexed_path_sequence(sequence: str) -> IndexedPathSequence:
    *path_parts, file_name = sequence.split("/")

    if path_parts.count("...") > 1:
        raise ValueError(f"Invalid indexed path sequence: {sequence}")

    if "..." not in path_parts:
        parsed = _parse_indexed_path_parts(path_parts, sequence)

        if parsed is None:
            return IndexedPathSequence(
                indices=None,
                prefix=None,
                file_name=file_name,
            )

        prefix, indices = parsed
        return IndexedPathSequence(
            indices=indices,
            prefix=prefix,
            file_name=file_name,
        )

    ellipsis_idx = path_parts.index("...")
    left = _parse_indexed_path_parts(
        path_parts[:ellipsis_idx],
        sequence,
    )
    right = _parse_indexed_path_parts(
        path_parts[ellipsis_idx + 1 :],
        sequence,
    )

    if right is None:
        # The path expands from the right first and then alternates sides,
        # so a non-empty left group can never have an empty right group.
        raise ValueError(f"Invalid indexed path sequence: {sequence}")

    right_prefix, right_indices = right

    if left is None:
        return IndexedPathSequence(
            indices=PathSequenceIndices(
                first_idx=None,
                last_idx=right_indices.last_idx,
            ),
            prefix=right_prefix,
            file_name=file_name,
        )

    left_prefix, left_indices = left

    if left_prefix != right_prefix:
        raise ValueError(f"Invalid indexed path sequence: {sequence}")

    return IndexedPathSequence(
        indices=PathSequenceIndices(
            first_idx=left_indices.first_idx,
            last_idx=right_indices.last_idx,
        ),
        prefix=left_prefix,
        file_name=file_name,
    )
