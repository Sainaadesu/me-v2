import time
import sys


def thinking_timer(stop_event):
    """AI боловсруулж байх үеийн хугацаа харуулах timer"""

    seconds = 0

    print("AI бодож байна... 0с")

    while not stop_event.is_set():

        time.sleep(1)
        seconds += 1

        sys.stdout.write("\033[F")
        sys.stdout.write(f"AI бодож байна... {seconds}с\n")
        sys.stdout.flush()
