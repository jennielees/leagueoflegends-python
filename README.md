leagueoflegends-python
==========

*This product is not endorsed, certified or otherwise approved in any way by Riot Games, Inc. or any of its affiliates.*

###Quickstart

    pip install leagueoflegends

    from leagueoflegends import LeagueOfLegends, RiotError
    lol = LeagueOfLegends('your-api-key')

    # Call the API with explicit summoner ID
    id = lol.get_summoner_by_name('your-summoner-name')
    lol.get_games(id)

    # Or set the ID globally for all future calls
    lol.set_summoner('your-summoner-name')
    lol.get_summoner_stats()
    lol.get_summoner_ranked_stats()

    # Access data through dictionaries
    try:
        teams = lol.get_summoner_teams()
        for t in teams:
            print t["name"]
            for m in t["roster"]["memberList"]:
                id = m["playerId"]
                print id
                print lol.get_summoner_by_id(id)["name"]
    except RiotError, e:
        print e.error_msg

###Words

This is an unofficial Python Library for the official League of Legends API (Riot Developer API), wrapping HTTP calls into Python dictionaries.

Full documentation for Riot's RESTful API is [here](https://developer.riotgames.com/api/). Dictionaries returned by this library corresponds to the datatypes documented there.

Library code is distributed under the [WTFPL](http://www.wtfpl.net/). You are free to modify and redistribute. Attribution is a nice touch, and I'd love to hear what you get up to with this library.

At last update this supported API versions:
 * champion-1.2
 * game-1.3
 * league-2.5
 * lol-static-data-1.2
 * stats-1.3
 * summoner-1.4
 * team-2.4
 * match-2.2
 * matchhistory-2.2

Not supported yet:
 * lol-status-1.0

###General Usage

The Riot Developer API does not support anonymous access. You must [register for an API key](https://developer.riotgames.com/) with Riot before using this API.


    from leagueoflegends import LeagueOfLegends
    lol = LeagueOfLegends('your-api-key')

####get_champions ([API Doc](https://developer.riotgames.com/api/methods#!/311))

Returns a list of all champions. Optionally only return free to play champions.

    champs = lol.get_champions(free_to_play=False)
    for champ in champs:
        print champ["name"]
        

###Summoner-Specific Methods

####get_summoner_games ([API Doc](https://developer.riotgames.com/api/methods#!/313/1061))

Returns a list of recent games played by a specific summoner, up to 10.

Takes a specific `summoner_id` (long) argument. If you want to query by summoner name, add a second lookup (see below).

    games = lol.get_summoner_games(12345678)
    for game in games:
        print game["championId"]

####get_summoner_leagues ([API Doc](https://developer.riotgames.com/api/methods#!/307/1055))

Returns the leagues associated with a specific summoner ID.

    leagues = lol.get_summoner_leagues(12345678)
    for queue_type in leagues:
        print leagues[queue_type]["tier"]

####get_summoner_stats ([API Doc](https://developer.riotgames.com/api/methods#!/317/1075))

Returns summary stats (aggregate over all champions) for a specific summoner ID.

    stats = lol.get_summoner_stats(12345678)
    for stat in stats:
        print stat["aggregatedStats"]["totalAssists"]

####get_summoner_ranked_stats ([API Doc](https://developer.riotgames.com/api/methods#!/317/1074))

Returns aggregated stats, summarized per champion, from ranked matches. Includes statistics for Twisted Treeline and Summoner's Rift.

    rankedstats = lol.get_summoner_ranked_stats(12345678)
    for champ in stats:
        print champ["id"]

####get_summoner_by_id ([API Doc](https://developer.riotgames.com/api/methods#!/315/1069))

Returns basic information about a specific summoner ID (name, level, etc).

    summoner = lol.get_summoner_by_id(12345678)
    print summoner["name"]

####get_summoner_by_name ([API Doc](https://developer.riotgames.com/api/methods#!/315/1067))

Returns the same information as `get_summoner_by_id` but queried by name.

    summoner = lol.get_summoner_by_name('RiotPhreak')
    print summoner["id"]

####get_summoner

Convenience shortcut to the above two functions. Takes either an ID or a name and returns the summoner object.

    summoner = lol.get_summoner('RiotPhreak')
    print summoner["id"]

    summoner = lol.get_summoner('12345678')
    print summoner["name"]

####get_summoner_id_from_name

Convenience shortcut to retrieving a summoner ID given a specific name, as per the `get_summoner_by_name` example snippet above.

    summoner_id = lol.get_summoner_by_name('RiotPhreak')
    stats = lol.get_summoner_stats(summoner_id)
    ...

####get_summoner_names ([API Doc](https://developer.riotgames.com/api/methods#!/315/1068))

Get up to 40 summoner names at once from a list of summoner IDs.

    summoner_ids = [1234, 5678, 12345678]
    summoner_names = lol.get_summoner_names(summoner_ids)
    for summoner in summoner_names:
        print summoner["name"]


####get_summoner_masteries ([API Doc](https://developer.riotgames.com/api/methods#!/315/1071))

Get mastery pages for a specific summoner ID.

    masteries = lol.get_summoner_masteries(12345678)
    for page in masteries:
        for talent in page["talents"]:
           print talent["name"]

####get_summoner_runes ([API Doc](https://developer.riotgames.com/api/methods#!/315/1070))

Get rune pages for a specific summoner ID.

    runes = lol.get_summoner_runes(12345678)
    for page in runes:
        for slot in page["slots"]:
           print slot["rune"]["name"] + ' '\
               + slot["rune"]["description"]



####get_summoner_teams ([API Doc](https://developer.riotgames.com/api/methods#!/310/1058))

Get team information for a specific summoner. Can return multiple teams.

    teams = lol.get_summoner_teams(12345678)

    for team in teams:
        print team["name"]

    for team in teams:
        for match in t["matchHistory"]:
            total_wins += 1 and match["win"]
    print total_wins


###Matches

####get_match ([API Doc](https://developer.riotgames.com/api/methods#!/856/2992))

Returns the match details for a specific `match_id`. Optional parameter `include_timeline` to return game timeline.

```
match = lol.get_match(12345678, include_timeline=True)
```

####get_summoner_match_history ([API Doc](https://developer.riotgames.com/api/methods#!/855/2991))

Returns the match history for a specific `summoner_id`. Optional parameters passed straight through to API: `championIds`, `rankedQueues`, `beginIndex`, `endIndex`.

```
matches = lol.get_summoner_match_history(12345678)
matches = lol.get_summoner_match_history(12345678, championIds=1, rankedQueues='RANKED_SOLO_5x5')

```

###Convenience

####set_summoner

Convenience function to set summoner ID from name. Summoner-specific functions can be called without an ID argument if this has been set.

    lol.set_summoner("RiotPhreak")
    lol.get_summoner_stats()
    lol.get_summoner_teams()

####get_games, get_leagues, get_stats, get_ranked_stats

If you're tired of typing 'summoner', these convenience functions might help.

###Config

####set_api_region

Takes a region as argument and executes all further API calls against that region.

Valid regions: `euw, eune, na, tr, br`.

Note: not all API functions support all regions. Check Riot documentation if you run into weird errors. At time of writing, `na, euw, eune` regions are valid for all calls.

Static data calls run against a `global` domain with a slightly different API URL format.

####set_api_version

Takes a version as argument, and sets it for future API calls. However, note that many API requests have the version hardcoded since there is variance between supported versions for each call. Where multiple versions of a specific endpoint are available, the newest version is used.

###Rate Limits

At time of writing, the Riot API limit is 10 requests every 10 seconds and 500 requests every 10 minutes. You will encounter a `RiotError` if you exceed this limit.

Consider your API request design wisely, and note that looking up a summoner ID from name is its own API call (although these queries are cached temporarily).

    try:
        for summoner in very_long_summoner_list:
            lol.get_summoner_by_name(summoner)
    except RiotError, e:
        print e.error_msg

###Tests

Tests are in `test_leagueoflegends.py` and the easiest way to run them is with [Nose](http://nose.readthedocs.org/en/latest/):

    pip install nose
    nosetests
