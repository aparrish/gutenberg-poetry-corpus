import json
import re
import codecs
import sys

from gutenbergdammit.ziputils import searchandretrieve
import wordfilter

def clean(s):
    "removes leading numbers and trailing numbers with whitespace"
    match = re.search(r"( {3,}\d+\.?)$", s)
    if match:
        s = s[:match.start()]
    s = re.sub(r"\[\d+\]", "", s)
    return s

# sorta hamfisted criteria for determining if a line of text is a line of
# "poetry." each function receives the text of the line to check along with the
# text of the previous line. all checks must succeed for the line to be
# included. TODO: Replace this with an actual classifier.

checks = {
    # between five and sixty-five characters (inclusive)
    'length': lambda prev, line: 5 <= len(line) <= 65,
    # not all upper-case
    'case': lambda prev, line: not(line.isupper()),
    # doesn't begin with a roman numeral
    'not_roman_numerals': lambda prev, line: \
            not(re.search("^[IVXDC]+\.", line)),
    # if the last line was long and this one is short, it's probably the end of
    # a paragraph
    'not_last_para_line': lambda prev, line: \
            not(len(prev) >= 65 and len(line) <= 65),
    # less than 25% of the line is punctuation characters
    'punct': lambda prev, line: \
        (len([ch for ch in line if ch.isalpha() or ch.isspace()]) / \
            (len(line)+0.01)) > 0.75,
    # doesn't begin with a bracket (angle or square)
    'no_bracket': lambda prev, line: \
            not(any([line.startswith(ch) for ch in '[<'])),
    # isn't in title case
    'not_title_case': lambda prev, line: not(line.istitle()),
    # isn't title case when considering only longer words
    'not_mostly_title_case': lambda prev, line: \
        not(" ".join([w for w in line.split() if len(w) >= 4]).istitle()),
    # not more than 50% upper-case characters
    'not_mostly_upper': lambda prev, line: \
        (len([ch for ch in line if ch.isupper()]) / (len(line)+0.01)) < 0.5,
    # doesn't begin or end with a digit
    'not_number': lambda prev, line: \
            not(re.search("^\d", line)) and not(re.search("\d$", line)),
    # passes the wordfilter
    'wordfilter_ok': lambda prev, line: not(wordfilter.blacklisted(line))
}

def err(*args):
    print(*args, file=sys.stderr)

if __name__ == '__main__':

    # remove some terms from wordfilter because they were filtering large
    # numbers of inoffensive lines; added one because its presence in this
    # corpus is almost always questionable. (terms in rot13 as a kind of
    # content warning)
    wordfilter.remove_words([codecs.encode(item, "rot_13") 
        for item in ['ynzr', 'pevc', 'tnfu', 'fcvp']])
    wordfilter.add_words([codecs.encode("wrj", "rot_13")])

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--srczip",
            help="path to gutenberg-dammit-files zip",
            default="gutenberg-dammit-files-v002.zip")
    options, _ = parser.parse_args()

    err("finding books of poetry in", options.srczip, "...")

    poetry = list(searchandretrieve(options.srczip, {
            'Language': 'English',
            'Subject': lambda x: 'poetry' in x.lower(),
            'Copyright Status': lambda x: not(x.startswith("Copyrighted"))
    }))

    err("done.")
    err("finding lines of poetry in", len(poetry), "books of poetry...")

    poem_lines = []
    line_count = 0
    for metadata, text in poetry:
        prev = ""
        for line in text.split("\n"):
            line = clean(line.strip())
            check_results = {k: v(prev, line) for k, v in checks.items()}
            if all(check_results.values()):
                poem_lines.append((line, metadata['Num']))
            line_count += 1
            prev = line

    err("done.")
    err("found", len(poem_lines), "lines of poetry, of", line_count, "total.")

    err("printing to stdout...")
    for line in poem_lines:
        print(json.dumps({'s': line[0], 'gid': line[1]}))

