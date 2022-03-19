"""The exceptions of signal interrupt."""

import signal
from types import FrameType
from typing import Any, Dict, Optional, Type, Union


class SignalInterrupt(Exception):
    """Exception of signal interrupt."""

    __subclasses: Dict[int, Type["SignalInterrupt"]] = {}

    def __init__(
                self,
                signum: int,
                sigframe: Optional[FrameType],
                *args: Any
            ) -> None:
        """
        Initialize SignalInterrupt.

        Parameters
        ----------
        signum : int
            Signal number.
        sigframe : types.FrameType, optional.
            The current stack frame (None or a frame object).
        """
        super().__init__(
                f"Signal interrupt (signum={signum}).",
                signum,
                sigframe,
                *args
            )

    @classmethod
    def subclass(
                cls,
                sig: Union[signal.Signals, int],
                alias: Optional[str] = None
            ) -> Type["SignalInterrupt"]:
        """
        Get subclass of SignalInterrupt.

        Parameters
        ----------
        sig : signal.Signals or int
            Signal number or signal.Signals member.
        alies : str, optional, default None.
            The name of alies.
            You can access like SignalInterrupt.XXX if alies is "XXX".
            If alies is None, alies sets to sig.name when
            sig is member of signal.Signals,
            alies sets to f"SIG{sig:02d}" when sig is integer.
        """
        if isinstance(sig, signal.Signals):
            alias = (sig.name if alias is None else alias)
            signum = sig.value
        else:
            signum = sig

        if signum <= 0 or signal.NSIG <= signum:
            raise OSError(22, 'Invalid argument')

        if signum not in cls.__subclasses:

            def _sub_init_func(
                        self: "SignalInterrupt",
                        sigframe: Optional[FrameType],
                        *args: Any
                    ) -> None:
                """Initialize subclass of SignalInterrupt."""
                super().__init__(signum, sigframe, *args)

            if not alias:
                alias = f"SIG{signum:02d}"

            subcls_name = f"{cls.__name__}.{alias}"
            _sub_cls = type(subcls_name, (cls,), {"__init__": _sub_init_func})
            cls.__subclasses[signum] = _sub_cls
            setattr(cls, alias, cls.__subclasses[signum])

        return cls.__subclasses[signum]


# Create default SignalInterrupt subclasses in signal.Signals.
for sig in signal.Signals:
    SignalInterrupt.subclass(sig)
