import json

def dict_to_file(dict, filename):
    if filename.endswith('.json'):
        with open(filename, 'w', encoding='utf8') as file:
            json.dump(dict, file, ensure_ascii=False) # ensure_ascii=False to encode properly
        print('Wrote', filename)
    elif filename.endswith('.txt'):
        with open(filename, 'w', encoding='utf8') as file:
            for k,v in dict.items():
                file.write(f'{k}  {v}\n')
        print('Wrote', filename)
    else:
        print('Failed to write', filename)

def get_dict(filename):
    dct = {}
    with open(filename, 'r', encoding='utf8') as file:
        for line in file:
            line = line.strip()
            tokens = line.split()
            if len(tokens) < 2 or line.startswith('#') or line.startswith('/'): continue
            dct[tokens[0]] = ' '.join(tokens[1:])
    return dct

def translate(text, dct):
    tokens = text.split()
    if len(tokens) > 1:
        result = ''
        for token in tokens:
            result += dct[token]
        return result
    return text

def translate_to_file(*filenames):
    inFilenames = filenames[0:-1]
    outFilename = filenames[-1]
    dcts = [get_dict(inFilename) for inFilename in inFilenames]
    dct = dcts[0].copy()
    for k in dct:
        for d in dcts[1:]:
            dct[k] = translate(dct[k], d)
    dict_to_file(dct, outFilename)

# translate_to_file('txt/customToSoundscript1.txt', 'json/customToSoundscript1.json')
# translate_to_file('txt/customToSoundscript2.txt', 'json/customToSoundscript2.json')
# translate_to_file('txt/customToIPA.txt', 'json/customToIPA.json')
# translate_to_file('txt/customToArpabet1.txt', 'json/customToArpabet1.json')
# translate_to_file('txt/customToArpabet2.txt', 'json/customToArpabet2.json')
# translate_to_file('txt/customToXSampa.txt', 'json/customToXSampa.json')
# translate_to_file('txt/customToDeseret.txt', 'json/customToDeseret.json')
# translate_to_file('txt/customToShavian.txt', 'json/customToShavian.json')
# translate_to_file('txt/customToConsonantVowel.txt', 'json/customToConsonantVowel.json')

# translate_to_file('txt/esperantoToCustom.txt', 'json/esperantoToCustom.json')
# translate_to_file('txt/japaneseToCustom.txt', 'json/japaneseToCustom.json')
# translate_to_file('txt/sinhaleseToCustom.txt', 'json/sinhaleseToCustom.json')
# translate_to_file('txt/englishToCustom.txt', 'json/englishToCustom.json')

# translate_to_file('txt/englishToCustom.txt', 'txt/customToSoundscript1.txt', 'txt/englishToSoundscript1.txt')
# translate_to_file('txt/englishToCustom.txt', 'txt/customToSoundscript1.txt', 'json/englishToSoundscript1.json')