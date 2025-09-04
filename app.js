const songsDiv = document.getElementById("songs");
let songs = [];
let votes = {};

fetch("http://127.0.0.1:5000/songs")
  .then(res => res.json())
  .then(data => {
    songs = data;
    votes = JSON.parse(localStorage.getItem("votes")) || {};
    songs.forEach(song => { if (!(song.name in votes)) votes[song.name] = 0; });
    renderSongs(false);
  })
  .catch(err => console.error("JSON取得エラー:", err));

function renderSongs(rank=false) {
  songsDiv.innerHTML = "";
  const displaySongs = rank
    ? [...songs].sort((a,b) => votes[b.name] - votes[a.name])
    : songs;

  displaySongs.forEach(song => {
    const div = document.createElement("div");
    div.className = "song";
    div.innerHTML = `
      <h3>${song.name}</h3>
      <img src="${song.img}" alt="${song.name}">
      <p>投票数: ${votes[song.name]}</p>
      <button onclick="vote('${song.name}')">投票する</button>
      ${song.embed ? `<iframe style="border-radius:12px" src="${song.embed}" width="100%" height="80" frameBorder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>` : ""}
    `;
    songsDiv.appendChild(div);
  });
}

function vote(songName) {
  votes[songName]++;
  localStorage.setItem("votes", JSON.stringify(votes));
  renderSongs();
}
