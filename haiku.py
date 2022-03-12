# Haikus copied from:
# https://github.com/herval/creative_machines/blob/master/haikuzao/src/main/resources/haiku.txt

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def load_all():
  with open('haiku.txt') as file:

    haikus = []

    for stanza in file.read().split("\n\n"):
      
      # trim whitespace
      stanza = stanza.strip()

      # collect all three-line stanzas
      if stanza.count("\n") == 2:
        haikus.append(stanza)

    return haikus