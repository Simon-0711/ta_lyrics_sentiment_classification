import re

import spacy


def chorus_normalization(original_lyrics):
    """
    Function gets rid of unnecessary tokens in the lyrics which don't
    add any value to he predections. 

    input: 
    original_lyrics: string
    output: 
    lyrics: string 
    """
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


def processing_pipeline(song_data: dict) -> dict:
    """Function executes the entire processing pipeline on given song data.
    Preprocessing steps:
    - Tokenization
    - Stop word removal
    - Punctuation removal
    - Lemmatization
    - ...

    :param song_data: song data saved in a json file containing song name, artist name and lyrics
    :type song_data: dict
    :return: preprocessed song data
    :rtype: dict
    """

    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    text_nlp_pipe = list(nlp.pipe([song_data["Lyrics"]]))

    # Tokenization
    song_data["Lyrics"] = tokenization(text_nlp_pipe)
    # Stop word removal
    song_data["Lyrics"] = stop_word_removal(song_data["Lyrics"])
    # Punctuation removal
    song_data["Lyrics"] = punctutation_removal(song_data["Lyrics"])
    # Lemmatization
    song_data["Lyrics"] = lemmatization(song_data["Lyrics"])

    return song_data


def tokenization(text: list[spacy.tokens.token.Token]) -> list[spacy.tokens.token.Token]:
    """Function tokenizes text.

    :param text: Text as list
    :type text: list[spacy.tokens.token.Token]
    :return: Tokenized text as list
    :rtype: list[spacy.tokens.token.Token]
    """

    token_list = []
    for doc in text:
        # iterate over tokens in docs
        for token in doc:
            token_list.append(token)

    return token_list


def stop_word_removal(text: list[spacy.tokens.token.Token]) -> list[spacy.tokens.token.Token]:
    """Function removes stop words. 

    :param text: Tokens to remove stop words from 
    :type text: list[spacy.tokens.token.Token]
    :return: Tokens without stop words
    :rtype: list[spacy.tokens.token.Token]
    """

    token_list_without_stop = []
    # Don't add token to list if stop word
    for token in text:
        if token.is_stop == False:
            token_list_without_stop.append(token)

    return token_list_without_stop


def punctutation_removal(text: list[spacy.tokens.token.Token]) -> list[spacy.tokens.token.Token]:
    """Function removes punctuation.

    :param text: Tokens to remove punctuation from
    :type text: list[spacy.tokens.token.Token]
    :return: Tokens without punctuation
    :rtype: list[spacy.tokens.token.Token]
    """

    token_list_no_stop_no_punct = []
    # Don't add token to list if punctuation
    for token in text:
        if token.is_punct == False:
            token_list_no_stop_no_punct.append(token)

    return token_list_no_stop_no_punct


def lemmatization(text: list[spacy.tokens.token.Token]) -> list[str]:
    """Function lemmatizes a given text.

    :param text: Tokens to lemmatize
    :type text: list[spacy.tokens.token.Token]
    :return: lemmatized tokens
    :rtype: list[str]
    """

    token_list_no_stop_no_punct_lemmatized = []
    for token in text:
        if "\n" not in token.lemma_:
            token_list_no_stop_no_punct_lemmatized.append(token.lemma_)
    return token_list_no_stop_no_punct_lemmatized
