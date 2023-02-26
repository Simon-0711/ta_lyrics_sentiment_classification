import React, { useState } from 'react'

export default function Main() {
    // Variables for song and artist name
    const [song_name, set_song_name] = useState(null);
    const [artist_name, set_artist_name] = useState(null);
    // Saves if user input was correct
    const [wrongInputIsShown, setWrongInputIsShown] = useState(false);
    // Saves mood and the similar songs and the looked up sopng/artist
    const [mood, setMood] = useState(null);
    const [similar_songs, setSimilarSongs] = useState(null);
    const [returned_song, setReturnedSong] = useState(null);
    const [returned_artist, setReturnedArtist] = useState(null);
    // error variable to catch the error if no song was found
    const [songNotFound, setsongNotFound] = useState(null);
    const [searchState, setSearchState] = useState(false);

    // Functions to get song and artist name
    function getSongName(input_box_input) {
        set_song_name(input_box_input.target.value)
    }
    function getArtistName(input_box_input) {
        set_artist_name(input_box_input.target.value)
    }

    async function postData(url = '', data = {}) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: data
        })
        return response.json();
    }

    // Function to send song and artist name to fast api
    function sendToFastApi(song_name, artist_name) {
        // Set variables to null to not produce output before new search
        setWrongInputIsShown(false)
        setReturnedSong(null)
        setReturnedArtist(null)
        setMood(null)
        setSimilarSongs(null)
        setsongNotFound(null)
        // Display "searching..." in frontend
        setSearchState(true)
        console.log("hi")
        console.log(searchState)
        if ((song_name) && (artist_name)) {
            // Don't display error message
            setWrongInputIsShown(false)
            // Send to fast api
            console.log("Sending song and artist to fastapi...")
            console.log(JSON.stringify({ song_name: song_name, artist_name: artist_name }))
            const response = postData(
                "http://localhost:8000/search",
                JSON.stringify({ song_name: song_name, artist_name: artist_name })
            )
            console.log(response)
            response.then(res => {
                if (res.error === 404) {
                    setsongNotFound(true)
                }
                else {
                    setReturnedSong(res.Song)
                    setReturnedArtist(res.Artist)
                    setMood(res.mood)
                    setSimilarSongs(res.similar_songs)
                    setsongNotFound(false)
                }
                setSearchState(false)
            })
            console.log("Request finished...")
        } else {
            // Display error message
            setWrongInputIsShown(true)
            setReturnedSong(null)
            setReturnedArtist(null)
            setMood(null)
            setSimilarSongs(null)
            setsongNotFound(null)
            setSearchState(false)
        }
    }

    return (
        <div id='mainDiv'>
            <h1 id='mainHeader'>Looking for similar Songs?</h1>
            <p id='lyricsRequest'>Just give us a song and artist name. We will find songs with a similar mood while you sit back and relax. </p>

            <div id="searchInput" className="searchInput">
                <input type="text" name="inputSong" id="inputSong" required spellCheck="false" placeholder='Song Name' onChange={getSongName}></input>
                <input type="text" name="inputArtist" id="inputArtist" required spellCheck="false" placeholder='Artist Name' onChange={getArtistName}></input>
            </div>
            <button id='searchSimilarLyricsButton' name="searchLyrics" onClick={() => sendToFastApi(song_name, artist_name)}>Find Similar Songs</button>
            {searchState && <p id="output_songs">Searching...</p>}
            {wrongInputIsShown && <p id="errorMissingInput">Please fill out both song and artist name</p>}
            {songNotFound && <p id="errorMissingInput">No result for this song and artist combination. Check the input for typos or try another one!</p>}
            {!songNotFound && mood != null && similar_songs != null && returned_artist != null && returned_song != null && !wrongInputIsShown && <p id="output_songs">Similar songs for '{returned_song}' from '{returned_artist}' with a '{mood}' mood: </p>}
            {!songNotFound && mood != null && similar_songs != null && returned_artist != null && returned_song != null && !wrongInputIsShown && <p id="output">{Object.keys(similar_songs).map((key) => {
                return (
                    <p>Song: {similar_songs[key].Song}, Artist: {similar_songs[key].Artist}, Similarity: {similar_songs[key].Similarity} %</p>
                );
            })}</p>}

        </div >
    )
}