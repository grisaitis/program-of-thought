# setup.sh
#!/bin/bash
# Works in codespaces, containers, and local development

set -e  # Exit on error
echo "🚀 Bootstrapping development environment..."

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Install dependencies
if [ -f "pyproject.toml" ]; then
    uv sync --all-extras
    uv run pre-commit install
fi

# Setup git aliases (works locally and in containers)
if [ ! -f ~/.gitalias ]; then
    curl -sSL https://raw.githubusercontent.com/GitAlias/gitalias/main/gitalias.txt > ~/.gitalias
    git config --global include.path ~/.gitalias
fi

echo "✅ Ready to develop!"
