#!/usr/bin/env bash
# MD2PPT Global Skill Installer
# Run from the MD2PPT repo root after any update to skills or design-profiles.
# Usage: bash install.sh

set -e

MD2PPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_SKILLS="$HOME/.claude/skills"
CODEX_SKILLS="$HOME/.codex/skills"

install_to() {
  local dest="$1"
  if [ ! -d "$dest" ]; then
    echo "  ⚠️  $dest does not exist — skipping"
    return
  fi

  # deck-builder (includes bundled design-profiles)
  rm -rf "$dest/deck-builder"
  cp -r "$MD2PPT/skills/deck-builder" "$dest/"
  cp -r "$MD2PPT/design-profiles" "$dest/deck-builder/"

  # ui-ux-pro-max
  rm -rf "$dest/ui-ux-pro-max"
  cp -r "$MD2PPT/skills/ui-ux-pro-max" "$dest/"

  echo "  ✓  deck-builder + ui-ux-pro-max → $dest"
}

echo "MD2PPT skill installer"
echo "Source: $MD2PPT"
echo ""

mkdir -p "$CLAUDE_SKILLS"
install_to "$CLAUDE_SKILLS"
install_to "$CODEX_SKILLS"

echo ""
echo "Done. Open a new Claude Code session for the updated skills to take effect."
echo ""
echo "Installed skills:"
echo "  ~/.claude/skills/deck-builder/           (deck-builder + design-profiles bundled)"
echo "  ~/.claude/skills/ui-ux-pro-max/           (design intelligence)"
