import React, { useState } from 'react'

export default function Main() {
    // Variables for song and artist name
    const [song_name, set_song_name] = useState(null)
    const [artist_name, set_artist_name] = useState(null)

    // Functions to get song and artist name
    function getSongName(input_box_input) {
        set_song_name(input_box_input.target.value)
    }
    function getArtistName(input_box_input) {
        set_artist_name(input_box_input.target.value)
    }

    // Function to send song and artist name to fast api
    function sendToFastApi(song_name, artist_name) {
        if ((song_name) && (artist_name)) {
            // send to fast api
            console.log(song_name)
            console.log(artist_name)
        }
    }

    return (
        <div id='mainDiv'>
            <h1 id='mainHeader'>Looking for similar Songs?</h1>
            <p id='lyricsRequest'>Just give us a song and artist name. We will find songs with a similar mood while you sit back and relax. </p>

            <div className="searchInput">
                <input type="text" name="inputSong" id="inputSong" required spellCheck="false" placeholder='Song Name' onChange={getSongName}></input>
                <input type="text" name="inputArtist" id="inputArtist" required spellCheck="false" placeholder='Artist Name' onChange={getArtistName}></input>
            </div>
            <button id='searchSimilarLyricsButton' name="searchLyrics" onClick={() => sendToFastApi(song_name, artist_name)}>Find Similar Songs</button>
        </div >
    )
}
