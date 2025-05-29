from __future__ import annotations

from typing_extensions import final

class AocdError(Exception):
    """base exception for this package"""


@final
class PuzzleLockedError(AocdError):
    """trying to access input before the unlock"""


@final
class PuzzleUnsolvedError(AocdError):
    """answer is unknown because user has not solved puzzle yet"""


@final
class DeadTokenError(AocdError):
    """the auth is expired/incorrect"""


@final
class UnknownUserError(AocdError):
    """the token for this userid was not found in the cache"""


@final
class ExampleParserError(AocdError):
    """for problems specific to the example extraction code"""
