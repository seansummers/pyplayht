from sys import stderr

from eliot import log_call, to_file

to_file(stderr)
import picologging as logging
from eliot.stdlib import EliotHandler

logging.getLogger().addHandler(EliotHandler())

__all__ = ["logging", "log_call"]
