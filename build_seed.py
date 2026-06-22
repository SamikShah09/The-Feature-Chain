import json
from pathlib import Path

SONGS = [
    ("Angels", ["Chance the Rapper", "Saba"]),
    ("Everybody's Something", ["Chance the Rapper", "Saba", "BJ the Chicago Kid"]),
    ("Ultralight Beam", ["Kanye West", "Chance the Rapper", "Kelly Price", "The-Dream", "Kirk Franklin"]),
    ("Forever", ["Drake", "Kanye West", "Lil Wayne", "Eminem"]),
    ("Chicago Freestyle", ["Drake", "Giveon"]),

    ("Monster", ["Kanye West", "Jay-Z", "Rick Ross", "Nicki Minaj", "Bon Iver"]),
    ("Mercy", ["Kanye West", "Big Sean", "Pusha T", "2 Chainz"]),
    ("No Church in the Wild", ["Jay-Z", "Kanye West", "Frank Ocean", "The-Dream"]),
    ("Clique", ["Kanye West", "Jay-Z", "Big Sean"]),
    ("Run This Town", ["Jay-Z", "Rihanna", "Kanye West"]),
    ("Otis", ["Jay-Z", "Kanye West"]),
    ("Swagga Like Us", ["Jay-Z", "T.I.", "Kanye West", "Lil Wayne"]),
    ("Renegade", ["Jay-Z", "Eminem"]),
    ("Empire State of Mind", ["Jay-Z", "Alicia Keys"]),
    ("Runaway", ["Kanye West", "Pusha T"]),
    ("All of the Lights", ["Kanye West", "Rihanna", "Kid Cudi"]),
    ("FourFiveSeconds", ["Rihanna", "Kanye West", "Paul McCartney"]),
    ("Champions", ["Kanye West", "Gucci Mane", "Big Sean", "2 Chainz", "Travis Scott", "Yo Gotti", "Quavo", "Desiigner"]),
    ("Birthday Song", ["2 Chainz", "Kanye West"]),

    ("I'm the One", ["DJ Khaled", "Justin Bieber", "Quavo", "Chance the Rapper", "Lil Wayne"]),
    ("No Brainer", ["DJ Khaled", "Justin Bieber", "Chance the Rapper", "Quavo"]),
    ("Wild Thoughts", ["DJ Khaled", "Rihanna", "Bryson Tiller"]),
    ("I'm on One", ["DJ Khaled", "Drake", "Rick Ross", "Lil Wayne"]),
    ("All I Do Is Win", ["DJ Khaled", "T-Pain", "Ludacris", "Snoop Dogg", "Rick Ross"]),
    ("No New Friends", ["DJ Khaled", "Drake", "Rick Ross", "Lil Wayne"]),
    ("POPSTAR", ["DJ Khaled", "Drake"]),
    ("GREECE", ["DJ Khaled", "Drake"]),
    ("Take It to the Head", ["DJ Khaled", "Chris Brown", "Rick Ross", "Nicki Minaj", "Lil Wayne"]),
    ("Top Off", ["DJ Khaled", "Jay-Z", "Future", "Beyonce"]),

    ("Loyalty.", ["Kendrick Lamar", "Rihanna"]),
    ("All The Stars", ["Kendrick Lamar", "SZA"]),
    ("Pray for Me", ["The Weeknd", "Kendrick Lamar"]),
    ("Sidewalks", ["The Weeknd", "Kendrick Lamar"]),
    ("Goosebumps", ["Travis Scott", "Kendrick Lamar"]),
    ("Big Shot", ["Kendrick Lamar", "Travis Scott"]),
    ("Family Ties", ["Baby Keem", "Kendrick Lamar"]),
    ("Range Brothers", ["Baby Keem", "Kendrick Lamar"]),
    ("Control", ["Big Sean", "Kendrick Lamar", "Jay Electronica"]),
    ("Collard Greens", ["ScHoolboy Q", "Kendrick Lamar"]),
    ("Mona Lisa", ["Lil Wayne", "Kendrick Lamar"]),
    ("Forbidden Fruit", ["J. Cole", "Kendrick Lamar"]),
    ("These Walls", ["Kendrick Lamar", "Bilal", "Anna Wise", "Thundercat"]),
    ("Wesley's Theory", ["Kendrick Lamar", "George Clinton", "Thundercat"]),
    ("Mask Off (Remix)", ["Future", "Kendrick Lamar"]),

    ("Sicko Mode", ["Travis Scott", "Drake"]),
    ("Portland", ["Drake", "Quavo", "Travis Scott"]),
    ("Pick Up the Phone", ["Young Thug", "Travis Scott", "Quavo"]),
    ("Watch", ["Travis Scott", "Lil Uzi Vert", "Kanye West"]),
    ("Franchise", ["Travis Scott", "Young Thug", "M.I.A."]),
    ("Beibs in the Trap", ["Travis Scott", "Nav"]),
    ("The London", ["Young Thug", "J. Cole", "Travis Scott"]),
    ("Hot (Remix)", ["Young Thug", "Gunna", "Travis Scott"]),
    ("Bubbly", ["Young Thug", "Drake", "Travis Scott"]),

    ("Jumpman", ["Drake", "Future"]),
    ("Where Ya At", ["Future", "Drake"]),
    ("Low Life", ["Future", "The Weeknd"]),
    ("Life Is Good", ["Future", "Drake"]),
    ("Wait for U", ["Future", "Drake", "Tems"]),
    ("Move That Dope", ["Future", "Pharrell Williams", "Pusha T"]),
    ("Karate Chop (Remix)", ["Future", "Lil Wayne"]),
    ("X", ["21 Savage", "Future"]),
    ("Love Me", ["Lil Wayne", "Drake", "Future"]),

    ("Bad and Boujee", ["Migos", "Lil Uzi Vert"]),
    ("MotorSport", ["Migos", "Nicki Minaj", "Cardi B"]),
    ("Walk It Talk It", ["Migos", "Drake"]),
    ("Congratulations", ["Post Malone", "Quavo"]),
    ("Slippery", ["Migos", "Gucci Mane"]),
    ("I Get the Bag", ["Gucci Mane", "Migos"]),
    ("Rockstar", ["Post Malone", "21 Savage"]),
    ("Psycho", ["Post Malone", "Ty Dolla $ign"]),
    ("Wow (Remix)", ["Post Malone", "Roddy Ricch", "Tyga"]),
    ("Sunflower", ["Post Malone", "Swae Lee"]),

    ("a lot", ["21 Savage", "J. Cole"]),
    ("Mr. Right Now", ["21 Savage", "Drake"]),
    ("Knife Talk", ["Drake", "21 Savage", "Project Pat"]),
    ("Jimmy Cooks", ["Drake", "21 Savage"]),
    ("Rich Flex", ["Drake", "21 Savage"]),
    ("First Person Shooter", ["Drake", "J. Cole"]),
    ("My Life", ["J. Cole", "21 Savage", "Morray"]),
    ("Pride Is the Devil", ["J. Cole", "Lil Baby"]),
    ("Drip Too Hard", ["Lil Baby", "Gunna"]),
    ("Yes Indeed", ["Lil Baby", "Drake"]),
    ("Wants and Needs", ["Drake", "Lil Baby"]),
    ("Never Recover", ["Lil Baby", "Gunna", "Drake"]),
    ("Hurricane", ["Kanye West", "The Weeknd", "Lil Baby"]),
    ("Solid", ["Young Thug", "Gunna", "Drake"]),
    ("Ski", ["Young Thug", "Gunna"]),
    ("Go Crazy", ["Chris Brown", "Young Thug"]),

    ("WAP", ["Cardi B", "Megan Thee Stallion"]),
    ("Hot Girl Summer", ["Megan Thee Stallion", "Nicki Minaj", "Ty Dolla $ign"]),
    ("Savage (Remix)", ["Megan Thee Stallion", "Beyonce"]),
    ("Sweetest Pie", ["Megan Thee Stallion", "Dua Lipa"]),
    ("Finesse (Remix)", ["Bruno Mars", "Cardi B"]),
    ("Bang Bang", ["Jessie J", "Ariana Grande", "Nicki Minaj"]),
    ("Side to Side", ["Ariana Grande", "Nicki Minaj"]),
    ("Truffle Butter", ["Nicki Minaj", "Drake", "Lil Wayne"]),
    ("Moment 4 Life", ["Nicki Minaj", "Drake"]),
    ("No Frauds", ["Nicki Minaj", "Drake", "Lil Wayne"]),
    ("Seeing Green", ["Nicki Minaj", "Drake", "Lil Wayne"]),
    ("Bedrock", ["Lil Wayne", "Drake", "Nicki Minaj", "Tyga", "Gudda Gudda"]),

    ("Lighters", ["Eminem", "Royce da 5'9\"", "Bruno Mars"]),
    ("No Love", ["Eminem", "Lil Wayne"]),
    ("Drop the World", ["Lil Wayne", "Eminem"]),
    ("Smack That", ["Akon", "Eminem"]),
    ("Forgot About Dre", ["Dr. Dre", "Eminem"]),
    ("I Need a Doctor", ["Dr. Dre", "Eminem", "Skylar Grey"]),
    ("Crack a Bottle", ["Eminem", "Dr. Dre", "50 Cent"]),
    ("Patiently Waiting", ["50 Cent", "Eminem"]),
    ("The Next Episode", ["Dr. Dre", "Snoop Dogg", "Kurupt", "Nate Dogg"]),
    ("Still D.R.E.", ["Dr. Dre", "Snoop Dogg"]),
    ("Drop It Like It's Hot", ["Snoop Dogg", "Pharrell Williams"]),
    ("Young, Wild & Free", ["Snoop Dogg", "Wiz Khalifa", "Bruno Mars"]),
    ("See You Again", ["Wiz Khalifa", "Charlie Puth"]),
    ("Sucker for Pain", ["Lil Wayne", "Wiz Khalifa", "Imagine Dragons", "Logic", "Ty Dolla $ign", "X Ambassadors"]),

    ("Erase Me", ["Kid Cudi", "Kanye West"]),
    ("Welcome to Heartbreak", ["Kanye West", "Kid Cudi"]),
    ("Make Her Say", ["Kid Cudi", "Kanye West", "Common"]),
    ("Reborn", ["Kanye West", "Kid Cudi"]),
    ("Pursuit of Happiness", ["Kid Cudi", "MGMT", "Ratatat"]),

    ("Crew Love", ["Drake", "The Weeknd"]),
    ("The Motto", ["Drake", "Lil Wayne"]),
    ("HYFR", ["Drake", "Lil Wayne"]),
    ("She Will", ["Lil Wayne", "Drake"]),
    ("Believe Me", ["Lil Wayne", "Drake"]),
    ("Grindin'", ["Lil Wayne", "Drake"]),
    ("Used To", ["Drake", "Lil Wayne"]),
    ("Pound Cake / Paris Morton Music 2", ["Drake", "Jay-Z"]),
    ("Light Up", ["Drake", "Jay-Z"]),
    ("Work", ["Rihanna", "Drake"]),
    ("Too Good", ["Drake", "Rihanna"]),
    ("What's My Name?", ["Rihanna", "Drake"]),
    ("Take Care", ["Drake", "Rihanna"]),
    ("Umbrella", ["Rihanna", "Jay-Z"]),
    ("Mine", ["Beyonce", "Drake"]),
    ("Loyal", ["Chris Brown", "Lil Wayne", "Tyga"]),

    ("Crazy in Love", ["Beyonce", "Jay-Z"]),
    ("Deja Vu", ["Beyonce", "Jay-Z"]),

    ("No Problem", ["Chance the Rapper", "Lil Wayne", "2 Chainz"]),
    ("Cocoa Butter Kisses", ["Chance the Rapper", "Vic Mensa", "Twista"]),
    ("No Lie", ["2 Chainz", "Drake"]),
    ("Feds Watching", ["2 Chainz", "Pharrell Williams"]),
    ("Blessings", ["Big Sean", "Drake", "Kanye West"]),
    ("Beware", ["Big Sean", "Lil Wayne", "Jhene Aiko"]),
    ("I Know", ["Big Sean", "Jhene Aiko"]),
    ("Sativa", ["Jhene Aiko", "Swae Lee"]),

    ("Black Beatles", ["Rae Sremmurd", "Gucci Mane"]),
    ("Unforgettable", ["French Montana", "Swae Lee"]),
    ("Powerglide", ["Rae Sremmurd", "Juicy J"]),
    ("Wake Up in the Sky", ["Gucci Mane", "Bruno Mars", "Kodak Black"]),
    ("Stay Schemin", ["Rick Ross", "Drake", "French Montana"]),
    ("Pop That", ["French Montana", "Rick Ross", "Drake", "Lil Wayne"]),
    ("Diced Pineapples", ["Rick Ross", "Wale", "Drake"]),
    ("Aston Martin Music", ["Rick Ross", "Drake", "Chrisette Michele"]),

    ("Get Lucky", ["Daft Punk", "Pharrell Williams"]),
    ("Blurred Lines", ["Robin Thicke", "T.I.", "Pharrell Williams"]),
    ("Live Your Life", ["T.I.", "Rihanna"]),
    ("Uptown Funk", ["Mark Ronson", "Bruno Mars"]),
]


def normalize_artist(name: str) -> str:
    return name.strip()


def main():
    seen = {}
    songs_out = []
    for title, artists in SONGS:
        artists = [normalize_artist(a) for a in artists]
        artists = list(dict.fromkeys(artists))
        songs_out.append({"title": title, "artists": artists})
        for a in artists:
            seen[a] = seen.get(a, 0) + 1

    data = {"version": 1, "songs": songs_out}
    out = Path(__file__).with_name("data.json")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Wrote {out} : {len(songs_out)} songs, {len(seen)} unique artists")


if __name__ == "__main__":
    main()
