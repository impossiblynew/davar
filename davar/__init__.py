# import stuff to top level
from davar.parsing import transcribe
from davar.utils import Davar
import nltk

nltk.data.path.append(r"./nltk_data")

try:
    nltk.data.find(r"corpora/omw")
except LookupError:
    nltk.download("omw", r"./nltk_data")

try:
    nltk.data.find(r"corpora/wordnet")
except LookupError:
    nltk.download("wordnet", r"./nltk_data")


__version__ = "0.2.0"
name = "davar"
