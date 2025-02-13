#!/bin/bash

# Define script path
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_PATH="$INSTALL_DIR/tf"

# Ensure ~/.local/bin exists
mkdir -p "$INSTALL_DIR"

# Create the script
cat << 'EOF' > "$SCRIPT_PATH"
#!/bin/bash
runner=$(which terraform || which tofu)

if [ -z "$runner" ]; then
    echo "Neither Terraform nor OpenTofu are installed. Exiting..."
    exit 1
fi

if [ -f ../config.json ];then
    echo "Please create a config.json file in the repository root."
    echo "This file SHOULD NOT be committed to version control."
    echo "Follow the template 'template.json'."
else
    "$runner" "$@"
fi
EOF

# Make it executable
chmod +x "$SCRIPT_PATH"

# Ensure ~/.local/bin is in PATH
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo "Added ~/.local/bin to PATH. Restart your terminal or run: source ~/.bashrc"
else
    echo "~/.local/bin is already in PATH"
fi

echo "Installation complete. You can now use 'tf' as a command."
