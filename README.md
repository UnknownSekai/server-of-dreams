# Server of Dreams (夢のサーバー)
A certain EOSed mobile theatre idol rhythm game's WIP private server implementation.

## Server setup (do once)

Note: these instructions are made for Linux and aren't tested for other OS. Since this is a python server,
it is possible to run it on Windows and MacOS, but those instructions doesn't cover them.

### Requirements

- Docker
- Python (with pip)
- mitmproxy (optional but strongly recommended)

### Config

First, make a copy of the `config.example.yml` file named `config.yml` and fill it.

### Database setup

Note: Docker commands may require "sudo" rights.

```bash
docker run --name soddb \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=server_of_dreams \
  -p 5432:5432 \
  -v sod_volume:/var/lib/postgresql \
  -d postgres:18
```

### Python venv setup

The following commands will setup a new python venv (virtual environment for python), install the requirements dependencies, then download assets:
```bash
python -m venv venv    # makes a new venv for this project
source venv/bin/activate    # activates it in your current terminal
pip install -r requirements.txt
python -m scripts.database_setup
python -m scripts.download_masterdata
python -m scripts.download_all_assets   # https://github.com/Ryota537/asset-of-dreams
```

Note: python commands are executed in the venv as long as the terminal is opened.
Type `source venv/bin/activate` to access it again on a new terminal.

### Certificates

You need to generate certificates for the realtime server (coop, friends, circle features).

For this, use one of the two methods listed below.

#### Generator script (automatic)
First, make sure to fill the realtime part properly in the config.yml file.
Then, you can simply run the generator script (make sure you're still in the venv first!):

```bash
python -m scripts.generate_realtime_cert
```

#### Openssl (manual)
You can also generate them manually if you want to.
Replace the two "REPLACEME" with your domain for realtime or your local network IP:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -sha256 \
  -keyout certs/realtime-key.pem -out certs/realtime-cert.pem -days 365 \
  -subj "/CN=REPLACEME" \
  -addext "subjectAltName=DNS:REPLACEME,DNS:localhost,IP:127.0.0.1"
```

## Run

### Start

Note: Docker commands may require "sudo" rights.

```bash
docker container start soddb
source venv/bin/activate
python main.py
```

Start mitmproxy (if needed)

```bash
mitmproxy -s mitm_redirect_sirius_to_local.py -p 8888
```

### Stop

- Press Ctrl+C on the server terminal and quit mitmproxy if needed.
- Use `docker container stop soddb` to stop the db, you can delete it after stopping it (with `docker container rm soddb`), but you have to build it again from the server setup step if you do so.

## Changelog
[Changelog](CHANGELOG.md)

## Features
✅ Done · 🚧 WIP · ❌ No

| Feature | | Feature | |
|---|:--:|---|:--:|
| Registration, tutorial & account import | ✅ | Character upgrades (level/awaken/sense/talent) | ✅ |
| Master data & asset serving | ✅ | Star-rank rewards | ✅ |
| Friends & inbox | ✅ | Accessory upgrades | ✅ |
| Gacha (pickup + reroll) | ✅ | Actor side stories | ✅ |
| Live play & scoring | ✅ | Episodes & read rewards | ✅ |
| Live drops (date-windowed) | ✅ | Missions & character missions | ✅ |
| Olivier SP Rate | ✅ | Anthology & auditions | ✅ |
| Stella / Olivier unlocks | ✅ | Comics & theater/MV records | ✅ |
| Song & chart purchases | ✅ | Customization & profile | ✅ |
| Shops & market | ✅ | Photos & albums | ✅ |
| Lessons & music courses | ✅ | Service-end date extension | ✅ |
| Player-rank XP & stamina | ✅ | Daily limit resets | ✅ |
| Music bookmarks | ✅ | **Multiplayer (co-op, circles, Theater League)** | **🚧** |
| Poster (levels/breaks/stories) | ❌ | Login bonuses | ❌ |
| Live events & rankings | ❌ | Mission Pass | ❌ |
| Roulette | ❌ | Flash sale | ❌ |
| Triple-cast parties | ❌ | Banners | ❌ |
| Friend-invitation missions | ❌ | Player rating history | ❌ |
| External payments | ❌ | | |

## Priority Todo
- Player rating history log
- Player rank calculations (live end)
- Senses voice ids (live start)
- Episodes (verify unlocked)
- Missions

## Backburner (less important)
- GET https://lb-api.wds-stellarium.com/api/Circles/Invited -> []
- POST https://lb-api.wds-stellarium.com/api/Home/CheckReceiveLoginBonus
- POST https://lb-api.wds-stellarium.com/api/FriendInvitation/Update (friend invitation mission)

## Help Requested
Please open an issue if you know how!
- Unknown where to find login bonuses or banners (not in master data?)

A lot of game resources may be in downloaded asset bundles? Confirmation would help us a lot :)

## Will Not Implement
POST https://lb-api.wds-stellarium.com/api/Home/CheckEexternalPayment -> no electronic external payments

# Credits
All contributors on this repository, plus...

- [t-wy](https://github.com/t-wy) for user ID hashing
- [wds-sirius/Adv-Resource](https://github.com/wds-sirius/Adv-Resource) for episode data and archive (`_data/episodes/`)
- [assets-of-dreams](https://github.com/Ryota537/asset-of-dreams) for archived game assets
- [Alehero](https://github.com/Alehero/yumesute-preservation-server) for their work on some features
- [ulong32](https://github.com/Alehero/yumesute-preservation-server/issues/1) for figuring out the Olivier SpRate math