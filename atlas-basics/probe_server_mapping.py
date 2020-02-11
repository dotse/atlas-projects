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
# TODO: get timestamp
# TODO: calculate at what time the nodes were synced
# TODO: caclulate propagation delay based on txt record

from ripe.atlas.sagan import DnsResult
from ripe.atlas.cousteau import AtlasResultsRequest
import dns.message
import base64
from collections import defaultdict
import os
import sys

d = defaultdict(list)

def measurement_list():
    """
    list of measurements
    :return:
    """
    listan = [
        {"msm_id": 23912948, "start": 1580736272, "stop": 1580736603},
        {"msm_id": 23917314, "start": 1580891978},
        ]

    for item in listan:
        yield item


def measurement_parser(kwargs):
    """
    receives a ripe atlas measurement id with a start time and possibly a stop time
    and returns a dictionary containing the nodes reached as keys and a list of probes that
    contacted the node as values

    :param kwargs:
    :return dictionary keys = dns nodes, values = list of probes that contacted
    the dns node:
    """
    is_success, results = AtlasResultsRequest(**kwargs).create()
    if is_success:
        for result in results:
            probe = result['prb_id']
            try:
                answer = result['result']['abuf'] + "=="
                content = base64.b64decode(answer)
                msg = dns.message.from_wire(content)
                soa_serial = msg.answer[0].to_text().split()[6]# if it is a soa query the soa will be in msg.answer[0]
                time = result['timestamp']
                for opt in msg.options:
                    if opt.otype == dns.edns.NSID:
                        print(f"{probe} -> NSID: {str(opt.data)} -> SOA: {soa_serial} : {time}")
                        d[str(opt.data.decode("utf-8"))].append(probe)
            except:
                 next
    return d
    # for item in d:
        # print(f"{item} -> {d[item]}")


def check_node_inclusion(responding_nodes):
    """
    compare the responding nodes to the nodes listed in nodes list to confirm
    that all node responded

    :param responding_nodes:
    :return Bool:
    """
    with open(os.path.join(sys.path[0], "denic_nodes"), "r") as file:
        denic_nodes = set([node.strip() for node in file])
        if set(responding_nodes) == denic_nodes:
            return True
        else:
            return False

if __name__ == '__main__':
    coll_dic = defaultdict(list)
    for measurement in measurement_list():
        mapping = measurement_parser(measurement)
    # for item in mapping:
        # print(f"{item} -> {mapping[item][0]}")

    listan = [x for x in mapping]
    print(listan)
    # for key in mapping.keys():
    #     print(key)

    print(check_node_inclusion(listan))
