import React, { useState } from 'react'

export default function Main() {
    // Variables for song and artist name
    const [song_name, set_song_name] = useState(null);
    const [artist_name, set_artist_name] = useState(null);
    // Saves if user input was correct
    const [wrongInputIsShown, setWrongInputIsShown] = useState(false);
    // Saves mood and the similar songs for the given song
    const [mood, setMood] = useState(null);
    const [similar_songs, setSimilarSongs] = useState(null);

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
            response.then(res => {
                setMood(res.mood)
                setSimilarSongs(res.similar_songs)
                console.log(res.mood)
                console.log(res.similar_songs)
            })
            console.log("Request finished...")
        } else {
            // Display error message
            setWrongInputIsShown(true)
            setMood(null)
            setSimilarSongs(null)
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
            {wrongInputIsShown && <p id="errorMissingInput">Please fill out both song and artist name</p>}
            <div id='recommendationsDiv'>
                { similar_songs && Object.keys(similar_songs) && Object.keys(similar_songs).map((key, index) => {
                        return(
                            <p>{key}: {similar_songs[key]}</p>
                        );
                })}
                { similar_songs && Object.keys(similar_songs) && Object.values(similar_songs).map((value, index) => {
                        return(
                            <p>key = {index}  {value}</p>  
                        );
                })}
            </div>
        </div >
    )
}