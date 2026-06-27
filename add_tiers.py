import json, sys
from pathlib import Path

TIER_250 = [
    "Drake","Eminem","Kanye West","JAY\u2010Z","Lil Wayne","Kendrick Lamar","Snoop Dogg","Dr. Dre",
    "J. Cole","2Pac","The Notorious B.I.G.","Nas","50 Cent","Travis Scott","Future","Nicki Minaj",
    "Cardi B","Post Malone","Lil Baby","21 Savage","The Weeknd","Rihanna","Beyonc\xe9","Ariana Grande",
    "Justin Bieber","Ed Sheeran","Dua Lipa","Billie Eilish","Taylor Swift","Bruno Mars","SZA",
    "Juice WRLD","Young Thug","Gunna","Migos","Quavo","2 Chainz","Big Sean","A$AP Rocky",
    "Chris Brown","Lil Uzi Vert","Doja Cat","Jack Harlow","Polo G","Lil Durk","DaBaby",
    "Pop Smoke","Roddy Ricch","Kodak Black","Wiz Khalifa","Mac Miller","Chance the Rapper",
    "Kid Cudi","Childish Gambino","Tyler, The Creator","Logic","G-Eazy","Meek Mill","Rick Ross",
    "French Montana","DJ Khaled","Ty Dolla $ign","Swae Lee","Wale","ScHoolboy Q","Jh\xe9n\xe9 Aiko",
    "Bryson Tiller","Summer Walker","Metro Boomin","Lil Tecca","Trippie Redd",
    "YoungBoy Never Broke Again","Kevin Gates","Fetty Wap","Megan Thee Stallion","Bad Bunny",
    "Karol G","J Balvin","Daddy Yankee","Ozuna","T.I.","Ludacris","Busta Rhymes","Fat Joe",
    "Jadakiss","Fabolous","The Game","Gucci Mane","Jeezy","Akon","Justin Timberlake",
    "Lady Gaga","Alicia Keys","John Legend","Frank Ocean","Anderson .Paak","Pusha T",
    "Playboi Carti","Lil Yachty","Offset","Dave East","Nipsey Hussle","YG","Yo Gotti",
    "Trey Songz","Pharrell Williams","Swizz Beatz","Missy Elliott","DMX","Ice Cube",
    "Andr\xe9 3000","Action Bronson","Joey Bada$$","Saba","Giveon","Tems","Lil Tjay","Rod Wave",
    "Fivio Foreign","Wizkid","Burna Boy","Davido","Sexyy Red","GloRilla","Coi Leray",
    "PnB Rock","NLE Choppa","PARTYNEXTDOOR","Jeremih","Don Toliver","Moneybagg Yo",
    "24kGoldn","Khalid","H.E.R.","Benny the Butcher","Freddie Gibbs","Raekwon","Method Man",
    "Redman","Bun B","Cam'ron","Lloyd Banks","LL Cool J","Timbaland","Ghostface Killah",
    "Common","Talib Kweli","Jay Rock","Ab\u2010Soul","Isaiah Rashad","Jidenna","SiR","Miguel",
    "6LACK","Brent Faiyaz","Lucky Daye","Ari Lennox","Baby Keem","Blxst","dvsn",
    "Fredo Bang","Boosie Badazz","Lil Kim","Eve","Ice T","Big Pun","Diplo","Major Lazer",
    "DJ Snake","Sean Paul","Popcaan","Vybz Kartel","Shenseea","6ix9ine","mgk",
    "A Boogie wit da Hoodie","Blueface","NF","Lil Skies","G Herbo","Stunna 4 Vegas",
    "GloRilla","Sexyy Red","Coi Leray","Fivio Foreign","Morray","Giveon","Brent Faiyaz",
]

TIER_500_EXTRA = [
    "E\u201040","Too $hort","Birdman","Slim Thug","Paul Wall","Chamillionaire",
    "Lil Flip","UGK","Pimp C","Three 6 Mafia","DJ Paul","Juicy J","Project Pat",
    "Trae","Z-Ro","Scarface","Geto Boys","Master P","Juvenile","BG","Turk",
    "Rich Homie Quan","Rae Sremmurd","iLoveMakonnen","Clipse","Westside Gunn",
    "Conway the Machine","Flee Lord","Ransom","38 Spesh","Meyhem Lauren","Roc Marciano",
    "billy woods","Elucid","Navy Blue","Wiki","Skyzoo","Smoke DZA","Vado","Papoose","Max B",
    "Jay Critch","Ron Suno","Michael Christmas","Kemba","Open Mike Eagle","Oddisee","Locksmith",
    "T-Pain","Ryan Leslie","Ne-Yo","Musiq Soulchild","Anthony Hamilton","Joe","Jaheim",
    "Case","Mario","Ginuwine","Keith Sweat","Jodeci","Bobby Brown","Ralph Tresvant",
    "Johnny Gill","Babyface","Teddy Riley","Aaron Hall","L.A. Reid","Jimmy Jam","Terry Lewis",
    "H.E.R.","Snoh Aalegra","Lucky Daye","Kiana Led\xe9","Victoria Mon\xe9t","Chloe Bailey",
    "Halle Bailey","Normani","Kehlani","Kali Uchis","Bia","Flo Milli","City Girls","Latto",
    "Asian Doll","Gloss Up","Blac Youngsta","42 Dugg","Rylo Rodriguez","Sleepy Hallow",
    "Calboy","Comethazine","Smokepurpp","Ski Mask the Slump God","XXXTentacion",
    "Craig Xen","Pouya","Night Lovell","Ghostemane","Bones","Ramirez","Chris Crack",
    "Tech N9ne","Krizz Kaliko","Yelawolf","Machine Gun Kelly","Rittz","Futuristic",
    "Chris Webby","Token","Classified","Madlib","J Dilla","Statik Selektah","DJ Premier",
    "Pete Rock","Large Professor","Lord Finesse","Buckwild","DJ Drama","DJ Envy",
    "Royce da 5\u20199\u2033","Joell Ortiz","KXNG Crooked","Slaughterhouse","38 Spesh",
    "Mick Jenkins","Noname","Ravyn Lenae","Smino","Amin\xe9","theMIND","Eryn Allen Kane",
    "Little Brother","Phonte","Black Thought","Mos Def","Queen Latifah","Lauryn Hill",
    "Erykah Badu","D'Angelo","Missy Elliott","Eve","Lil Kim","DMX","Ice Cube","Ice T",
    "Andr\xe9 3000","Big Pun","Cam'ron","Lloyd Banks","LL Cool J","Ghostface Killah",
]

TIER_500 = list(dict.fromkeys(TIER_250 + TIER_500_EXTRA))


def main():
    data_path = Path("data.json")
    if not data_path.exists():
        sys.exit("data.json not found. Run from the project directory.")

    data = json.loads(data_path.read_text(encoding="utf-8"))
    in_dataset = set()
    for s in data.get("songs", []):
        in_dataset.update(s.get("artists", []))

    t250_missing = [a for a in TIER_250 if a not in in_dataset]
    t500_missing = [a for a in TIER_500 if a not in in_dataset]

    print(f"Dataset: {len(data['songs'])} songs, {len(in_dataset)} artists")
    print()
    print(f"TIER_250 ({len(TIER_250)} names)  — missing from dataset: {len(t250_missing)}")
    if t250_missing:
        for a in t250_missing:
            print(f"  - {a}")
    else:
        print("  All present ✓")
    print()
    print(f"TIER_500 ({len(TIER_500)} names)  — missing from dataset: {len(t500_missing)}")
    if t500_missing:
        for a in t500_missing:
            print(f"  - {a}")
    else:
        print("  All present ✓")
    print()

    if not (t250_missing or t500_missing):
        print("Nothing to add.")
        return

    print("To add missing artists, run build_dataset.py with those names as seeds:")
    missing_seed = ",".join(set(t250_missing + t500_missing))
    print(f'  python3 build_dataset.py --seed "{missing_seed}" --expand --max-artists 100 \\')
    print(f'    --user-agent "FeatureLine/1.0 ( you@example.com )"')
    print()
    print("That will pull their songs from MusicBrainz and merge them into data.json.")
    print("Then run rebuild.py to bake the new data into index.html.")


if __name__ == "__main__":
    main()
