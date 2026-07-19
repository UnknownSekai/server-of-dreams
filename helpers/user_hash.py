from typing import Optional


def base9(x: int) -> str:
    return str(x) if x < 9 else (base9(x // 9) + str(x % 9))


sboxes = {
    "0": "187320496",
    "1": "072368941",
    "2": "724396108",
    "3": "274619083",
    "4": "743901826",
    "6": "102394768",
    "7": "082416793",
    "8": "842309716",
    "9": "923864701",
}

sboxes_rev = {
    key: {digit: str(i) for i, digit in enumerate(value)}
    for key, value in sboxes.items()
}

paddings = {
    "0": ("19875", "520"),
    "1": ("37805", "592"),
    "2": ("02415", "593"),
    "3": ("67215", "548"),
    "4": ("74685", "523"),
    "6": ("80725", "549"),
    "7": ("82305", "541"),
    "8": ("31685", "592"),
    "9": ("82635", "574"),
}


def hash_id(user_id: int) -> str:
    sbox_idx = "691082374"[(user_id % 100) % 9]
    sbox = sboxes[sbox_idx]
    pleft, pright = paddings[sbox_idx]
    inner = sbox_idx + "".join([sbox[int(digit)] for digit in base9(user_id)])
    plen = 10 - len(inner)
    if plen > 0:
        right = (plen + (plen <= 2) - 1) // 2
        return pleft[right - plen :] + inner + pright[:right]
    return inner


def unhash_id(hashed_id: str) -> Optional[int]:
    if len(hashed_id) < 10:
        return None
    hashed_id_ori = hashed_id
    parts = hashed_id.split("5")
    if len(parts) > 3:
        return None
    hashed_id = parts[bool(len(parts) - 1)]
    if not hashed_id or hashed_id[0] not in sboxes_rev:
        return None
    sbox_rev = sboxes_rev[hashed_id[0]]
    try:
        user_id = int("".join(sbox_rev[c] for c in hashed_id[1:]), 9)
    except (KeyError, ValueError):
        return None
    if hash_id(user_id) != hashed_id_ori:
        return None
    return user_id
