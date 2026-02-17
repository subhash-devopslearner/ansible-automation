#!/bin/bash

echo "Run the ansible playbook"
echo "#######################"

echo "Enter lab number 1/2: "
read lab

echo "Enter OS windows/linux"
read os

ls -1 playbook/$os

echo "#######################"

echo "Enter playbook number..."
read pb
echo "Enter hostname..."
read host

ansible-playbook -i inventory/lab$lab-$os-inventory.yml playbook/$os/$pb-*.yml -e target_host=$host
