#!/usr/bin/python3

import stanfordnlp
stanfordnlp.download('en')
nlp = stanfordnlp.Pipeline()
doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
doc.sentences[0].print_dependencies()

