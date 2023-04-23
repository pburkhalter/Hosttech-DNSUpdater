import platform
import argparse
import requests
import yaml
from os import getenv
from datetime import datetime


parser = argparse.ArgumentParser(description='Simple DNS update-service for the hosttech API')

parser.add_argument('--domain', metavar='domain', type=str, dest='domain',
                    default=getenv('HTUPD_DOMAIN'),
                    help='The domain (zone) to update')

parser.add_argument('--record', metavar='record', type=int, dest='record',
                    default=getenv('HTUPD_RECORD'),
                    help='The record of the specified sub-domain')

parser.add_argument('--token', metavar='token', type=str, dest='token',
                    default=getenv('HTUPD_TOKEN'),
                    help='The token needed to access the API')

parser.add_argument('--subdomain', metavar='subdomain', type=str, dest='subdomain',
                    default=getenv('HTUPD_SUBDOMAIN'),
                    help='The subdomain to update')

parser.add_argument('--ttl', metavar='ttl', type=str, dest='ttl',
                    default=getenv('HTUPD_TTL'),
                    help='TTL (time to live) in seconds (default 3600)')

parser.add_argument('--url', metavar='url', type=str, dest='url',
                    default=getenv('HTUPD_URL'),
                    help='The base-url for the hosttech API (optional)')

args = vars(parser.parse_args())


with open(r'/config/token', 'a+') as token_file:
    token_file.seek(0)
    if len(token_file.read()) == 0:
        if not args.get('token'):
            raise IndexError('Missing token! Exiting...')

        token_file.write(args.get('token'))
        token = args.pop('token')
    else:
        token_file.seek(0)
        token = token_file.read(-1)

with open(r'/config/conf.yaml', 'a+') as config_file:
    config_file.seek(0)
    if len(config_file.read()) == 0:
        if not all(key in args.keys() for key in ['record', 'domain', 'subdomain']):
            raise IndexError('Missing arguments! Exiting...')

        yaml.dump(args, config_file, default_flow_style=False)
        config = args
    else:
        config_file.seek(0)
        config = yaml.safe_load(config_file)


def get_public_ip():
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    return ip


def create_api_client(token):
    client = requests.Session()
    client.headers.update({'Authorization': f'Bearer {token}'})
    client.headers.update({'Content-Type': 'application/json'})
    client.headers.update({'Accept': 'application/json'})
    client.headers.update({'User-Agent': 'Custom-API-Client/Python' + platform.python_version()})
    return client


def update_dns_record(token, domain, subdomain, record, url, ttl):
    client = create_api_client(token)
    ip = get_public_ip()
    date_time = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

    record_response = client.put(url + domain + '/records/' + str(record), json={
        'name': subdomain,
        'ipv4': ip,
        'ttl': ttl,
        'comment': 'Last Update: ' + date_time + " (API-Client)"
    })

    if record_response.status_code != 200:
        print("Error updating IP (" + ip + ") for " + ".".join([subdomain, domain]))
        print("Status Code: " + str(record_response.status_code))
        print("Reason: " + record_response.reason)
    else:
        print("IP (" + ip + ") updated successfully for " + ".".join([subdomain, domain]) + " at " + date_time)


if __name__ == "__main__":
    update_dns_record(
        token=token,
        domain=config.get('domain'),
        subdomain=config.get('subdomain'),
        record=config.get('record'),
        url=config.get('url'),
        ttl=config.get('ttl')
    )
