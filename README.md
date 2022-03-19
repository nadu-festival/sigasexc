# **Sig**nal **As** **Exc**eption

Write code that uses signals like an exception.

## Install
```bash
git clone https://github.com/nadu-festival/sigasexc
cd sigasexc
python setup.py install
```

## Example

Define handler and call handler.listen.

```Python
import signal
from sigasexc import SignalHandler, SignalInterrupt

handler = SignalHandler()

try:
  with handler.listen(signal.SIGUSR1, signal.SIGUSR2):
    # Start convert slgnal interrupt --> exception
    time.sleep(10)
    # Stop convert slgnal interrupt --> exception
except SignalInterrupt.SIGUSR1:
  print("Receive signal.SIGUSR1")
except SignalInterrupt.SIGUSR2:
  print("Receive signal.SIGUSR2")
else:
  print("No signal interrupt")
```


`SignalHandler` can take your original handler, or `signal.Handlers`.

```Python
import signal
from sigasexc import SignalHandler, SignalInterrupt

handler = SignalHandler(signal.SIG_IGN)

with handler.listen(signal.SIGUSR1, signal.SIGUSR2):
  # Start ignore slgnal interrupt
  time.sleep(10)
  # Stop ignore slgnal interrupt
```


For more simple, decorate your function.

```Python
import signal
from sigasexc import SignalHandler, SignalInterrupt

handler = SignalHandler()

@handler.listen(signal.SIGUSR1, signal.SIGUSR2)
def main():
  # Start convert slgnal interrupt
  time.sleep(10)
  # Stop convert slgnal interrupt

if __name__ == '__main__':
  try:
    main()
  except SignalInterrupt.SIGUSR1:
    print("Receive signal.SIGUSR1")
  except SignalInterrupt.SIGUSR2:
    print("Receive signal.SIGUSR2")
  else:
    print("No signal interrupt")
```
