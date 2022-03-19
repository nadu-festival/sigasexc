import signal
import unittest

from sigasexc import SignalInterrupt


class TestSignalInterrupt(unittest.TestCase):

    def test_sub_classes(self):
        for signum in range(1, signal.NSIG):
            self.assertTrue(
                    issubclass(
                            SignalInterrupt.subclass(signum),
                            SignalInterrupt
                        )
                )

    def test_invalid_argument(self):
        with self.assertRaises(OSError):
            SignalInterrupt.subclass(0)

        with self.assertRaises(OSError):
            SignalInterrupt.subclass(signal.NSIG)

    def test_sub_classes_has_alias(self):
        for sig in signal.Signals:
            alies = sig.name
            self.assertTrue(
                    issubclass(
                            getattr(SignalInterrupt, alies),
                            SignalInterrupt
                        )
                )

if __name__ == '__main__':
    unittest.main()
