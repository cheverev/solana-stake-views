import json
import subprocess as sp
import argparse as ap


def solana():
    parser = ap.ArgumentParser(description='Solana stake views')
    parser.add_argument('-v', '--vote-account', metavar='', type=str, help='Solana vote key validator', required=True)
    args = parser.parse_args()
    sol_str = sp.getoutput(f"solana stakes -um {args.vote_account} --output json")
    sol_list = json.loads(sol_str)
    list_withdrawer= []
    seen = set()
    stake_res = []
    for elem in range(len(sol_list)):
        list_withdrawer.append(sol_list[elem].get('withdrawer'))
    list_withdrawer = [x for x in list_withdrawer if x not in seen and not seen.add(x)]
    for withdrawer in list_withdrawer:
        quantity = 0
        stake_sum = 0
        for elem in range(len(sol_list)):
            if withdrawer == sol_list[elem].get('withdrawer'):
                quantity += 1
                stake_sum += sol_list[elem].get('delegatedStake')
        stake_sum = stake_sum / 1000000000
        stake_res.append({'withdrawer': withdrawer, 'quantity': quantity, 'stake_sum': stake_sum})
        stake_res.sort(key=lambda d: d['stake_sum'], reverse=True)
        print("\n")
    for stake in stake_res:
        print(f"withdrawer key {stake.get('withdrawer')}")
        print(f"Количество стекйков {stake.get('quantity')} на сумму {stake.get('stake_sum')}")
        print("-"*60)

if __name__ == '__main__':
    solana()
