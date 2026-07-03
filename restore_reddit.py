#!/usr/bin/env python3
"""Restore Reddit sheet rows 2-8 and move music entries to rows 17-21."""

from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1XVkN3dyk1Xj-UNFj2kVRMe8APBDNTlCj2oY9car8Xzk"
SHEET = "Reddit "  # trailing space is actual tab name

# Column indices (0-based): A=0 B=1 C=2 D=3 E=4 F=5 G=6
A, B, C, D, F, G = 0, 1, 2, 3, 5, 6


def get_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def col_letter(idx):
    result = ""
    while True:
        result = chr(ord("A") + idx % 26) + result
        idx = idx // 26 - 1
        if idx < 0:
            break
    return result


def cell(col, row):
    return f"'{SHEET}'!{col_letter(col)}{row}"


def make_update(col, row, value):
    return {"range": cell(col, row), "values": [[value]]}


def get_sheet_id(service):
    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    for s in meta["sheets"]:
        if s["properties"]["title"] == SHEET:
            return s["properties"]["sheetId"]


def format_rows(service, sid, start_row, end_row):
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"requests": [{
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": start_row - 1, "endRowIndex": end_row},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"fontFamily": "Calibri", "fontSize": 10},
                    "wrapStrategy": "WRAP",
                }},
                "fields": "userEnteredFormat(textFormat,wrapStrategy)",
            }
        }]},
    ).execute()


def main():
    service = get_service()
    ss = service.spreadsheets()
    sid = get_sheet_id(service)

    updates = []

    # --- RESTORE ROWS 2-8 (old data) ---

    # Row 2 — National Park Trust post (29/06/26)
    updates += [
        make_update(A, 2, "29/06/26"),
        make_update(C, 2, """Has anyone volunteered with National Park Trust?

I'm 22M and I'm doing a small road trip with my dad in a few weeks. Nothing too fancy, honestly. It started as one of those "we should do something before life gets busy again" ideas and somehow turned into a rough PA/Maryland/DC route.

Right now the loose plan is Gettysburg, then Monocacy National Battlefield, then staying somewhere around Rockville/DC for a few days before heading back. My dad is very into Civil War/history stuff, and I'm more into the outdoors side of it, so Monocacy seemed like a good middle ground for both of us.

While looking up things around the area, I came across National Park Trust. From what I understand, they've been involved with park preservation stuff, including places in Maryland, and they're based in Rockville. I found this page while searching around:

https://donaroo.org/nonprofits/national-park-trust-rockville-md-521691924

I'm not really looking to just donate and move on. Since we'll already be around Rockville for a couple days, we were thinking it might be nice to actually volunteer or help with something if there's a real opportunity. Even something small like a cleanup, event help, park stewardship thing, or anything where we can be useful for a day or two.

Also, selfishly, it would be nice to meet people while we're there. Road trips with your dad are great, but after three straight hours of him explaining battlefield tactics in the car, I might need to talk to other humans lol.

Has anyone here actually volunteered with National Park Trust, or done anything connected to them around Maryland/Rockville? Are they active with in-person opportunities, or is it mostly donations and programs from a distance?

Would really appreciate any honest firsthand experiences before I reach out."""),
        make_update(F, 2, "https://www.reddit.com/r/NationalPark/s/4S9DuDCQX5"),
    ]

    # Row 3 — Durham / Hope Project post (29/06/26)
    updates += [
        make_update(A, 3, "29/06/26"),
        make_update(C, 3, """Going to be in Durham for a bit, has anyone worked with The Hope Project / ReCity Network?

I'm going to be in Durham for a little while soon and I've been trying to figure out something useful to do there besides just eating, walking around, and pretending I know the difference between all the coffee shops.

Long story short, I'm helping a friend/cousin with some moving stuff in the Triangle area, and my schedule is going to be weird. Some days I'll be free for half the day, some days not at all. So I started looking up local nonprofits or community spaces where maybe I could help out for a couple days, meet people, and not just sit around scrolling in a hotel room or Airbnb.

I came across The Hope Project Live Love Serve Inc., which seems connected with ReCity Network in Durham. From what I can tell, it's not exactly a normal "show up and pack boxes for two hours" type of nonprofit. It looks more like a hub or support space for other nonprofits and mission-driven groups.

This is the listing I found:

https://donaroo.org/nonprofits/the-hope-project-live-love-serve-inc-durham-nc-800402656

I'm curious if anyone here has interacted with them in real life. Volunteered there, attended an event, worked out of the space, partnered with them, or even just knows people involved. I'm interested in knowing whether there are actual ways to show up and help, even if it's event support, admin help, community stuff, or getting connected to one of the organizations around them. Also, since I won't know many people in Durham, part of the appeal is honestly just being around people doing something meaningful instead of wandering around alone and overthinking where to eat dinner. Has anyone had experience with them? Good place to start, or should I look at other Durham volunteer groups first?"""),
        make_update(F, 3, "https://www.reddit.com/r/bullcity/s/1ATRVJBHCo"),
    ]

    # Row 4 — Removed (29/06/26)
    updates += [
        make_update(A, 4, "29/06/26"),
    ]

    # Row 5 — Winston-Salem link only (29/06/26)
    updates += [
        make_update(A, 5, "29/06/26"),
        make_update(F, 5, "https://www.reddit.com/r/winstonsalem/s/zJuXykGXdl"),
    ]

    # Row 6 — Patriot Point post (30/06/26)
    updates += [
        make_update(A, 6, "30/06/26"),
        make_update(B, 6, "anyone here know Patriot Point near Cambridge?"),
        make_update(C, 6, """random but has anyone here volunteered at Patriot Point before?

I was looking up some Eastern Shore volunteer stuff and found them through Donaroo. Hadnt heard of it before but it seems like a retreat place for veterans / military families, somewhere near Cambridge from what I understood.

The one I saw was this watersports volunteer thing:

https://donaroo.org/volunteer/dc/washington/guide-guests-in-watersports-activities-patriotpoint-org

I'm not military or anything, I just like being around water and thought it could be a decent way to help without doing the usual boring volunteer event where everyone stands around confused.

But I also dont wanna reach out if they need actual certified kayak guides or lifeguards. I'm comfortable around water but not a professional.

Anyone local know the place or volunteered there? Is it organized / normal people can help, or mostly people already connected to veteran orgs?"""),
        make_update(F, 6, "https://www.reddit.com/r/easternshoremd/s/DGECuL7VYz"),
    ]

    # Row 7 — Annapolis comment (30/06/26)
    updates += [
        make_update(A, 7, "30/06/26"),
        make_update(B, 7, "Volunteering in Annapolis"),
        make_update(D, 7, """Patriot Point might be worth checking out if you're okay with something a little outside Annapolis.

I found them while looking through Donaroo for volunteer stuff. Seems like a veteran retreat place on the Eastern Shore and one of the roles was helping with meals during retreats.

I havent done it myself yet so dont want to oversell it, but it sounded more useful than the usual volunteer thing where 20 people show up and nobody knows what to do with them. Food / setup / basic hospitality actually seems needed.

Could be a decent service day type thing, especially if you're looking for something community related but not just the same few local orgs everyone mentions."""),
        make_update(G, 7, "https://www.reddit.com/r/Annapolis/comments/1ns8zlt/comment/ouvvzn0/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"),
    ]

    # Row 8 — Adaptive Kayaking comment (30/06/26)
    updates += [
        make_update(A, 8, "30/06/26"),
        make_update(B, 8, "Adaptive Kayaking - Awareness"),
        make_update(G, 8, "https://www.reddit.com/r/Kayaking/comments/1krdprk/comment/ouvv7i1/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"),
    ]

    # --- MUSIC ENTRIES — append at rows 17-21 ---

    # Row 17 — Music & mental health comment
    updates += [
        make_update(A, 17, "03/07/26"),
        make_update(D, 17, """Yeah I get what you mean. I don't think music "controls" you or anything, but if you keep feeding your brain the same mood every day, it probably does start shaping the way you react to people.

Some songs are good for one moment, like the gym, driving, partying, getting hyped, whatever. But if the whole soundtrack around you is anger, numbness, ego, paranoia, revenge, sex, flexing, or not caring about anyone, I can see how that slowly becomes the emotional weather you live in. Not because the artist forced you to be that way, but because you're rehearsing that state over and over.

I've been thinking about this more because I came across HeartSupport while browsing mental health nonprofits on Donaroo. They're connected to music communities and talk a lot about how people use music to cope with depression, addiction, anxiety, self-harm, loneliness and stuff like that. It made me think that music can either help people process what they're feeling, or it can keep them stuck inside the same loop. For me the real question is probably: after I listen to this song a lot, do I become more honest, more calm, more alive, more connected, or do I become more defensive, cold, angry, or careless?"""),
        make_update(G, 17, "https://www.reddit.com/r/Music/comments/1lxnqjy/music_and_mental_health/"),
    ]

    # Row 18 — EDM production comment
    updates += [
        make_update(A, 18, "03/07/26"),
        make_update(D, 18, """This is such a good thread. Producing music can be weirdly therapeutic because it gives anxiety, grief, anger, loneliness, or whatever else somewhere to go instead of just sitting in your head.

One resource that fits this topic is HeartSupport. They're a nonprofit built around music fans and mental health support. From what I've seen, they connect people through shared music taste and peer support, which makes sense because sometimes it's easier to open up with people who already "get" the kind of music/community you're part of.

I came across HeartSupport while browsing mental health nonprofits on Donaroo: https://donaroo.org/nonprofits/heartsupport-inc-round-rock-tx-464342239

Thought they were very relevant to the idea that music can be medicine. Not in the sense that music replaces therapy or professional help, but in the sense that music communities can become a bridge toward actually talking about what you're going through.

For producers especially, I think that matters. Making music can be healing, but it can also get lonely, obsessive, or emotionally heavy if you're only processing everything alone in a DAW."""),
        make_update(G, 18, "https://www.reddit.com/r/edmproduction/comments/ztpb4c/music_is_medicine_please_share_your_music_mental/"),
    ]

    # Row 19 — Artist mental health comment
    updates += [
        make_update(A, 19, "03/07/26"),
        make_update(D, 19, """Honestly, the biggest thing would be something that understands the lifestyle instead of giving generic wellness advice.

Musicians need support that works around irregular schedules, touring, late nights, financial instability, rejection, burnout, substance pressure, identity being tied to art, and the weird loneliness of being around people all the time but still feeling isolated. A normal "book weekly therapy at 2pm every Tuesday" setup isn't always realistic for artists.

I'd want a program that has:
- low-cost or free support
- peer groups with other musicians
- help during touring/burnout periods
- substance use support without judgment
- someone to talk to after shows or during emotional crashes
- resources for partners/families too
- actual follow-up, not just a one-time workshop

HeartSupport comes to mind as one example of the kind of model that makes sense. They're built around music fans and mental health, and they use music/community as the entry point instead of treating music like an unrelated hobby. I came across HeartSupport on Donaroo here: https://donaroo.org/nonprofits/heartsupport-inc-round-rock-tx-464342239

To me, the best artist mental health program would not just say "take care of yourself." It would understand that the music life itself creates specific pressures, and the support has to be built around that reality."""),
        make_update(G, 19, "https://www.reddit.com/r/Music/comments/119zaya/as_an_artist_what_would_you_want_from_a_mental/"),
    ]

    # Row 20 — Metalcore post
    updates += [
        make_update(A, 20, "03/07/26"),
        make_update(B, 20, "Any metalcore people here into mental health/community support work?"),
        make_update(C, 20, """Hey, I'm a 22F. I've been getting more involved in mental health/community support work, and I wanted to ask if anyone here is in that world too.

I'm asking in this sub because metalcore people usually understand the mental health side of music without needing it explained. I'm especially interested in connecting with people who have volunteered, joined support spaces, done peer support, worked with music-related mental health communities; for context, I've been around HeartSupport-type spaces and found their Donaroo page here while looking through related nonprofit/community resources: https://donaroo.org/nonprofits/heartsupport-inc-round-rock-tx-464342239

I'm just curious to know if anyone here is involved in similar work or knows other metalcore / hardcore / alternative people doing mental health support."""),
        make_update(F, 20, "https://www.reddit.com/r/Metalcore/"),
    ]

    # Row 21 — Screamo post
    updates += [
        make_update(A, 21, "03/07/26"),
        make_update(B, 21, "does anyone here do scene/community care stuff?"),
        make_update(C, 21, """hey, i'm 22f. random question but does anyone here do any kind of community care / peer support / diy mutual aid type stuff around music scenes?

i'm asking here because screamo/skramz feels like one of the few scenes where the whole point is emotional honesty without making it clean or inspirational. like it's not "wellness" music lol. it's more like people screaming through grief, shame, panic, breakups, loneliness, family stuff, whatever.

i've been getting more involved in mental health/community support work and i'm trying to find people who approach it from more of a diy scene angle, not corporate self-care language. stuff like checking in on people at shows, sober support, harm reduction, mutual aid, grief support, peer groups, zines/resources, anything like that.

for context, these are a few music/mental health/community resources i've been looking at:

HeartSupport on Donaroo: https://donaroo.org/nonprofits/heartsupport-inc-round-rock-tx-464342239
Backline: https://backline.care/
TWLOHA: https://twloha.com/

not trying to advertise anything. i'm more asking if anyone in screamo/emo/hardcore is doing this kind of thing in a real, diy way, or if there are people here who've been part of similar support/community projects."""),
        make_update(F, 21, "https://www.reddit.com/r/screamo/"),
    ]

    # Execute all writes
    ss.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"valueInputOption": "RAW", "data": updates},
    ).execute()
    print(f"Written {len(updates)} cell updates.")

    # Apply formatting to restored and new rows
    format_rows(service, sid, 2, 21)
    print("Formatting applied to rows 2-21.")


if __name__ == "__main__":
    main()
