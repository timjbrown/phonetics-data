import json

expansions = {
    "ER": ["AH2", "R"],
    "OR": ["O", "R"],
    "EL": ["AH2", "L"],
    "EM": ["AH2", "M"],
    "EN": ["AH2", "N"],
}
with open("out/customToConsonantVowel.json", "r", encoding="utf8") as custom_to_consonant_vowel_file:
    custom_to_consonant_vowel = json.load(custom_to_consonant_vowel_file)


def dict_to_file(dct, filename):
    if filename.endswith(".json"):
        with open(filename, "w", encoding="utf8") as file:
            json.dump(
                dct, file, ensure_ascii=False
            )  # ensure_ascii=False to encode properly
        print("Wrote", filename)
    elif filename.endswith(".txt"):
        with open(filename, "w", encoding="utf8") as file:
            for k, v in dct.items():
                file.write(f"{k}  {v}\n")
        print("Wrote", filename)
    else:
        print("Failed to write", filename)


def file_to_dict(filename):
    dct = {}
    with open(filename, "r", encoding="utf8") as file:
        for line in file:
            line = line.strip()
            tokens = line.split()
            if len(tokens) < 2 or line.startswith("#") or line.startswith("/"):
                continue
            tokens_rest_str = " ".join(tokens[1:])
            if "," in line:  # multiple entries
                dct[tokens[0]] = tokens_rest_str.split(",", maxsplit=1)[0]
            else:  # one entry
                dct[tokens[0]] = tokens_rest_str
    return dct


def matches_pattern(phones, startIndex, pattern):
    tokens = pattern.split()
    if len(phones) - startIndex < len(tokens):
        return False
    for i, token in enumerate(tokens):
        phone = phones[startIndex + i]
        if token not in (phone, custom_to_consonant_vowel[phone]):
            return False
    return True


def expand(phones):
    new_phones = []
    for phone in phones:
        expansion = expansions.get(phone)
        if expansion:
            new_phones.extend(expansion)
        else:
            new_phones.append(phone)
    return new_phones


def mutate(phones):
    phones = [f"{phone}2" if phone in ["IY", "UW"] else phone for phone in phones]
    for i, phone in enumerate(phones):
        if matches_pattern(phones, i, "v IY2") and phone not in ["OY", "EY", "AY"]:
            phones[i + 1] = "IY"
        if matches_pattern(phones, i, "IY2 v") and phones[i + 1] not in ["IH"]:
            phones[i] = "IY"
        if matches_pattern(phones, i, "UW2 v") and phones[i + 1] not in ["IH"]:
            phones[i] = "UW"
    return phones


def translate(text, dct):
    tokens = text.split()
    if len(tokens) > 1 or text.isupper():
        tokens = mutate(expand(tokens))
        return "".join([dct[token] for token in tokens])
    return text


def generate(*filenames):
    in_filenames = filenames[0:-1]
    out_filename = filenames[-1]
    dcts = []
    for in_filename in in_filenames:
        if isinstance(in_filename, str):
            dcts.append(file_to_dict(in_filename))
        else:  # dictionary
            dcts.append(in_filename)

    dct = dcts[0].copy()
    for k, v in dct.items():
        for d in dcts[1:]:
            dct[k] = translate(v, d)
    dict_to_file(dct, out_filename)


def clean_ipa(filename):
    dct = file_to_dict(filename)
    for k, v in dct.items():
        dct[k] = dct[k].replace("/", "")
        dct[k] = dct[k].replace("ˈ", "")
        dct[k] = dct[k].replace("ˌ", "")
    return dct


def main():
    generate("txt/customToSoundscript1.txt", "out/customToSoundscript1.json")
    generate("txt/customToSoundscript2.txt", "out/customToSoundscript2.json")
    generate("txt/customToIPA.txt", "out/customToIPA.json")
    generate("txt/customToArpabet1.txt", "out/customToArpabet1.json")
    generate("txt/customToArpabet2.txt", "out/customToArpabet2.json")
    generate("txt/customToXSampa.txt", "out/customToXSampa.json")
    generate("txt/customToDeseret.txt", "out/customToDeseret.json")
    generate("txt/customToShavian.txt", "out/customToShavian.json")
    generate("txt/customToConsonantVowel.txt", "out/customToConsonantVowel.json")

    generate("txt/esperantoToCustom.txt", "out/esperantoToCustom.json")
    generate("txt/japaneseToCustom.txt", "out/japaneseToCustom.json")
    generate("txt/sinhaleseToCustom.txt", "out/sinhaleseToCustom.json")
    generate("txt/englishToCustom.txt", "out/englishToCustom.json")
    # generate(clean_ipa('../ipa-dict/data/de.txt'), 'out/germanToIPA.json')

    # generate('txt/englishToCustom.txt', 'txt/customToSoundscript1.txt', 'out/englishToSoundscript.txt')
    generate('txt/englishToCustom.txt', 'txt/customToSoundscript1.txt', 'out/englishToSoundscript.json')


if __name__ == "__main__":
    main()
