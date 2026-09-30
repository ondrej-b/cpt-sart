'''
Cedrus RB-840 (XID) button mapping tool.

Run this standalone (no PsychoPy window, no monitor calibration needed) to
find out which XID button number corresponds to which physical key on the
pad. Press keys one at a time and read the printed button number, then set
CEDRUS_LEFT_BUTTON / CEDRUS_RIGHT_BUTTON in sart-tp.py accordingly.

Ctrl+C to quit.
'''
try:
    import pyxid2
except ImportError:
    raise SystemExit(
        "pyxid2 isn't installed in this Python environment.\n"
        'Install with:  pip install pyxid2'
    )

devices = pyxid2.get_xid_devices()
if not devices:
    raise SystemExit(
        'No Cedrus XID device found. Check it is connected, powered on '
        '(should show a light), and its drivers are installed.'
    )

dev = devices[0]
print(f'Connected to: {getattr(dev, "device_name", dev)}')
print('Press buttons on the pad. Ctrl+C to quit.\n')

dev.reset_timer()
try:
    while True:
        dev.poll_for_response()
        while dev.response_queue:
            evt = dev.get_next_response()
            state = 'pressed' if evt['pressed'] else 'released'
            print(f'button {evt["key"]}  ({state}, port {evt["port"]}, t={evt["time"]} ms)')
except KeyboardInterrupt:
    print('\nStopped.')
