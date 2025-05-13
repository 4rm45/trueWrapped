import json
from collections import defaultdict
import glob

# Lue tiedostot
files = glob.glob("Spotify Extended Streaming History/Streaming_History_Audio_*.json")

# Luo sanakirja, jossa avaimina ovat kappaleet ja arvoina striimauksen kesto
streaming_data = defaultdict(int)
play_count = defaultdict(int)

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            artist = item.get('master_metadata_album_artist_name')
            track = item.get('master_metadata_track_name')
            if artist and track:  # Tarkista, että artisti ja kappale eivät ole None tai tyhjiä
                key = (artist, track)
                streaming_data[key] += item['ms_played']
                play_count[key] += 1

# Järjestä sanakirja striimauksen keston mukaan
sorted_streaming_data = sorted(streaming_data.items(), key=lambda x: x[1], reverse=True)

# Muunna millisekunnit ihmisen luettavaan muotoon
def ms_to_human_readable(ms):
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    human_readable = []
    if days > 0:
        human_readable.append(f"{days} days")
    if hours > 0:
        human_readable.append(f"{hours} hours")
    if minutes > 0:
        human_readable.append(f"{minutes} minutes")
    if seconds > 0:
        human_readable.append(f"{seconds} seconds")

    return ', '.join(human_readable)

# Avaa tiedosto kirjoittamista varten
with open('output.html', 'w', encoding='utf-8') as f:
    # Aloita HTML-dokumentti
    f.write("<html>\n")
    f.write("<head>\n")
    f.write("<style>\n")
    f.write("table { width: 100%; border-collapse: collapse; }\n")
    f.write("tr:nth-child(even) { background-color: #f2f2f2; }\n")
    f.write("th, td { padding: 8px; text-align: left; }\n")
    f.write("</style>\n")
    f.write("</head>\n")
    f.write("<body>\n")

    # Aloita taulukko
    f.write("<table>\n")

    # Tulosta otsikkorivi
    f.write("<tr><th>Streamed for</th><th>Played times</th><th>Artist</th><th>Track</th></tr>\n")

    # Tulosta jokainen rivi
    for (artist, track), msPlayed in sorted_streaming_data:
        f.write("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n".format(ms_to_human_readable(msPlayed), play_count[(artist, track)], artist, track))

    # Lopeta taulukko
    f.write("</table>\n")

    # Lopeta HTML-dokumentti
    f.write("</body>\n")
    f.write("</html>\n")