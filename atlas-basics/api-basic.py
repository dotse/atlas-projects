#!/usr/bin/env python3
# by rog
# https://ripe-atlas-sagan.readthedocs.io/en/latest/use.html#how-to-use-this-library
# https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html#dns

"""
Gets the measurement specified by the measurement id (msm_id) start and end time
and returns a list of dns nodes responding and their response time for the query

"""


from ripe.atlas.sagan import DnsResult
from ripe.atlas.cousteau import AtlasResultsRequest

kwargs = {"msm_id": 1413716, "start": 1567133400, "stop": 1567134000}

is_success, results = AtlasResultsRequest(**kwargs).create()

if is_success:
    for result in results:
        my_result = DnsResult(result)
        print(
            my_result.responses[0].abuf.answers[0].data_string
            + " -> "
            + str(my_result.responses[0].response_time)
        )
