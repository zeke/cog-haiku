# https://github.com/herval/creative_machines/blob/master/haikuzao/src/main/resources/haiku.txt

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def load_all():
  with open('haiku.txt') as f:
    lines = f.readlines()
    haikus = [ ]
    for chunk in list(chunks(lines, 4)):
      haiku = "".join(chunk).strip()
      haikus.append(haiku)

    while("" in haikus) :
      haikus.remove("")

    return haikus