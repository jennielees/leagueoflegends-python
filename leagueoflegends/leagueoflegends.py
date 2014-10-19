#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Python library for the League of Legends official API
Copyright (c) 2013 Jennie Lees <jennielees@gmail.com>

The LoL API belongs to Riot and can be found here:
https://developer.riotgames.com/

This product is not endorsed, certified or otherwise
approved in any way by Riot Games, Inc. or any of its affiliates.
"""

__author__ = 'Jennie Lees'
__version__ = '1.4b'

import urllib2
import json
import unicodedata
import re

class LeagueOfLegends:

    API_BASE_URL = 'api.pvp.net/api/lol'
    GLOBAL_BASE_URL = 'https://global.pvp.net/api/lol'
    api_region = 'na'
    api_version = '1.4'
    api_url = 'https://' + api_region + '.' + API_BASE_URL + '/' + api_region + '/' + 'v' + api_version + '/'

    def __init__(self, api_key, cache={}):
        self.api_key = api_key
        self.__cache = cache

    def __webrequest(self, url):
        # print 'Making request to: ' + url
        try:
            opener = urllib2.build_opener(NotModifiedHandler())
            req = urllib2.Request(url)

            if url in self.__cache:
                # Return summoner detail URLs from cache explicitly
                # to avoid repeated API calls
                if url.find('summoner/by-name'):
                    return self.__cache[url]['response']

                if 'etag' in self.__cache[url]:
                    print 'Adding ETag to request header: '\
                        + self.__cache[url]['etag']
                    req.add_header('If-None-Match',
                                   self.__cache[url]['etag'])
                if 'last_modified' in self.__cache[url]:
                    print 'Adding Last-Modified to request header: '\
                        + self.__cache[url]['last_modified']
                    req.add_header('If-Modified-Since',
                                   self.__cache[url]['last_modified'])

            url_handle = opener.open(req)

            if hasattr(url_handle, 'code') and url_handle.code == 304:
                print 'Got 304 response, no body send'
                return self.__cache[url]['response']
            else:
                headers = url_handle.info()
                response = url_handle.read()

                cache_data = {
                    'response': response,
                    'url': url.replace('?api_key=' + self.api_key, '')}

                if headers.getheader('Last-Modified'):
                    cache_data['last_modified'] = headers.getheader('Last-Modified')

                if headers.getheader('ETag'):
                    cache_data['etag'] = headers.getheader('ETag').replace('"', '')

                self.__cache[url] = cache_data
                return response
        except urllib2.HTTPError, e:
            # You should surround your code with try/catch that looks for a HTTPError
            # code 429 -- this is a rate limit error from Riot.
            # print 'HTTPError calling ' + url
            raise RiotError(e.code)
            return None

    def get_cache(self, url=None):
        if url is not None:
            return self.__cache[url]
        else:
            return self.__cache

    def set_api_region(self, region):
        if region is not None:
            if region.lower() in ['na', 'euw', 'eune', 'br', 'lan', 'las' 'oce']:
                self.api_region = region.lower()
                self.update_api_url()
                return self.api_url
            else:
                return None

    def set_api_version(self, version):
        if version is not None:
            self.api_version = version
            self.update_api_url()
            return self.api_url

    def update_api_url(self):
        self.api_url = 'https://' +  self.api_region+ '.' + self.API_BASE_URL + '/' + self.api_region + '/' + 'v' + self.api_version + '/'
      #  print self.api_url

    def __getjsondata(self, namespace, query=''):

        query = query.replace(' ', '+')
        query = unicodedata.normalize('NFKD',
                                      query.decode('utf-8')) \
            .encode('ascii', 'ignore')
        url = self.api_url + namespace + query + '.js?api_key='\
            + self.api_key
        response = self.__webrequest(url)
        if response is not None:
            response = json.loads(response, strict=False)
        return response

    def get_data(self, namespace, query=''):
        result = self.__getjsondata(namespace, '/%s' % query)
        return result

    # Riot Games API
    # https://developer.riotgames.com/api/methods

    # ====================================================================
    # champion-v1.2
    # https://developer.riotgames.com/api/methods#!/617

    # Retrieve all champions.
    # https://developer.riotgames.com/api/methods#!/617/1923
    def get_champions(self, free_to_play=False):
        self.set_api_version('1.2')
        url = self.api_url + 'champion?freeToPlay=' + str(free_to_play) + '&api_key=%s' % (self.api_key)
        response = json.loads(self.__webrequest(url))
        return response['champions']

    # Retrieve champion by ID.
    # https://developer.riotgames.com/api/methods#!/617/1922
    def get_champion_by_id(self, champion_id=None):
        if champion_id is None:
            return
        self.set_api_version('1.2')
        url = self.api_url + 'champion/%s/?api_key=%s' % (champion_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # ====================================================================
    # game-v1.3
    # https://developer.riotgames.com/api/methods#!/618

    # Get recent games by summoner ID
    # https://developer.riotgames.com/api/methods#!/618/1924
    def get_summoner_games(self, summoner_id=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        self.set_api_version('1.3')
        url = self.api_url + 'game/by-summoner/%s/recent?api_key=%s' % (summoner_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response['games']

    # ====================================================================
    # league-v2.5
    # https://developer.riotgames.com/api/methods#!/741

    # Get leagues mapped by summoner ID for a given list of summoner IDs.
    # https://developer.riotgames.com/api/methods#!/741/2640
    def get_summoner_full_league(self, summoner_id=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        self.set_api_version('2.5')
        url = self.api_url + 'league/by-summoner/%s?api_key=%s' % (summoner_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response.get(str(summoner_id))

    # Get league entries mapped by summoner ID for a given list of summoner IDs.
    # https://developer.riotgames.com/api/methods#!/741/2641
    def get_summoner_league(self, summoner_id=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        self.set_api_version('2.5')
        url = self.api_url + 'league/by-summoner/%s/entry?api_key=%s' % (summoner_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response.get(str(summoner_id))

    # Get leagues mapped by team ID for a given list of team IDs.
    # https://developer.riotgames.com/api/methods#!/741/2639
    def get_team_full_league(self, team_id=None):
        if team_id is None:
            if self.team_id is not None:
                team_id = self.team_id
            else:
                return
        self.set_api_version('2.5')
        url = self.api_url + 'league/by-team/%s/?api_key=%s' % (team_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Get league entries mapped by team ID for a given list of team IDs.
    # https://developer.riotgames.com/api/methods#!/741/2638
    def get_team_league(self, team_id=None):
        if team_id is None:
            if self.team_id is not None:
                team_id = self.team_id
            else:
                return
        self.set_api_version('2.5')
        url = self.api_url + 'league/by-team/%s/entry?api_key=%s' % (team_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Get challenger tier leagues.
    # Default selection for Ranked Solo Queue
    # https://developer.riotgames.com/api/methods#!/741/2637
    def get_challenger(self, ranked_solo=False, ranked_5s=False, ranked_3s=False):
        queue = 'RANKED_SOLO_5x5'
        if ranked_5s == True:
            queue = 'RANKED_TEAM_5x5'
        elif ranked_3s == True:
            queue = 'RANKED_TEAM_3x3'
        self.set_api_version('2.5')
        url = self.api_url + 'league/challenger?type=%s&api_key=%s' % (queue, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # ====================================================================
    # lol-static-data-v1.2
    # Requests to this API will not be counted in your Rate Limit.
    # https://developer.riotgames.com/api/methods#!/710

    # Retrieves champion list.
    # https://developer.riotgames.com/api/methods#!/710/2529
    def get_champions_static(self, locale=None, version=None, dataById=False, champData=None):
        localeURL = ''
        versionURL = ''
        champDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        dataByIdURL = 'dataById=%s&' % (dataById)
        if champData != None:
            champDataURL = 'champData=%s&' % (champData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/champion?%s%s%s%sapi_key=%s' % (self.api_version, localeURL, versionURL, dataByIdURL, champDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves a champion by its id.
    # https://developer.riotgames.com/api/methods#!/710/2526
    def get_champion_by_id_static(self, champion_id=None, locale=None, version=None, champData=None):
        if champion_id is None:
            return
        localeURL = ''
        versionURL = ''
        champDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        if champData != None:
            champDataURL = 'champData=%s&' % (champData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/champion/%s?%s%s%sapi_key=%s' % (self.api_version, champion_id, localeURL, versionURL, champDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves item list.
    # https://developer.riotgames.com/api/methods#!/710/2523
    def get_items(self, locale=None, version=None, itemListData=None):
        localeURL = ''
        versionURL = ''
        itemListDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        if itemListData != None:
            itemListDataURL = 'itemListData=%s&' % (itemListData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/item?%s%s%sapi_key=%s' % (self.api_version, localeURL, versionURL, itemListDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves item by its unique id.
    # https://developer.riotgames.com/api/methods#!/710/2534
    def get_item_by_id(self, item_id=None, locale=None, version=None, itemListData=None):
        if item_id is None:
            return
        localeURL = ''
        versionURL = ''
        itemListDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        if itemListData != None:
            itemListDataURL = 'itemListData=%s&' % (itemListData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/item/%s?%s%s%sapi_key=%s' % (self.api_version, item_id, localeURL, versionURL, itemListDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves mastery list.
    # https://developer.riotgames.com/api/methods#!/710/2531
    def get_masteries(self, locale=None, version=None, masteryListData=None):
        localeURL = ''
        versionURL = ''
        masteryListDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        if masteryListData != None:
            masteryListDataURL = 'masteryListData=%s&' % (masteryListData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/mastery?%s%s%sapi_key=%s' % (self.api_version, localeURL, versionURL, masteryListDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves mastery item by its unique id.
    # https://developer.riotgames.com/api/methods#!/710/2533
    def get_mastery_by_id(self, mastery_id=None, locale=None, version=None, masteryListData=None):
        if mastery_id is None:
            return
        localeURL = ''
        versionURL = ''
        masteryListDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        if masteryListData != None:
            masteryListDataURL = 'masteryListData=%s&' % (masteryListData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/mastery/%s?%s%s%sapi_key=%s' % (self.api_version, mastery_id, localeURL, versionURL, masteryListDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieve realm data.
    # https://developer.riotgames.com/api/methods#!/710/2528
    def get_realms(self):
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/realm?api_key=%s' % (self.api_version, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves rune list.
    # https://developer.riotgames.com/api/methods#!/710/2530
    def get_runes(self, locale=None, version=None, runeData=None):
        localeURL = ''
        versionURL = ''
        runeDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        if runeData != None:
            runeDataURL = 'runeData=%s&' % (runeData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/rune?%s%s%sapi_key=%s' % (self.api_version, localeURL, versionURL, runeDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves rune by its unique id.
    # https://developer.riotgames.com/api/methods#!/710/2525
    def get_rune_by_id(self, rune_id=None, locale=None, version=None, runeData=None):
        if rune_id is None:
            return
        localeURL = ''
        versionURL = ''
        runeDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        if runeData != None:
            runeDataURL = 'runeData=%s&' % (runeData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/rune/%s?%s%s%sapi_key=%s' % (self.api_version, rune_id, localeURL, versionURL, runeDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves summoner spell list.
    # https://developer.riotgames.com/api/methods#!/710/2532
    def get_summoner_spells(self, locale=None, version=None, dataById=False, spellData=None):
        localeURL = ''
        versionURL = ''
        spellDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        dataByIdURL = 'dataById=%s&' % (dataById)
        if spellData != None:
            spellDataURL = 'spellData=%s&' % (spellData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/summoner-spell?%s%s%s%sapi_key=%s' % (self.api_version, localeURL, versionURL, dataByIdURL, spellDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieves summoner spell by its unique id.
    # https://developer.riotgames.com/api/methods#!/710/2524
    def get_summoner_spell_by_id(self, summoner_spell_id=None, locale=None, version=None, spellData=None):
        if summoner_spell_id is None:
            return
        localeURL = ''
        versionURL = ''
        spellDataURL = ''
        if locale != None:
            localeURL = 'locale=%s&' % (locale)
        if version != None:
            versionURL = 'version=%s&' % (version)
        if spellData != None:
            spellDataURL = 'spellData=%s&' % (spellData)
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/summoner-spell/%s?%s%s%sapi_key=%s' % (self.api_version, summoner_spell_id, localeURL, versionURL, spellDataURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Retrieve version data.
    # https://developer.riotgames.com/api/methods#!/710/2527
    def get_versions(self):
        self.set_api_version('1.2')
        url = self.GLOBAL_BASE_URL + '/static-data/' + self.api_region + '/v%s/versions?api_key=%s' % (self.api_version, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # ====================================================================
    # match-v2.2
    # https://developer.riotgames.com/api/methods#!/856

    # Get match detail from match ID.
    # https://developer.riotgames.com/api/methods#!/856/2992
    def get_match(self, match_id, include_timeline=False):
        if not match_id: return
        self.set_api_version('2.2')
        url = self.api_url + 'match/%s?api_key=%s' % (match_id, self.api_key)
        if include_timeline:
            url += '&includeTimeline=True'
        response = json.loads(self.__webrequest(url))
        return response


    # ====================================================================
    # matchhistory-v2.2
    # https://developer.riotgames.com/api/methods#!/855

    # Get match history from summoner ID.
    # https://developer.riotgames.com/api/methods#!/855/2991
    # Optional arguments:
    #  championIds (comma-separated)
    #  rankedQueues (comma-separated)
    #  beginIndex
    #  endIndex
    def get_summoner_match_history(self, summoner_id=None, **kwargs):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        self.set_api_version('2.2')
        url = self.api_url + 'matchhistory/%s?api_key=%s' % (summoner_id, self.api_key)
        if kwargs:
            from urllib import urlencode
            url += '&' + urlencode(kwargs)
        response = json.loads(self.__webrequest(url))
        return response

    # ====================================================================
    # stats-v1.3
    # https://developer.riotgames.com/api/methods#!/622

    # Get ranked stats by summoner ID
    # https://developer.riotgames.com/api/methods#!/622/1937
    def get_summoner_ranked_stats(self, summoner_id=None, season=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        if season is None:
            seasonURL = ''
        else:
            seasonURL = 'season=SEASON%s&' % (season)
        self.set_api_version('1.3')
        url = self.api_url + 'stats/by-summoner/%s/ranked?%sapi_key=%s' % (summoner_id, seasonURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Get player stats summaries by summoner ID.
    # https://developer.riotgames.com/api/methods#!/622/1938
    def get_summoner_stats(self, summoner_id=None, season=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        if season is None:
            seasonURL = ''
        else:
            seasonURL = 'season=SEASON%s&' % (season)
        self.set_api_version('1.3')
        url = self.api_url + 'stats/by-summoner/%s/summary?%sapi_key=%s' % (summoner_id, seasonURL, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # ====================================================================
    # summoner-v1.4
    # https://developer.riotgames.com/api/methods#!/620

    # Get summoner objects mapped by standardized summoner name for a given list of summoner names.
    # https://developer.riotgames.com/api/methods#!/620/1930
    def get_summoner_by_name(self, summoner_name):
        if summoner_name == '':
            return
        self.set_api_version('1.4')
        url = self.api_url + 'summoner/by-name/%s?api_key=%s' % (summoner_name, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response.get(summoner_name.lower())

    # Get summoner objects mapped by summoner ID for a given list of summoner IDs.
    # https://developer.riotgames.com/api/methods#!/620/1931
    def get_summoner_by_id(self, summoner_id=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        self.set_api_version('1.4')
        url = self.api_url + 'summoner/%s?api_key=%s' % (summoner_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response.get(str(summoner_id))

    # Get mastery pages mapped by summoner ID for a given list of summoner IDs.
    # https://developer.riotgames.com/api/methods#!/620/1933
    def get_summoner_masteries(self, summoner_id=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        self.set_api_version('1.4')
        url = self.api_url + 'summoner/%s/masteries?api_key=%s' % (summoner_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Get summoner names mapped by summoner ID for a given list of summoner IDs.
    # https://developer.riotgames.com/api/methods#!/620/1934
    def get_summoner_names(self, summoner_ids):
        if len(summoner_ids) == 0:
            return
        self.set_api_version('1.4')
        try:
            summoner_ids = ",".join([str(s) for s in summoner_ids])
        except ValueError:
            raise Exception("Summoner IDs must be numeric.")
        url = self.api_url + 'summoner/%s/name?api_key=%s' % (summoner_ids, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # Get rune pages mapped by summoner ID for a given list of summoner IDs.
    # https://developer.riotgames.com/api/methods#!/620/1932
    def get_summoner_runes(self, summoner_id=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        self.set_api_version('1.4')
        url = self.api_url + 'summoner/%s/runes?api_key=%s' % (summoner_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # ====================================================================
    # team-v2.4
    # https://developer.riotgames.com/api/methods#!/743

    # Get teams mapped by summoner ID for a given list of summoner IDs.
    # https://developer.riotgames.com/api/methods#!/743/2644
    def get_summoner_teams(self, summoner_id=None):
        if summoner_id is None:
            if self.summoner_id is not None:
                summoner_id = self.summoner_id
            else:
                return
        self.set_api_version('2.4')
        url = self.api_url + 'team/by-summoner/%s?api_key=%s' % (summoner_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response.get(str(summoner_id))

    # Get teams mapped by team ID for a given list of team IDs.
    # This API will be deprecated on 07/06/14.
    # https://developer.riotgames.com/api/methods#!/743/2645
    def get_team(self, team_id=None):
        if team_id is None:
            if self.team_id is not None:
                team_id = self.team_id
            else:
                return
        self.set_api_version('2.4')
        url = self.api_url + 'team/%s?api_key=%s' % (team_id, self.api_key)
        response = json.loads(self.__webrequest(url))
        return response

    # ====================================================================
    # Convenience function to set local summoner ID variable
    # from summoner name. All future API calls will use this
    # ID if there is none passed in.

    def set_summoner(self, summoner_name):
        summoner_id = self.get_summoner_by_name(summoner_name)['id']
        # print summoner_id
        self.summoner_id = summoner_id

    def set_summoner_id(self, summoner_id):
        # check numeric type
        self.summoner_id = summoner_id

    def set_team_id(self, team_id):
        # check numeric type
        self.team_id = team_id

    def get_summoner_id_from_name(self, summoner_name):
        return self.get_summoner_by_name(summoner_name)['id']

    def get_summoner_name_from_id(self, summoner_id):
        return self.get_summoner_by_id(summoner_id)['name']

    # Convenience functions to save typing.
    def get_games(self, summoner_id):
        return self.get_summoner_games(summoner_id)

    def get_league(self, summoner_id):
        return self.get_summoner_league(summoner_id)

    def get_stats(self, summoner_id):
        return self.get_summoner_stats(summoner_id)

    def get_ranked_stats(self, summoner_id):
        return self.get_summoner_ranked_stats(summoner_id)

    def get_summoner(self, summoner_argument):
        numeric = re.compile('\d+')
        if numeric.match(str(summoner_argument)):
            # Argument is an ID
            return self.get_summoner_by_id(summoner_argument)
        else:
            return self.get_summoner_by_name(summoner_argument)

# ====================================================================

class RiotResponse(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)

class InputError(Exception):
    # Input problem. Please check your input is within the correct parameters.
    pass

class RiotError(Exception):
    def __init__(self, code):
        self.code = code
        if code == 429:
            self.error_msg = "Rate limit exceeded. Riot smash."
        else:
            self.error_msg = "Error %s from Riot servers." % code

    def __str__(self):
        return repr(self.error_msg)

class DataMismatchError(Exception):
    # Received data back for a different query than requested, e.g. summoner ID mismatch.
    pass

class NotModifiedHandler(urllib2.BaseHandler):

    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl
