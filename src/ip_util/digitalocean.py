from digitalocean import Firewall, Manager, InboundRule
from digitalocean.baseapi import PUT
import json
from typing import List, Union
import requests
import os
from . import config


def binarize_ip(ip): 
    return sum(
    int(ip.split('.')[3-s]) << (8*s) for s in range(4))


def recover_ip(bin_ip): 
    return '.'.join(
    str((bin_ip >> (8*(3-s)))-(bin_ip >> (8*(4-s)) << 8)) for s in range(4))


def sites(bin_ip1, bin_ip2): 
    return 32 - next(n for n in range(1, 33) if bin_ip1 >> n == bin_ip2 >> n)


def get_subnet(ip1, ip2):
    binip1, binip2 = binarize_ip(ip1.split('/')[0]), binarize_ip(ip2.split('/')[0])
    st = sites(binip1, binip2)
    return recover_ip(binip1>>(32-st)<<(32-st))+'/'+str(st)


def get_external_ip():
    r = requests.get('https://api.ipify.org')
    return r.content.decode('utf-8')


def merge_into_ip_pool(ip, ip_pool, threshod_sites=10):
    ip = ip.split('/')[0]
    common_sites = [sites(binarize_ip(ip), binarize_ip(p.split('/')[0])) for p in ip_pool]
    if max(common_sites) < threshod_sites:
        ip_pool.append(ip)
        return ('new',)
    else:
        update_ind, to_update = next((i, ip_pool[i]) for i, s in enumerate(common_sites) if s==max(common_sites))
        ip_pool[update_ind] = get_subnet(to_update, ip)
        return ('update', to_update, ip_pool[update_ind])



class DigitalOcean:
    __token__ = config.get('digitalocean', 'token')
    if not __token__:
        raise ValueError('DigitalOcean token not found. Please set "token" in digitalocean section of config.ini.')
    manager = Manager(token=__token__)
    firewall = manager.get_all_firewalls()[0]
    
    def get_ssr_rules(self):
        return self.firewall.inbound_rules[-1].sources.addresses
    
    def rule_to_json(self, rule: Union[InboundRule, List[InboundRule]]):
        return json.loads(json.dumps(rule, default=lambda o: o.__dict__))
    
    def firewall_to_json(self):
        firewall_dict = self.firewall.__dict__
        res = {
            k: v for k, v in firewall_dict.items() if k in ['name', 'droplet_ids', 'tags']
            }
        res['inbound_rules'] = self.rule_to_json(self.firewall.inbound_rules)
        res['outbound_rules'] = self.rule_to_json(self.firewall.outbound_rules)
        return res
    
    def add_ssr_ip(self, new_ip: str=None):
        if not new_ip:
            new_ip = get_external_ip()
            print('Public IP is retrieved: %s.' % new_ip)
        update_type = merge_into_ip_pool(new_ip, self.firewall.inbound_rules[-1].sources.addresses)
        if update_type[0] == 'new':
            print('New IP %s is appended to IP pools.' % new_ip)
        else:
            print('%s is updated to %s with %s.' % (update_type[1], update_type[2], new_ip))
        print('Result IPs: \n', self.get_ssr_rules())
        
    
    def update(self):
        self.firewall.get_data(
            'firewalls/%s'%self.firewall.id, type=PUT,
            params=self.firewall_to_json()
        )


if __name__ == '__main__':
    obj = DigitalOcean()
    obj.add_ssr_ip()
    obj.update()
    print('SSR IPs are updated automatically!')