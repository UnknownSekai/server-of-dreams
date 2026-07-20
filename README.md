# Server of Dreams (夢のサーバー)
A certain EOSing mobile theatre idol rhythm game's private server implementation.

## Run

Fill out config

Needs a postgresql database

```bash
pip install -r requirements.txt
python -m scripts.database_setup
python -m scripts.download_masterdata
python -m scripts.download_asset_catalogs
python main.py
```

## Roadmap
2026/07/17 - EOS announced (RIP)

2026/07/17 - Development begins

2026/07/18 - Masterdata/assets routes implemented

2026/07/18 - Account registration and tutorial implemented

2026/07/18 - Basic friends system implemented

2026/07/18 - Game hints and splash read statuses implemented

2026/07/19 - Inbox receive/bulk receive implemented

2026/07/19 - Live start and stamina

2026/07/19 - Live end, drops, ratings, clear lamps

2026/07/19 - Episodes (and read rewards)

## Priority Todo
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
- Unknown where to find max autoPlayTimes, dailyLessonTimes, or musicCourseFreeChallengeTimes (we default to all 0 for now).
- Unknown where to find login bonuses or banners (not in master data?)

A lot of game resources may be in downloaded asset bundles? Confirmation would help us a lot :)

## Will Not Implement
POST https://lb-api.wds-stellarium.com/api/Home/CheckEexternalPayment -> no electronic external payments

# Credits
- [t-wy](https://github.com/t-wy) for user ID hashing
- [wds-sirius/Adv-Resource](https://github.com/wds-sirius/Adv-Resource) for episode data and archive (`_data/episodes/`)