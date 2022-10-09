import json

expansions = {'ER':['AH2', 'R'], 'OR':['O', 'R'], 'EL':['AH2', 'L'], 'EM':['AH2', 'M'], 'EN':['AH2', 'N']}
with open('out/customToConsonantVowel.json', 'r', encoding='utf8') as file:
    customToConsonantVowel = json.load(file)

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

def file_to_dict(filename):
    dct = {}
    with open(filename, 'r', encoding='utf8') as file:
        for line in file:
            line = line.strip()
            tokens = line.split()
            if len(tokens) < 2 or line.startswith('#') or line.startswith('/'): continue
            dct[tokens[0]] = ' '.join(tokens[1:])
    return dct

def matchesPattern(phones, startIndex, pattern):
    tokens = pattern.split()
    if len(phones) - startIndex < len(tokens):
        return False
    for i,token in enumerate(tokens):
        phone = phones[startIndex + i]
        if token != phone and token != customToConsonantVowel[phone]:
            return False
    return True

def expand(phones):
    new_phones = []
    for phone in phones:
        expansion = expansions.get(phone)
        if expansion: new_phones.extend(expansion)
        else: new_phones.append(phone)
    return new_phones

def mutate(phones):
    phones = [f'{phone}2' if phone in ['IY', 'UW'] else phone for phone in phones]
    for i,phone in enumerate(phones):
        if matchesPattern(phones, i, 'v IY2') and phone not in ['OY', 'EY', 'AY']:
            phones[i + 1] = 'IY'
        if matchesPattern(phones, i, 'IY2 v') and phones[i + 1] not in ['IH']:
            phones[i] = 'IY'
        if matchesPattern(phones, i, 'UW2 v') and phones[i + 1] not in ['IH']:
            phones[i] = 'UW'
    return phones

def translate(text, dct):
    tokens = text.split()
    if len(tokens) > 1 or text.isupper():
        tokens = mutate(expand(tokens))
        return ''.join([dct[token] for token in tokens])
    return text

def generate(*filenames):
    inFilenames = filenames[0:-1]
    outFilename = filenames[-1]
    dcts = [file_to_dict(inFilename) for inFilename in inFilenames]
    dct = dcts[0].copy()
    for k in dct:
        for d in dcts[1:]:
            dct[k] = translate(dct[k], d)
    dict_to_file(dct, outFilename)

def main():
    generate('txt/customToSoundscript1.txt', 'out/customToSoundscript1.json')
    generate('txt/customToSoundscript2.txt', 'out/customToSoundscript2.json')
    generate('txt/customToIPA.txt', 'out/customToIPA.json')
    generate('txt/customToArpabet1.txt', 'out/customToArpabet1.json')
    generate('txt/customToArpabet2.txt', 'out/customToArpabet2.json')
    generate('txt/customToXSampa.txt', 'out/customToXSampa.json')
    generate('txt/customToDeseret.txt', 'out/customToDeseret.json')
    generate('txt/customToShavian.txt', 'out/customToShavian.json')
    generate('txt/customToConsonantVowel.txt', 'out/customToConsonantVowel.json')

    generate('txt/esperantoToCustom.txt', 'out/esperantoToCustom.json')
    generate('txt/japaneseToCustom.txt', 'out/japaneseToCustom.json')
    generate('txt/sinhaleseToCustom.txt', 'out/sinhaleseToCustom.json')
    generate('txt/englishToCustom.txt', 'out/englishToCustom.json')

    generate('txt/englishToCustom.txt', 'txt/customToSoundscript1.txt', 'out/englishToSoundscript.txt')
    generate('txt/englishToCustom.txt', 'txt/customToSoundscript1.txt', 'out/englishToSoundscript.json')

if __name__ == '__main__':
    main()