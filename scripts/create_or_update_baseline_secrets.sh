#!/bin/bash

set -e  # Exit on error

# Generate or update baseline
if [ -f ".secrets.baseline" ]; then
    echo "Updating existing baseline..."
    uv run detect-secrets scan \
        --baseline .secrets.baseline \
        --exclude-files '\.env$' \
        --exclude-files '\.venv/' \
        --update
else
    echo "Creating new baseline..."
    uv run detect-secrets scan \
        --exclude-files '\.env$' \
        --exclude-files '\.venv/' \
        > .secrets.baseline
fi
