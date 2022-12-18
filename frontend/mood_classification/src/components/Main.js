import React from 'react'

export default function Main() {
    return (
        <div id='mainDiv'>
            <h1 id='mainHeader'>Looking for similar Songs?</h1>
            <p id='lyricsRequest'>Just give us a song and artist name. We will find songs with a similar mood while you sit back and relax. </p>

            <div class="searchInput">
                <input type="text" name="inputSong" id="inputSong" required spellcheck="false" placeholder='Song Name'></input>
                <input type="text" name="inputArtist" id="inputArtist" required spellcheck="false" placeholder='Artist Name'></input>
            </div>
            <button id='searchSimilarLyricsButton' name="searchLyrics">Find Similar Songs</button>
        </div >
    )
}
