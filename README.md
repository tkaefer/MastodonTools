## What is this?

A script to add and update domain based blocks to a [Mastodon](https://joinmastodon.org/) instance via the [Mastodon Admin API](https://docs.joinmastodon.org/methods/admin/domain_blocks/)

## Alternatives?

As it seems there will be, see [this pull request on GitHub](https://github.com/mastodon/mastodon/pull/20597).

## What is working
* externalized credentials
* use CSV to import
* add and update blocks

## What is not working
* un block

## How to use

### Create a CSV file 
Use a CSV file with this structure:
```
"domain","when blocked","block reason"
"kenfm.de","taken from fediblock.org","racism, conspiracism, covid denial"
"froth.zone","2022-11-26","harassment, racism"
...
```

### Setup the credentials.yaml file

copy `credentials.yaml.default` to `credentials.yaml`

Update the content appropriately
```
client_id: 'client_id'
client_secret: 'client_secret'
api_base_url: 'https://some.mastodon.instance.url'
username: 'username@email.com'
password: 'user password'
```

### Install dependencies

[install python](https://www.python.org/downloads/)

[install pip3](https://pip.pypa.io/en/stable/installation/) (mostly optional, check your environment)

### Add python dependencies
```
pip3 install Mastodon.py
pip3 install pyyaml
```


### Run the script

```
python3 blockDomains.py -c credentials.yaml -i domainblocks.csv
```


## You found issues?

Thanks for reporting issues and any pull requests
