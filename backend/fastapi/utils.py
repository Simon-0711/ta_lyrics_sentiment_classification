import re
def chorus_normalization(original_lyrics):
    lyrics = original_lyrics
    # filter everything in [..]
    lyrics = re.sub("\[[^]]*\]", "", lyrics)
    # filter everything in (..)
    lyrics = re.sub("\([^)]*\)", "", lyrics)
    # filter everything in {..}
    lyrics = re.sub("\{[^}]*\}", "", lyrics)
    # filter everything in <..>
    lyrics = re.sub("\<[^>]*\>", "", lyrics)
    # filter everything in ::..::
    lyrics = re.sub("::[^(::)]*::", "", lyrics)
    
    # filter more specific combinations of chorus
    lyrics = re.sub("\nchorus\n", "", lyrics)
    lyrics = re.sub("\[chorus", "", lyrics)
    lyrics = re.sub("\nchorus", "", lyrics)
    lyrics = re.sub("pre[-]?chorus", "", lyrics)
    lyrics = re.sub("\nrepeat chorus\n", "", lyrics)
    
    return lyrics
    # TODO: ideas for further cleaning:
        # TODO: could also just remove something like chorus, verse, ... completely since it should not have impact on classification (just need to be careful with words containing the keywords like "uni-verse")
        # TODO: do same/similar specific "chorus" cleaning steps for verse, ...
        # TODO: remove all artists names
        # TODO: replace \n, \w, \t,... with " " (after all cleaning steps involving \n, maybe regarding chorus, ...) 
        # TODO: as last step remove all non-alphabetic characters