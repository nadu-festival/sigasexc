"""Signal handlers."""

import signal
from contextlib import contextmanager
from types import FrameType
from typing import Callable, Optional, Union

from sigasexc.signal_interrupt import SignalInterrupt

CALLABLE_SIGNAL_HANDLER_TYPE = Callable[[int, Optional[FrameType]], None]
"""Type of callable handler."""

HANDLER_TYPE = Union[signal.Handlers, CALLABLE_SIGNAL_HANDLER_TYPE]
"""Type of handler."""


class SignalHandler:
    """
    Signal handler.

    Example
    -------
    Import signal and sigasexc libs.

    >>> import signal
    >>> from sigasexc import SignalInterrupt, SignalHandler

    And write codes.

    >>> # use default handler (raise SignalInterrupt)
    >>> handler = SignalHandler()
    >>> try:
    >>>     with handler.listen(signal.SIGUSR1, signal.SIGUSR2):
    >>>         # Break when got signal.
    >>>         while True:
    >>>             pass
    >>>     # After the with block, the handler for the signal is
    >>>     # returned to the before the with block.
    >>> except SignalInterrupt.SIGUSR1:
    >>>     print("SIGUSR1 except.")
    >>> except SignalInterrupt.SIGUSR2:
    >>>     print("SIGUSR1 except.")
    >>> else:
    >>>     print("No signal except.")
    """

    def __init__(self, handler: Optional[HANDLER_TYPE] = None) -> None:
        """
        Initialize SignalHandler.

        Parameters
        ----------
        handler: func(int, frame) or member of signal.Handlers, optional.
            When handler is None, handler set to raise SignalInterrupt.
            handler can be a callable Python object taking two arguments,
            or one of the special values signal.SIG_IGN or signal.SIG_DFL.
        """
        if handler is None:
            handler = self.default_handler
        self.handler = handler

    def default_handler(
                self,
                signum: int,
                sigframe: Optional[FrameType]
            ) -> None:
        """
        Raise subclass of SignalInterrupt has signum.

        Parameters
        ----------
        signum : int
            The signal number.
        sigframe : types.FrameType, optional
            The current stack frame (None or a frame object).

        Raises
        ------
        Subclass of SignalInterrupt
        """
        sigexc = SignalInterrupt.subclass(signum)
        raise sigexc(sigframe)  # type: ignore

    @contextmanager  # type: ignore
    def listen(  # type: ignore
                self,
                *sigset: Union[signal.Signals, int]
            ) -> "SignalHandler":
        """
        Set handler to signal in sigset.

        This function set handler and yeild self.
        After that, reset the handler.

        Parameters
        ----------
        *sigset : signal.Signals or int
            The signals which handler set.
        """
        old_handler = {}
        try:
            for sig in sigset:
                old_handler[sig] = signal.signal(sig, self.handler)
            yield self
        finally:
            for sig in sigset:
                signal.signal(sig, old_handler[sig])
