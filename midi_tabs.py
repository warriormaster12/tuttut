import pretty_midi
from app.tab import Tab
from app.theory import Tuning, Note
import argparse
import traceback
from time import time
import numpy as np
from pathlib import Path

def init_parser():
  """Initializes the argument parser for execution.

  Returns:
      argparse.ArgumentParser: The parser object
  """
  parser = argparse.ArgumentParser(description="MIDI to Guitar Tabs convertor")
  parser.add_argument("source", metavar="src", type=Path, help = "Name of the MIDI file to convert")
  return parser

if __name__ == "__main__":
  np.seterr(divide="ignore")
  parser = init_parser()
  args = parser.parse_args()

  file = args.source.with_suffix(".mid")

  try:
    start = time()
    f = pretty_midi.PrettyMIDI(Path("./midis", file).as_posix())
    tab = Tab(file.stem, Tuning(), f)
    # tab = Tab(file.stem, Tuning(), f, weights={'b': 0.5, 'height': 0.09090909090909091, 'length': 0.45454545454545453, 'n_changed_strings': 0.45454545454545453})
    tab.to_ascii()
    tab.to_json()
    print("Time :", time() - start)

  except Exception as e:
    print(traceback.print_exc())
    print("There was an error. You might want to try another MIDI file. The tool tends to struggle with more complicated multi-channel MIDI files.")