# setup.sh
#!/bin/bash
# Works in codespaces, containers, and local development

set -e  # Exit on error
echo "🚀 Bootstrapping development environment..."

# Navigate to project root
cd $(git rev-parse --show-toplevel)

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Install dependencies
if [ -f "pyproject.toml" ]; then
    echo "calling uv sync..."
    uv sync --all-extras
    echo "calling uv run pre-commit install..."
    uv run pre-commit install
    echo "checking secrets baseline..."
    ./scripts/create_or_update_baseline_secrets.sh
fi

# Setup git aliases (only in codespaces containers)
if [ "$CODESPACES" = "true" ]; then
    echo "Setting up git aliases..."
    if [ ! -f ~/.gitalias ]; then
        curl -sSL https://raw.githubusercontent.com/GitAlias/gitalias/main/gitalias.txt > ~/.gitalias
        echo "Created ~/.gitalias with default git aliases."
        echo $(ls -l ~/.gitalias)
        git config --global include.path ~/.gitalias
    fi
fi

echo "✅ Ready to develop!"
