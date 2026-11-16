"""fm1_install wrapper using /dev/snd/midiC0D0 raw MIDI (for WSL2 where ALSA sequencer is unavailable)."""
import queue
import threading
import time
import glob
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from fm1_install import main

DEVICE_NAME = "Felucca"

def find_raw_device():
    for path in glob.glob("/dev/snd/midiC*D*"):
        return path
    return None


class RawMidiLink:
    def __init__(self, path, name):
        self.name = name
        self._path = path
        self._q = queue.Queue()
        self._fh = open(path, "r+b", buffering=0)
        self._stop = threading.Event()
        self._t = threading.Thread(target=self._reader, daemon=True)
        self._t.start()
        time.sleep(0.05)

    def _reader(self):
        buf = bytearray()
        while not self._stop.is_set():
            try:
                self._fh._checkClosed()
            except Exception:
                break
            try:
                b = self._fh.read(1)
            except Exception:
                break
            if not b:
                continue
            byte = b[0]
            if byte == 0xF0:
                buf = bytearray([0xF0])
            elif buf:
                buf.append(byte)
                if byte == 0xF7:
                    self._q.put(bytes(buf))
                    buf = bytearray()

    @property
    def lost(self):
        return not os.path.exists(self._path)

    def send(self, pkt):
        try:
            self._fh.write(bytes(pkt))
            return True
        except Exception:
            return False

    def read(self, timeout):
        try:
            return self._q.get(timeout=max(timeout, 0))
        except queue.Empty:
            return None

    def drain(self):
        while not self._q.empty():
            try:
                self._q.get_nowait()
            except queue.Empty:
                break

    def close(self):
        self._stop.set()
        try:
            self._fh.close()
        except Exception:
            pass


class RawMidiBackend:
    def __init__(self, path):
        self._path = path

    def input_names(self):
        return [DEVICE_NAME] if os.path.exists(self._path) else []

    def output_names(self):
        return [DEVICE_NAME] if os.path.exists(self._path) else []

    def open(self, in_name, out_name):
        return RawMidiLink(self._path, in_name)


if __name__ == "__main__":
    path = find_raw_device()
    if not path:
        sys.exit("error: no raw MIDI device found at /dev/snd/midiC*D*")
    print(f"using raw MIDI device: {path}", file=sys.stderr)
    backend = RawMidiBackend(path)
    sys.exit(main(backend=backend))
