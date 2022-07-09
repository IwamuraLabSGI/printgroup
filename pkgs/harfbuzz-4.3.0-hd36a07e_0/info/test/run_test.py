#  tests for harfbuzz-4.3.0-hd36a07e_0 (this is a generated file);
print('===== testing package: harfbuzz-4.3.0-hd36a07e_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import gi
gi.require_version('HarfBuzz', '0.0')
from gi.repository import HarfBuzz as hb
import sys

if hb.buffer_create () is None:
    sys.exit(1)
#  --- run_test.py (end) ---

print('===== harfbuzz-4.3.0-hd36a07e_0 OK =====');
