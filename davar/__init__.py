# import stuff to top level
from davar.parsing import transcribe
from davar.utils import Davar
import nltk
import __main__

try:
    nltk.data.find(r"corpora/omw")
except LookupError:
    nltk.download("omw", r"./nltk_data")

__version__ = "0.1.1"
name = "davar"
