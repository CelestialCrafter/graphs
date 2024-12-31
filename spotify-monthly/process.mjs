import fs from "fs";
import path from "path";
import SpotifyWebApi from "spotify-web-api-node";

// data
const pastMonthTracks = (year, month) =>
  plays.filter((track) => {
    const date = new Date(track.ts);
    if (date.getFullYear() != year) return false;

    const max = new Date(year, month, 0);
    const min = max - 1000 * 60 * 60 * 24 * 30;

    return date >= min && date <= max;
  });

const unique = (arr, key) => {
  const seen = {};
  return arr.filter((item) => {
    if (!seen[item[key]]) {
      seen[item[key]] = true;
      return true;
    }

    return false;
  });
};

const sortByPlays = (plays) => {
  const counts = plays.reduce((acc, x) => {
    const uri = x.spotify_track_uri;
    if (!(uri in acc)) acc[uri] = 0;
    acc[uri]++;
    return acc;
  }, {});

  return unique(plays, "spotify_track_uri")
    .map((track) => ({ ...track, count: counts[track.spotify_track_uri] }))
    .toSorted(
      (a, b) => counts[b.spotify_track_uri] - counts[a.spotify_track_uri],
    );
};

// auth
const spotifyClient = new SpotifyWebApi({
  clientId: "",
  clientSecret: "",
  redirectUri: "",
});

//console.log(
//  spotifyClient.createAuthorizeURL(
//    ["playlist-modify-public", "playlist-modify-private"],
//    "abcdefghijklmnopqrstuvwxyz",
//  ),
//);

//const code =
//  "";
//const token = await spotifyClient.authorizationCodeGrant(code);
//console.log(token.body.access_token);

spotifyClient.setAccessToken("");

// spotify api
const createPlaylist = async (year, month, tracks) => {
  const date = new Date(year, month, 0);
  const m = date.toLocaleString("default", { month: "long" }).toLowerCase();
  const playlist = await spotifyClient.createPlaylist(`${m}`, {
    description: "",
  });
  await spotifyClient.addTracksToPlaylist(playlist.body.id, tracks);
};

// exec
const basePath = "data/";
const files = fs.readdirSync(basePath).map((file) => path.join(basePath, file));
const plays = files.map((path) => JSON.parse(fs.readFileSync(path))).flat();

const year = 2022;
for (let month = 1; month < 12 + 1; month++) {
  const uris = sortByPlays(
    pastMonthTracks(year, month)
      .filter((play) => play.ms_played > 30 * 1000)
      .filter((play) => play.spotify_track_uri),
  )
    .slice(0, 50)
    .map((track) => track.spotify_track_uri);

  await createPlaylist(year, month, uris);
  await new Promise((res) => setTimeout(res, 2000));
}
