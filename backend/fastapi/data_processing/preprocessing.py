import spacy

def tokenization(text: str) -> list:
    """Use this function to tokenize text.

    :param text: Text to tokenize
    :type text: string
    :return: Tokenized text as list
    :rtype: list[str]
    """
    nlp = spacy.load("en_core_web_sm", disable = ['ner'])
    print(nlp.pipe_names)


    word_list = []

    # Iterate over the spoken words (Hint: df_script) and append the lemmatized tokens as detailed above
    # test_string = ["This is just a sample text and texts for the purpose of testing"]
    for doc in list(nlp.pipe(text)): 
        # iterate over tokens in docs
        for token in doc:
            # Add token to list
            word_list.append(token)

    return word_list


def stop_word_removal(text: list) -> list: 
    """Use this function to remove stop words. 

    :param text: Text to remove stop words from 
    :type text: str
    :return: Text without stop words
    :rtype: str
    """

    word_list = []

    # Don't add token to list if punctuation or stop word
    for token in text:
        if token.is_stop == False: 
            word_list.append(token)


    return word_list


def punctutation_removal(text: list) -> list: 
    """Use this function to remove punctuation.

    :param text: Text to remove punctuation from
    :type text: str
    :return: Text without punctuation
    :rtype: str
    """

    word_list = []
    
    for token in text:
        if token.is_punct == False
            word_list.append(token)

    return word_list


def lemmatization(text: list) -> list: 
    """Use this function to lemmatize a given text.

    :param text: Text to lemmatize
    :type text: str
    :return: lemmatized text
    :rtype: str
    """

    word_list = []

    for token in text: 
        word_list.append(token.lemma_)
        
    return word_list


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
