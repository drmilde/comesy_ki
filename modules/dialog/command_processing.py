from fuzzywuzzy import fuzz
from fuzzywuzzy import process

komandos = ["links", "nach links", "rechts", "nach rechts", "weiter", "stop"]

def checkCommand(input):
    max = 160;
    result = input
    for command in komandos:
        #print(f'{command}:{input}')
        vr = fuzz.ratio(input.lower(), command)
        vp = fuzz.partial_ratio(input.lower(), command)
        #print (vr)
        #print (vp)
        if ((vr + vp) > max):
            max = vr + vp;
            result = command
    return result


