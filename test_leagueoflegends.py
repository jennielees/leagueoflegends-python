from leagueoflegends import LeagueOfLegends, RiotError
from nose.tools import *

import doctest
import time

import os

doctest.testfile('README.md', verbose=False)

api_key = os.environ['LOL_API_KEY']
lol = LeagueOfLegends(api_key)

TEST_SUMMONER_ID = 5908
TEST_SUMMONER_NAME = "Dyrus"

TEST_SUMMONER_IDS = [ 5908, 120546, 19347723 ]
TEST_SUMMONER_NAMES = [ "Dyrus", "RiotPhreak", "PhantomL0rd"]

# Test region switching
def test_region_set():
    url = lol.set_api_region('euw')
    assert url == 'https://prod.api.pvp.net/api/lol/euw/v1.2/'
    url = lol.set_api_region('azeroth')
    assert url == None
    lol.set_api_region('na')

# Test version switching
def test_version_set():
    url = lol.set_api_version('1.1')
    assert url == 'https://prod.api.pvp.net/api/lol/na/v1.1/'
    lol.set_api_version('1.2')

# Test champion retrieval
def test_champion_get():
    result = lol.get_champions()
    assert len(result) > 0

def test_champion_free():
    result = lol.get_champions(True)
    for c in result:
        assert c['freeToPlay'] == True

def test_summoner_games_get():
    result = lol.get_summoner_games(TEST_SUMMONER_ID)
    assert len(result) > 0

def test_summoner_leagues():
    result = lol.get_summoner_leagues(TEST_SUMMONER_ID)
    assert len(result) > 0

def test_summoner_stats():
    result = lol.get_summoner_stats(TEST_SUMMONER_ID)
    assert len(result) > 0

@raises(RiotError)
def test_rate_limit_handling():
    result = lol.get_summoner_leagues(TEST_SUMMONER_ID)
    league_members = result["RANKED_SOLO_5x5"]["entries"]
    for summoner in league_members[:10]:
#        print summoner["playerOrTeamId"]
        lol.get_summoner_by_id(summoner["playerOrTeamId"])

def test_sleep_for_rate_limit():
    # Inserting a sleep statement in here: when nose runs tests
    # in succession, a rate limit error is guaranteed.
    print "Sleeping for 10 seconds to avoid rate limits."
    time.sleep(10)

def test_summoner_ranked_stats():
    result = lol.get_summoner_ranked_stats(TEST_SUMMONER_ID)
    assert len(result) > 0

def test_summoner_get_by_id():
    result = lol.get_summoner_by_id(TEST_SUMMONER_ID)
    assert result["name"] == TEST_SUMMONER_NAME

def test_summoner_get_by_name():
    result = lol.get_summoner_by_name(TEST_SUMMONER_NAME)
    assert result["id"] == TEST_SUMMONER_ID

def test_summoner_masteries():
    result = lol.get_summoner_masteries(TEST_SUMMONER_ID)
    assert len(result) > 0

def test_summoner_runes():
    result = lol.get_summoner_runes(TEST_SUMMONER_ID)
    assert len(result) > 0

def test_summoner_names_batch():
    result = lol.get_summoner_names(TEST_SUMMONER_IDS)
    assert result[0]["name"] == TEST_SUMMONER_NAMES[0]

def test_summoner_teams():
    result = lol.get_summoner_teams(TEST_SUMMONER_ID)
    assert result[0].get("teamStatSummary") is not None

# Test internal summoner_id setter
def test_summoner_id():
    lol.set_summoner(TEST_SUMMONER_NAME)
    result = lol.get_summoner_by_id()
    assert result["name"] == TEST_SUMMONER_NAME

# Test smart get_summoner

def test_summoner_get():
    result = lol.get_summoner(TEST_SUMMONER_NAME)
    assert result["id"] == TEST_SUMMONER_ID
    result = lol.get_summoner(TEST_SUMMONER_ID)
    assert result["name"] == TEST_SUMMONER_NAME

# shortcut for command line to test tests.
# usually run via nose
if __name__=='__main__':
    test_champion_free()