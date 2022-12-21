def tokenization(text: str) -> str:
    """Use this function to tokenize text.

    :param text: Text to tokenize
    :type text: string
    :return: Tokenized text
    :rtype: str
    """
    return print("Tokenized")


def stop_word_removal(text: str) -> str: 
    """Use this function to remove stop words. 

    :param text: Text to remove stop words from 
    :type text: str
    :return: Text without stop words
    :rtype: str
    """
    return print("Stop words removed")


def punctutation_removal(text: str) -> str: 
    """Use this function to remove punctuation.

    :param text: Text to remove punctuation from
    :type text: str
    :return: Text without punctuation
    :rtype: str
    """
    return print("Punctuation removed")


def lemmatization(text: str) -> str: 
    """Use this function to lemmatize a given text.

    :param text: Text to lemmatize
    :type text: str
    :return: lemmatized text
    :rtype: str
    """
    return print("Lemmatized")


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
