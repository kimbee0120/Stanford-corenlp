import stanza
stanza.download('en') 
nlp = stanza.Pipeline('en') # initialize English neural pipeline
doc = nlp("Barack Obama was born in Hawaii.")
print(doc)
print(doc.entities)
