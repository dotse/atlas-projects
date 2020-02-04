#!/usr/bin/env python3
# by rog
# https://ripe-atlas-sagan.readthedocs.io/en/latest/use.html#how-to-use-this-library
# https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html#dns
# https://atlas.ripe.net/api/v2/measurements/23265672/results/?start=1574595600&stop=1574596200&format=json

"""
Gets the measurement specified by the measurement id (msm_id) start and end time
and returns a list of dns nodes responding and their response time for the query

"""


from ripe.atlas.sagan import DnsResult
from ripe.atlas.cousteau import AtlasResultsRequest
import dns.message
import base64
from collections import defaultdict

d = defaultdict(list)


kwargs = {"msm_id": 23912948, "start": 1580736272, "stop": 1580736603}
# kwargs = {"msm_id": 1413716, "start": 1567133400, "stop": 1567134000}
# kwargs = {"msm_id": 23265672, "start": 1574595600, "stop": 1574596200}

is_success, results = AtlasResultsRequest(**kwargs).create()

if is_success:
    count = 0
    for result in results:
        probe = result['prb_id']
        try:
            answer = result['result']['abuf'] + "=="
            content = base64.b64decode(answer)
            msg = dns.message.from_wire(content)
            for opt in msg.options:
                if opt.otype == dns.edns.NSID:
                    print(f"{probe} -> NSID: {str(opt.data)}")
                    d[str(opt.data)].append(probe)




        except:
            next
    for item in d:
        print(f"{item} -> {d[item]}")
        # my_result = DnsResult(result)
        # print(
        #     my_result.responses[0].abuf.answers[0].data_string
        #     + " -> "
        #     + str(my_result.responses[0].response_time)
        # )
