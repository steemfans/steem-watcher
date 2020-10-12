#encoding:UTF-8
import json, os, sys, time, re

watchingTypes = {
    'claim_account': 1,
    'create_claimed_account': 2,
    'account_create': 3,
}

notNeedToConvertOps = [
    'vote',
]

measurement = 'op_analytics'

def parseOpsIntoInflux(ops, timestamp):
    timestamp = timestamp.replace(' ', 'T') + 'Z'
    data = []
    for op in ops:
        if op[0] in notNeedToConvertOps:
            data.append({
                "measurement": measurement,
                "tags": {
                    "op_type": op[0],
                },
                "time": timestamp,
                "fields": op[1]
            })

        if op[0] == 'account_create' or op[0] == 'create_claimed_account':
            data.append({
                "measurement": measurement,
                "tags": {
                    "op_type": op[0],
                },
                "time": timestamp,
                "fields": {
                    "creator": op[1]["creator"],
                    "new_account_name": op[1]["new_account_name"],
                }
            })
        if op[0] == 'comment':
            content = op[1]['body']
            # check if this comment is a patch
            pattern = re.compile(r'@@ -\d+,\d+ \+\d+,\d+ @@', re.I)
            m = pattern.match(content)
            if m is None:
                # check if this comment is a post
                if op[1]['parent_author'] == '':
                    data.append({
                        "measurement": measurement,
                        "tags": {
                            "op_type": op[0]+'_post',
                        },
                        "time": timestamp,
                        "fields": {
                            "author": op[1]["author"],
                            "permlink": op[1]["permlink"],
                        }
                    })
                else:
                    data.append({
                        "measurement": measurement,
                        "tags": {
                            "op_type": op[0]+'_comment',
                        },
                        "time": timestamp,
                        "fields": {
                            "parent_author": op[1]["parent_author"],
                            "parent_permlink": op[1]["parent_permlink"],
                            "author": op[1]["author"],
                            "permlink": op[1]["permlink"],
                        }
                    })
        if op[0] == 'claim_account':
            data.append({
                "measurement": measurement,
                "tags": {
                    "op_type": op[0],
                },
                "time": timestamp,
                "fields": {
                    "creator": op[1]["creator"]
                }
            })
        if op[0] == 'transfer_to_vesting':
            data.append({
                "measurement": measurement,
                "tags": {
                    "op_type": op[0],
                },
                "time": timestamp,
                "fields": {
                    "from": op[1]["from"],
                    "to": op[1]["to"],
                    "amount": float(op[1]["amount"].split()[0]),
                }
            })
        if op[0] == 'withdraw_vesting':
            data.append({
                "measurement": measurement,
                "tags": {
                    "op_type": op[0],
                },
                "time": timestamp,
                "fields": {
                    "account": op[1]["account"],
                    "vesting_shares": float(op[1]["vesting_shares"].split()[0]),
                }
            })

    return data
