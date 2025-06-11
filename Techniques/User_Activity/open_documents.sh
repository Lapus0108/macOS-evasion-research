#!/bin/zsh

FILENAMES=(
    "avatar.jpeg"
    "Budget.xlsx"
    "Agreement.doc"
    "dog.jpg"
    "family1.jpg"
    "family2.jpg"
    "Letter.docx"
    "passport.png"
    "Passwords.txt"
    "Presentation.pptx"
)

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

# Populate the system with dummy files of various formats
SOURCE_REPO="https://github.com/Lapus0108/macOS-evasion-research/raw/refs/heads/main/Techniques/User_Activity/Assets/"

TEMP_DIR="/tmp/dummy_assets"
mkdir -p "$TEMP_DIR"

for file in "${FILENAMES[@]}"; do
    temp_file="/$TEMP_DIR/$file"
    curl -s -L -o "$temp_file" "${SOURCE_REPO}${file}"

    if [[ $? -ne 0 ]]; then
        echo "Failed to download $file"
        continue
    fi

    for destination_dir in "${DIRECTORIES[@]}"; do
        cp "$temp_file" "$destination_dir/"
    done
done

rm -rf "$TEMP_DIR"

# Open the files with their default applications
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