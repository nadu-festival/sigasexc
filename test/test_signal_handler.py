import os
import signal
import time
import unittest
from threading import Event, Thread

from sigasexc import SignalHandler, SignalInterrupt


class TestSignalHandler(unittest.TestCase):

    def kill_me_after(self, sleep: float, sig: signal.Signals) -> None:
        time.sleep(sleep)
        os.kill(os.getpid(), sig)

    def kill_me_on(self, event: Event, sig: signal.Signals) -> None:
        event.wait()
        os.kill(os.getpid(), sig)

    def test_timer(self):
        handler = SignalHandler()
        sig = signal.SIGINT
        thread = Thread(target=self.kill_me_after, args=(3.0, sig))
        try:
            with self.assertRaises(SignalInterrupt.SIGINT):
                with handler.listen(sig):
                    thread.start()
                    time.sleep(5)
        finally:
            thread.join()

    def test_event(self):
        handler = SignalHandler()
        event = Event()
        sig = signal.SIGINT
        thread = Thread(target=self.kill_me_on, args=(event, sig))
        thread.start()
        time.sleep(5)
        with self.assertRaises(SignalInterrupt.SIGINT):
            with handler.listen(sig):
                event.set()
                time.sleep(5)
        thread.join()

    def test_except_1(self):
        sig_a = signal.SIGTERM
        sig_b = signal.SIGINT
        handler = SignalHandler()
        thread = Thread(target=self.kill_me_after, args=(3.0, sig_a))

        try:
            with handler.listen(sig_a, sig_b):
                thread.start()
                time.sleep(5)
        except SignalInterrupt.SIGTERM:
            pass
        except SignalInterrupt.SIGINT:
            self.failure("Got SIGINT")
        else:
            self.failure("No SignalInterrupt")
        finally:
            thread.join()

    def test_except_2(self):
        sig_a = signal.SIGTERM
        sig_b = signal.SIGINT
        handler = SignalHandler()
        thread = Thread(target=self.kill_me_after, args=(3.0, sig_b))

        try:
            with handler.listen(sig_a, sig_b):
                thread.start()
                time.sleep(5)
        except SignalInterrupt.SIGTERM:
            self.failure("Got SIGTERM")
        except SignalInterrupt.SIGINT:
            pass
        else:
            self.failure("No SignalInterrupt")
        finally:
            thread.join()

    def test_handler_1(self):
        sig = signal.SIGTERM
        handler = SignalHandler(signal.SIG_IGN)
        thread = Thread(target=self.kill_me_after, args=(3.0, sig))

        try:
            with handler.listen(sig):
                thread.start()
                time.sleep(5)
        finally:
            thread.join()

    def test_handler_2(self):
        sig = signal.SIGTERM
        handler_a = SignalHandler(signal.SIG_IGN)
        handler_b = SignalHandler()
        thread = Thread(target=self.kill_me_after, args=(3.0, sig))
        try:
            with self.assertRaises(SignalInterrupt.SIGTERM):
                with handler_a.listen(sig):
                    with handler_b.listen(sig):
                        thread.start()
                        time.sleep(5)
        finally:
            thread.join()

    def test_handler_3(self):
        sig = signal.SIGTERM
        handler_a = SignalHandler(signal.SIG_IGN)
        handler_b = SignalHandler()
        thread = Thread(target=self.kill_me_after, args=(3.0, sig))
        try:
            with handler_a.listen(sig):
                with handler_b.listen(sig):
                    time.sleep(5)
                thread.start()
                time.sleep(5)
        finally:
            thread.join()

    def test_handler_4(self):
        sig = signal.SIGTERM
        handler_a = SignalHandler()
        handler_b = SignalHandler(signal.SIG_IGN)
        thread = Thread(target=self.kill_me_after, args=(3.0, sig))
        try:
            with handler_a.listen(sig):
                with handler_b.listen(sig):
                    thread.start()
                    time.sleep(5)
        finally:
            thread.join()

    def test_decorator_1(self):
        sig = signal.SIGTERM
        handler = SignalHandler()
        thread = Thread(target=self.kill_me_after, args=(3.0, sig))

        @handler.listen(sig)
        def innter_func():
            time.sleep(5)

        try:
            with self.assertRaises(SignalInterrupt.SIGTERM):
                thread.start()
                innter_func()
        finally:
            thread.join()

if __name__ == '__main__':
    unittest.main()
