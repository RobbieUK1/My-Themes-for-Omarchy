#!/usr/bin/env bash
set -euo pipefail
command -v python3 >/dev/null || { echo "Python 3 is required." >&2; exit 1; }
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
install -Dm755 "$HERE/my-themes" "$HOME/.local/bin/my-themes"
mkdir -p "$HOME/.config/my-themes-omarchy" "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/my-themes-omarchy.desktop" <<EOF
[Desktop Entry]
Name=My Themes for Omarchy
Comment=Choose from your installed custom Omarchy themes
Exec="$HOME/.local/bin/my-themes"
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;
Icon=preferences-desktop-theme
Actions=ManageStock;Previews;

[Desktop Action ManageStock]
Name=Choose pre-installed themes
Exec="$HOME/.local/bin/my-themes" --manage-stock

[Desktop Action Previews]
Name=Wallpaper previews
Exec="$HOME/.local/bin/my-themes" --previews
EOF
printf 'Installed: %s\n' "$HOME/.local/bin/my-themes"
printf 'Launch "My Themes for Omarchy" from the app launcher, or run %s/.local/bin/my-themes\n' "$HOME"
