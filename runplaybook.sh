#!/bin/bash

while true; do
    echo -e "\nAnsible Playbook Runner"
    echo "#######################"
    
    # 1. Get Lab Number
    read -p "Enter lab number (1/2) or 'q' to quit: " lab
    [[ "$lab" == "q" ]] && break

    # 2. Get OS via numeric choice
    echo -e "\nSelect Operating System:"
    echo "1) Windows"
    echo "2) Linux"
    read -p "Choice (1/2): " os_choice

    case $os_choice in
        1) os="windows" ;;
        2) os="linux" ;;
        *) echo "Invalid choice. Please select 1 or 2."; continue ;;
    esac

    # Inner loop for playbooks within the selected OS
    while true; do
        echo -e "\nAvailable playbooks for $os:"
        ls -1 "playbook/$os"
        echo "#######################"

        # 3. Get Playbook, Host, and Tags
        read -p "Enter playbook number (e.g., 1, 2) or 'b' to go back: " pb
        [[ "$pb" == "b" ]] && break

        read -p "Enter hostname (press Enter for 'all'): " host
        read -p "Enter tags (press Enter to skip): " tags

        # 4. Find the specific playbook file
        PB_FILE=$(ls playbook/$os/$pb-*.yml 2>/dev/null)

        if [ -z "$PB_FILE" ]; then
            echo "Error: Playbook for number '$pb' not found in playbook/$os/."
            continue
        fi

        # 5. Fix for [ERROR]: Keyword 'hosts' is required
        # If user input for host is empty, we explicitly set it to 'all'
        if [ -z "$host" ]; then
            target="all"
        else
            target="$host"
        fi

        # 6. Build and Execute command
        CMD="ansible-playbook -i inventory/lab$lab-$os-inventory.yml $PB_FILE -e target_host=$target"
        
        if [ -n "$tags" ]; then
            CMD="$CMD --tags=$tags"
        fi

        echo -e "\nExecuting: $CMD\n"
        eval $CMD

        # 7. Ask to stay in this OS or go back
        echo -e "\nExecution finished."
        read -p "Run another playbook for $os? (y/n): " again
        [[ "$again" != "y" ]] && break
    done
done

echo "Exiting. Goodbye!"
