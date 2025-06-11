#!/bin/zsh

# Populate the system with dummy files of various formats




EXTENSIONS=(
    "pdf" 
    "txt" 
    "xls" 
    "xlsx" 
    "doc"
    "docx" 
    "pptx" 
    "png"
    "jpg"
    "csv"
)

DIRECTORIES=(
    "$HOME/Desktop"
    "$HOME/Documents" 
    "$HOME/Downloads"
)

count=0

for dir in "${DIRECTORIES[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Directory $dir not found."
        continue
    fi

    for file in "$dir"/*; do
        if [ -f "$file" ]; then
            if [[ " ${EXTENSIONS[@]} " =~ " ${file##*.} " ]]; then
                open "$file" &

                ((count++))

                if [ "$count" -ge 10 ]; then
                    break 2
                fi
            fi
        fi
    done
done