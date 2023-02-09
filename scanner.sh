#!/bin/bash -eu

website=$(redis-cli LPOP websites)
subdomains="$(~/go/bin/subfinder -d \"$website\" -all -silent)"
~/go/bin/nuclei -ut -silent

for subdomain in $subdomains
do
  result=$(~/go/bin/nuclei -u "$subdomain" -silent -nc)
  redis-cli RPUSH "$website" "$subdomain@@@@$result"
done

cd ~/PycharmProjects/VulScan/
./venv/bin/python manage.py submit "$website"