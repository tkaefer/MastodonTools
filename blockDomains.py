import sys , getopt, csv, yaml
from mastodon import Mastodon
from pathlib import Path

def check_is_file(file_name: str):
    path = Path(file_name)
    if not path.is_file():
        print (f'The file {file_name} does not exist')
        sys.exit()




def main(argv):
    input_file = ''
    credentials_file = ''
    opts, args = getopt.getopt(argv,"hi:c:")
    for opt, arg in opts:
        if opt == '-h':
            print ('blockDomains.py -c <credentials file> -i <inputfile>')
            sys.exit()
        elif opt in ("-i"):
            input_file = arg
        elif opt in ("-c"):
            credentials_file = arg

    check_is_file(input_file)
    check_is_file(credentials_file)

    with open(credentials_file, 'r') as stream:
        credentials = yaml.safe_load(stream)

    
    mastodon = Mastodon (
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        api_base_url=credentials['api_base_url']
    )

    mastodon.access_token = mastodon.log_in (
        username=credentials['username'],
        password=credentials['password'],
        scopes=['admin:read', 'admin:write']
    )


    domain_blocks = mastodon.admin_domain_blocks()
    domain_blocks = mastodon.fetch_remaining(domain_blocks)

    domain_dict = dict(map(lambda x: (x['domain'], x['id']), domain_blocks))

    with open(input_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                domain_to_block=repr(row['domain'].encode('idna'))
                print(domain_to_block)
                public_comment=f'{row["block reason"]} {row["when blocked"]}'
                obfuscate=row['obfuscate'].lower() in ['true', '1', 't', 'y', 'yes'] or False
                if domain_to_block in list(domain_dict.keys()):
                    print(f'update {row}')
                    block_id=domain_dict[domain_to_block]
                    result = mastodon.admin_update_domain_block(id=block_id, severity='suspend', public_comment=public_comment) 
                    print(result)
                else:
                    print(f'add {row}')
                    result = mastodon.admin_create_domain_block(domain=domain_to_block, severity='suspend', public_comment=public_comment) 
                    print(result)
                    domain_dict[result['domain']] = result['id']
            line_count += 1        



# print (json.dumps(domain_names, indent=4, default=str))
if __name__ == "__main__":
   main(sys.argv[1:])




