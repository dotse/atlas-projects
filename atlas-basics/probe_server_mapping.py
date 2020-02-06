#!/usr/bin/env python3
# by rog


#!/usr/bin/env python3
# by rog
# https://ripe-atlas-sagan.readthedocs.io/en/latest/use.html#how-to-use-this-library
# https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html#dns
# https://atlas.ripe.net/api/v2/measurements/23265672/results/?start=1574595600&stop=1574596200&format=json

"""
Maps which name server instances are answering which atlas probes
"""


from ripe.atlas.sagan import DnsResult
from ripe.atlas.cousteau import AtlasResultsRequest
import dns.message
import base64
from collections import defaultdict

d = defaultdict(list)

def measurement_list():
    listan = [
        {"msm_id": 3912948, "start": 1580736272, "stop": 1580736603},
        {"msm_id": 23917314, "start": 1580891978},
        ]

    for item in listan:
        yield item


def measurement_parser(kwargs):
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
                        # print(f"{probe} -> NSID: {str(opt.data)}")
                        d[str(opt.data)].append(probe)
            except:
                 next
    return d
    # for item in d:
        # print(f"{item} -> {d[item]}")


if __name__ == '__main__':
    coll_dic = defaultdict(list)
    for measurement in measurement_list():
        print(measurement)
        mapping = measurement_parser(measurement)
        for item in mapping:
            print(f"{item} -> {len(mapping[item])}")
