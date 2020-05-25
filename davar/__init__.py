# import stuff to top level
from davar.parsing import transcribe
from davar.utils import Davar
import nltk
import __main__

nltk.download(
    "omw", r"./nltk_data"
)  # FIXME: #5 Tries to install even if already installed.

__version__ = "0.1.1"
name = "davar"
