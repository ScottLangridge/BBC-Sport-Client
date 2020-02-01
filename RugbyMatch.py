import requests
import json
import re


class RugbyMatch:
    _MATCH_URL_TEMPLATE = 'https://www.bbc.co.uk/sport/rugby-union/match/%s'

    _JSON_URL_TEMPLATE = 'https://push.api.bbci.co.uk/p?t=morph%%3A%%2F%%2Fdata%%2Fbbc-morph-graphql%%2Fquery%%2F' \
                         '%%257Bsbl%%257BrugbyUnion%%257Bevent(' \
                         'eventId%%253A%%2522%s%%2522)%%257Bid%%252CstartDate%%252Cstatus%%252CstatusIndicator' \
                         '%%252CstatusReason%%252Cteams%%257BabbreviatedName%%252Cactions%%257BconversionsSummary' \
                         '%%252CdropGoalsSummary%%252CpenaltiesSummary%%252CtriesSummary%%257Dalignment%%252CfullName' \
                         '%%252CfullTimeScore%%252ChalfTimeScore%%252Cid%%252Cplayers%%257BabbreviatedName' \
                         '%%252CfullName%%252Cid%%252CshirtNumber%%252Cstarter%%257DrunningScore%%252Cslug' \
                         '%%257DtimeToDisplay%%252Ctournament%%257BfullName%%252Cslug%%257Dvenue%%257D%%257D%%257D' \
                         '%%257D%%2Ftoken%%2F%s%%2Fversion%%2F1.1.65&c=1&t=morph%%3A%%2F%%2Fdata%%2Fbbc-morph-graphql' \
                         '%%2Fquery%%2F%%257Bsbl%%257BrugbyUnion%%257Bevent(' \
                         'eventId%%253A%%2522%s%%2522)%%257Bteams%%257BabbreviatedName%%252Cactions' \
                         '%%257BconversionsSummary%%252CdropGoalsSummary%%252CpenaltiesSummary%%252CtriesSummary' \
                         '%%257Dalignment%%252CfullName%%252CfullTimeScore%%252ChalfTimeScore%%252Cplayers' \
                         '%%257BabbreviatedName%%252CfullName%%252Cid%%252CshirtNumber%%252Cstarter%%257DrunningScore' \
                         '%%252Cslug%%257D%%257D%%257D%%257D%%257D%%2Ftoken%%2F%s%%2Fversion%%2F1.1.55&c=1 '

    _EMPTY_RETURN = '{"moments":[],"meta":{"poll-interval":30}}'

    # Takes a "moment" (the JSON object used in the BBC sport API response) and unpacks it into the useful information.
    @staticmethod
    def _unpack_payload(payload):
        return json.loads(payload['payload'])['sbl']['rugbyUnion']['event']

    def __init__(self, match_id):
        # Config for fetching data
        self._match_id = match_id
        self._tokens = self._get_tokens()

        # Public attributes
        self.match_stats = None
        self.team_stats = None

        # Get data
        self.update()

    def _get_tokens(self):
        pre_token = '/token/'
        post_token = '/version/'

        match_page_url = self._MATCH_URL_TEMPLATE % self._match_id
        match_request = requests.get(match_page_url)
        match_page_html = match_request.text

        search_string = '%s(.*)%s(.*)%s(.*)%s' % (pre_token, post_token, pre_token, post_token)
        token_match = re.search(search_string, match_page_html).groups()
        return token_match[0], token_match[-1]

    def update(self):
        # Get JSON
        request_url = self._JSON_URL_TEMPLATE % (self._match_id, self._tokens[0], self._match_id, self._tokens[1])
        r = requests.get(request_url)
        print("Get request made.")

        if r.text == self._EMPTY_RETURN:
            request_url = self._JSON_URL_TEMPLATE % (self._match_id, self._tokens[1], self._match_id, self._tokens[0])
            r = requests.get(request_url)

        # Unpack Payloads
        topics = [self._unpack_payload(payload) for payload in r.json()['moments']]

        # Convert payloads into correct format for my purposes and save them.
        full_stats = topics[0]
        del full_stats['teams']
        self.match_stats = full_stats

        team_stats = topics[1]
        team_stats = team_stats['teams']
        for team in range(len(team_stats)):
            display_name = team_stats[team]['abbreviatedName'][:3].upper()
            team_stats[team]['displayName'] = display_name
        self.team_stats = team_stats
