#!/bin/bash
TMP_FILE=$(mktemp)

pip freeze > "$TMP_FILE"

if ! cmp -s "$TMP_FILE" requirements.txt; then
    mv "$TMP_FILE" requirements.txt
    echo "requirements.txt updated."
else
    rm "$TMP_FILE"
fi


chmod +x scripts/update_requirements.sh
