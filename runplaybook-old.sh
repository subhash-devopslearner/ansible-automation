#!/bin/bash

echo "Ansible Playbook Runner"
echo "#######################"

# 1. Get Lab and OS
read -p "Enter lab number (1/2): " lab
read -p "Enter OS (windows/linux): " os

# 2. List available playbooks for that OS
echo -e "\nAvailable playbooks for $os:"
ls -1 "playbook/$os"
echo "#######################"

# 3. Get Playbook, Host, and Tags
read -p "Enter playbook number (e.g., 1,2,3): " pb
read -p "Enter hostname: " host
read -p "Enter tags (press Enter to skip): " tags

# 4. Find the specific playbook file
# This handles the wildcard expansion correctly
PB_FILE=$(ls playbook/$os/$pb-*.yml 2>/dev/null)

if [ -z "$PB_FILE" ]; then
    echo "Error: Playbook playbook/$os/$pb-*.yml not found."
    exit 1
fi

# 5. Build the command dynamically
# We only add the --tags flag if the user actually typed something
CMD="ansible-playbook -i inventory/lab$lab-$os-inventory.yml $PB_FILE -e target_host=$host"

if [ -n "$tags" ]; then
    CMD="$CMD --tags=$tags"
fi

# 6. Execute
echo -e "\nExecuting: $CMD\n"
eval $CMD
