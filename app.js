const songsDiv = document.getElementById("songs");
let votes = JSON.parse(localStorage.getItem("votes")) || {};

async function fetchSongs(playlistId) {
    const res = await fetch(`http://127.0.0.1:5000/playlist/${playlistId}`);
    return await res.json();
}

async function renderSongs(ranking=false) {
    const songs = await fetchSongs("4PcEEEqnkE4FA7AhZ2k5rV?si=27268732007844e3");
    
    // 投票数初期化
    songs.forEach(song => {
        if (!(song.name in votes)) votes[song.name] = 0;
    });

    if (ranking) {
        songs.sort((a,b) => votes[b.name]-votes[a.name]);
    }

    songsDiv.innerHTML = "";
    songs.forEach(song => {
        const div = document.createElement("div");
        div.className = "song";
        div.innerHTML = `
            <h3>${song.name}</h3>
            <img src="${song.img}" alt="${song.name}">
            <p>投票数: ${votes[song.name]}</p>
            <button onclick="vote('${song.name}')">投票する</button>
            <iframe style="border-radius:12px" src="${song.embed}" width="100%" height="80" frameBorder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
        `;
        songsDiv.appendChild(div);
    });

    localStorage.setItem("votes", JSON.stringify(votes));
}

function vote(name) {
    votes[name]++;
    renderSongs();
}

// 初期描画
renderSongs();
