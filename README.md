# My Themes for Omarchy

A lightweight, searchable picker for your custom Omarchy themes. Python standard library only. Built-in themes and the original picker remain untouched.

**[Download v0.1 ZIP](https://github.com/RobbieUK1/My-Themes-for-Omarchy/releases/download/v0.1/My-Themes-for-Omarchy-v0.1.zip)** · **[Release notes](https://github.com/RobbieUK1/My-Themes-for-Omarchy/releases/tag/v0.1)**

![My Themes for Omarchy showing custom themes and the active theme](preview.png)

Screenshot supplied by RobbieUK1.

## Omarchy shell plugin (v0.1.1)

Install the native bar button on Omarchy Quattro:

```bash
omarchy plugin add https://github.com/RobbieUK1/My-Themes-for-Omarchy --enable
```

Left-click **My Themes** to search custom themes. Right-click for wallpaper thumbnails. The bundled Python utility runs directly from the plugin folder; you do not need to run install.sh. Only one picker per bar button runs at a time. The button uses Omarchy's own styling and English strings with translation fallback.

Requires Omarchy Quattro's shell, Python 3 and the native menu commands. No Python packages, network polling, administrator permissions, theme rewrites or replacement of the original picker. Adding/enabling uses Omarchy's normal consent and bar-placement flow. Removing the plugin removes only its own widget and checkout:

```bash
omarchy plugin disable io.github.robbieuk1.my-themes
omarchy plugin remove io.github.robbieuk1.my-themes
```

License: MIT. Marketplace submission is subject to maintainer review. The native wrapper is validated with Omarchy's manifest validator; live graphical behavior of the new bar button has not yet been visually verified. The standalone v0.1 picker has been confirmed working by its user.

## Standalone install (v0.1)

Run this one-line command as your normal user (no sudo). Requires Bash, curl, unzip and Python 3:

```bash
bash -c 'set -euo pipefail; d=$(mktemp -d); trap '\''rm -rf "$d"'\'' EXIT; curl -fL https://github.com/RobbieUK1/My-Themes-for-Omarchy/releases/download/v0.1/My-Themes-for-Omarchy-v0.1.zip -o "$d/themes.zip"; unzip -q "$d/themes.zip" -d "$d"; bash "$d/my-themes-omarchy/install.sh"'
```

Or extract the ZIP and run `bash install.sh` inside `my-themes-omarchy`.

Launch **My Themes for Omarchy** from your application launcher or run `~/.local/bin/my-themes`. If `~/.local/bin` is on PATH, use `my-themes`.

## Search and previews

The default menu uses Omarchy's native searchable menu on current releases, then falls back to Fuzzel, Rofi, Wofi, or a numbered terminal menu on older systems. The active theme is marked `[active]`.

```text
My Themes for Omarchy
  babylon-berlin
  [active] murder-of-crows
  person-of-interest-electronic-blue
  sunny-oled
```

This is an illustrative text preview, not a desktop screenshot.

Run `my-themes --previews` for Omarchy's native searchable wallpaper thumbnail picker. It uses each theme's preview.png/preview.jpg or its first supported wallpaper, including user background overrides. If any theme lacks an image, it returns to the complete list so no theme becomes inaccessible. Requires `omarchy-menu-images` and its normal Omarchy dependencies; no additional Python packages. Escape cancels.

## Theme discovery

Automatically scans `~/.config/omarchy/themes/`, including symlinked custom themes. Recognizes colors.toml, alacritty.toml, preview.png, backgrounds or .git. Themes matching names in Omarchy's bundled theme directories are hidden by default, including stock-name overlays. Does not move, delete, update or rewrite themes. Switching delegates to `omarchy theme set <slug>` (legacy `omarchy-theme-set` fallback).

Use `my-themes --list` to inspect discovered slugs. For a deliberately customized stock-name overlay, add its slug to `~/.config/my-themes-omarchy/include.txt`, one per line. `exclude.txt` always hides matching entries. Blank lines and comments beginning with # are ignored.

## Compatibility and verification

Reviewed against Omarchy 4.5.0-3 installed command sources and current upstream theme-set/theme-list scripts on 7 November 2026. The old picker did not support the native menu and compared display names against slugs; both are corrected. Automated isolated checks cover filtering, active labels, validated switching, cancellation, preview mapping and installation/uninstallation. No live theme switch is performed during verification. Graphical appearance depends on your Omarchy theme and menu backend; interactive desktop behavior has not been visually verified.

Installer writes only `~/.local/bin/my-themes`, its own configuration directory and its own application launcher entry. It does not alter bindings, Omarchy menus, packaged files or update behavior. Re-running it updates this utility.

## Uninstall

Run `bash uninstall.sh` from an extracted download. Keeps all themes and personal utility settings. No keyboard bindings are installed automatically.
