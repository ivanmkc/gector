from transformers import AutoTokenizer, AutoModel
import os

# define the name of the directory to be created
DIRECTORY = "./bert-base-cased"

try:
    os.mkdir(DIRECTORY)
except OSError:
    print("Creation of the directory %s failed" % DIRECTORY)
else:
    print("Successfully created the directory %s " % DIRECTORY)

AutoTokenizer.from_pretrained("bert-base-cased").save_pretrained(DIRECTORY)
AutoModel.from_pretrained("bert-base-cased").save_pretrained(DIRECTORY)
