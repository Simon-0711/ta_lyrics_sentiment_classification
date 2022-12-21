import spacy

def tokenization(text: str) -> list[spacy.tokens.token.Token]:
    """Use this function to tokenize text.

    :param text: Text to tokenize
    :type text: string
    :return: Tokenized text as list
    :rtype: list[spacy.tokens.token.Token]
    """
    nlp = spacy.load("en_core_web_sm", disable = ['ner'])

    token_list = []
    for doc in list(nlp.pipe([text])): 
        # iterate over tokens in docs
        for token in doc:
            token_list.append(token)

    return token_list


def stop_word_removal(text: list[spacy.tokens.token.Token]) -> list[spacy.tokens.token.Token]: 
    """Use this function to remove stop words. 

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
    """Use this function to remove punctuation.

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
    """Use this function to lemmatize a given text.

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


def processing_pipeline(song_data: dict) -> dict:
    """Use this function to execute the entire processing pipeline on given song data.
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
    
    # Tokenization
    song_data["Lyrics"] = tokenization(song_data["Lyrics"])
    # Stop word removal
    song_data["Lyrics"] = stop_word_removal(song_data["Lyrics"])
    # Punctuation removal
    song_data["Lyrics"] = punctutation_removal(song_data["Lyrics"])
    # Lemmatization
    song_data["Lyrics"] = lemmatization(song_data["Lyrics"])

    return song_data
