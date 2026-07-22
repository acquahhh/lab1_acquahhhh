#!/bin/bash
#
# organizer.sh - Archives grades.csv with a timestamp, resets the workspace,
#                and logs every action.
#
# Usage: ./organizer.sh
#

set -euo pipefail

ARCHIVE_DIR="archive"
SOURCE_FILE="grades.csv"
LOG_FILE="organizer.log"

# 1. Ensure the archive directory exists
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi

# 2. Generate a timestamp (format: YYYYMMDD-HHMMSS)
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# 3. Archival process
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi

ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
mv "$SOURCE_FILE" "$ARCHIVE_DIR/$ARCHIVED_NAME"
echo "Archived '$SOURCE_FILE' -> '$ARCHIVE_DIR/$ARCHIVED_NAME'"

# 4. Workspace reset: create a fresh, empty grades.csv
touch "$SOURCE_FILE"
echo "Created a fresh empty '$SOURCE_FILE'."

# 5. Logging: append this operation's details
echo "[$TIMESTAMP] Original: $SOURCE_FILE | Archived as: $ARCHIVE_DIR/$ARCHIVED_NAME" >> "$LOG_FILE"
echo "Logged operation to '$LOG_FILE'."
