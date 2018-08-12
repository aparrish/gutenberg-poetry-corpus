# A Gutenberg Poetry Corpus

By [Allison Parrish](https://www.decontextualize.com/)

This is a Gutenberg Poetry corpus, comprised of approximately three million
lines of poetry extracted from hundreds of books from [Project
Gutenberg](https://gutenberg.org/). The corpus is especially suited to
applications in creative computational poetic text generation.

[Download the corpus here.](http://static.decontextualize.com/gutenberg-poetry-v001.ndjson.gz)

## How to use it

The corpus is provided as a gzipped [newline-delimited JSON format](http://ndjson.org/).
Here's a representative excerpt:

    {"s": "The Heav'ns and all the Constellations rung,", "gid": "20"}
    {"s": "The Planets in thir stations list'ning stood,", "gid": "20"}
    {"s": "While the bright Pomp ascended jubilant.", "gid": "20"}
    {"s": "Open, ye everlasting Gates, they sung,", "gid": "20"}
    {"s": "Open, ye Heav'ns, your living dores; let in", "gid": "20"}

Each line of poetry is represented by a JSON object, with one object per line
in the archive. The value for the `s` key is the line of poetry itself, and the
value for the `gid` key is the ID of the Project Gutenberg book that the line
comes from. You can use the value for `gid` to look up the title and author of
the book that serves as that line's source, either "by hand" (just type the ID
into Project Gutenberg's search box) or using a computer-readable version of
the Project Gutenberg metadata (such as [Gutenberg,
dammit](https://github.com/aparrish/gutenberg-dammit/)).

The [Quick Experiments notebook](quick-experiments.ipynb) included in this
repository shows how to get up and running quickly with the corpus in Python.
No need to install the Python module in this repository---working with the data is
surprisingly straightforward!

## How it was made

The corpus was generated using the included `build.py` script, which uses 
[Gutenberg, dammit](https://github.com/aparrish/gutenberg-dammit/) to provide
access to books from Project Gutenberg. First, books with the string `poetry`
listed in their "Subject" metadata are added to a list. Then, the plaintext
versions of those books are scanned for lines that "look like" poetry, based on
a set of textual characteristics, such as their length and capitalization.
(See `build.py` for a list of these characteristics.) Finally, lines are
compared against a word list (from
[wordfilter](https://github.com/dariusk/wordfilter)) to exclude lines that
may contain egregiously offensive content.

> NOTE: While a best-effort attempt has been made to exclude offensive language
> from this corpus, I have not personally vetted each of the three million
> lines. If you use this corpus to produce work for the public, please read
> over it first or take approriate measures to ensure that the language in the
> work is appropriate for you and your audience.read over it first or take
> approriate measures to ensure that the language in the work is appropriate
> for you and your audience.

The corpus contains only lines of poetry from books that the Project Gutenberg
metadata identifies as being written in English and as being free from
copyright (i.e., public domain) in the United States.

## Examples of usage

Previous versions of this corpus have served as a foundation for several
projects produced by myself and others:

* [Gutenberg Poetry
  Autocomplete](http://gutenberg-poetry.decontextualize.com/), a search
  engine-like interface for writing poems mined from Project Gutenberg. (A poem
  written using this interface was [recently published in the Indianapolis
  Review](https://theindianapolisreview.com/betting-the-under/)!)
* [*Articulations*](http://counterpathpress.org/articulations-allison-parrish),
  a book of poetry created by finding phonetically similar lines of poetry in
  Project Gutenberg
* [Plot to Poem](http://static.decontextualize.com/plot-to-poem.html), a quick
  [NaPoGenMo](https://github.com/NaPoGenMo/) project that finds the lines of
  poetry closest in meaning to sentences from Wikipedia plot summaries
* [Lynn Cherny](http://www.ghostweather.com/) used a version of this corpus to
  do [some quick and dirty computational stylistics on computer-generated
  poetry](https://medium.com/@lynn_72328/cocos-memory-palace-a-strange-fantasia-28b48264612f).

If you make something cool with this corpus, let me know!

## Build your own from scratch

You don't need to read any of the following if you just want to use the corpus.
If you're interested in building your own version from scratch, read on.

This repository includes a script to build the Gutenberg Poetry corpus from the
files included in [Gutenberg,
dammit](https://github.com/aparrish/gutenberg-dammit/). First, download the
*Gutenberg, dammit* archive. Then install this package, like so:

```bash
pip install --process-dependency-links https://github.com/aparrish/gutenberg-poetry-corpus/archive/master.zip
```

You can then run the following command to produce your own version of the
corpus:

```bash
python -m gutenbergpoetrycorpus.build --srczip=PATH-TO-GUTENBERG-DAMMIT-ZIP | gzip -c >gutenberg-poetry.ndjson.gz
```

Parameters for what gets included in the corpus can be adjusted in `build.py`.
(E.g., it should be relatively easy to adapt this script to produce corpora of
poetry in different languages!)

## License

To the best of my knowledge, the Gutenberg Poetry corpus contains only text
excerpted from works that are is in the public domain (at least in the United
States). For avoidance of doubt, I release the particular arrangement of these
excerpts in the provided format as
[CC0](https://creativecommons.org/share-your-work/public-domain/cc0/).

The code in this repository is provided under the following license:

    Copyright 2018 Allison Parrish

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

