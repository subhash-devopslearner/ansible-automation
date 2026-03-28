#!/bin/bash

echo "Running send message to student playbook"
echo "########################################"

# 1. Ask for system numbers (target hosts)
#read -p "Enter the target system number (e.g., cc1-1, pl-1): " target_input
target_input=$1

# 2. Ask for the custom message
default_msg="Attention: Please do your lab work. Focus on learning."
#read -p "Enter the message to send (Press Enter for default): " message_input
message_input=$2

# Use default message if input is empty
final_msg="${message_input:-$default_msg}"

# 3. Run the playbook with extra variables
# Extra vars have the highest precedence and will override variables in the playbook

cd ~/ansible-automation && source venv/bin/activate && ansible-playbook -i inventory/lab1-windows-inventory.yml playbook/windows/17-send-message-to-users.yml -e "target_host=$target_input custom_msg='$final_msg'"

# 4. Deactivate venv after execution
deactivate

# 4. Exit
exit
