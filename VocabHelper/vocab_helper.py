from Foundation import NSRange
from DictionaryServices import DCSGetTermRangeInString, DCSCopyTextDefinition
import genanki
import sys
from typing import List

MODEL_ID = 1190284380
DECK_ID  = 1336545183

word_def_model = genanki.Model(
    MODEL_ID,
    "Vocab Helper Model",
    fields=[
        {"name": "Word"},
        {"name": "Definition"}
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "<h3 style='text-align: center'>{{Word}}</h3><hr/>",
            "afmt": "<h3 style='text-align: center'>{{Word}}</h3><hr/>{{Definition}}"
        }
    ]
)


class VocabHelperNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "Words.md"
    deck = create_flashcards(get_words(path))
    if ("anki" in sys.argv[0]):
        mw.checkpoint("Add Notes from Vocab Helper")
        genanki.Package(deck).write_to_collection_from_addon()
        mw.reset()
    else:
        genanki.Package(deck).write_to_file("out.apkg")

def get_words(filename: str) -> List[str]:
    out = []
    with open(filename) as file:
        for line in file:
            idx = 0
            while idx < len(line) and not str.isalnum(line[idx]):
                idx += 1
            word = line[idx:-1]
            if (len(word)):
                out.append(word)
    return out

def create_flashcards(words: List[str]) -> genanki.Deck:
    deck = genanki.Deck(DECK_ID, "Vocab Helper")

    for word in words:
        print(word)
#        rng = DCSGetTermRangeInString(None, word, 0)
        rng = NSRange(0, len(word))
        defn = DCSCopyTextDefinition(None, word, rng)
        
        if (defn):
            note = VocabHelperNote(model=word_def_model, fields=[word, defn])
        else:
            print(f"skipping word: {word}")
        deck.add_note(note)

    return deck

if __name__ == "__main__":
    main()
