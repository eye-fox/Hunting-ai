#!/bin/bash
set -e

# Install OpenCode
curl -fsSL https://opencode.ai/install | bash

# Buat direktori auth
mkdir -p ~/.local/share/opencode

# Baca prompt dari file prompt.txt
PROMPT=$(cat prompt.txt)

# Jalankan OpenCode dengan isi prompt.txt
~/.opencode/bin/opencode run "$PROMPT" -m opencode/laguna-s-2.1-free --auto
