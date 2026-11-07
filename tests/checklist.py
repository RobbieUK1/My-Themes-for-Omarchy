"""Isolated checks: stock-only discovery, persisted selections, cancellation and bar opt-out."""
import importlib.machinery
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import subprocess

app = importlib.machinery.SourceFileLoader('checklist_app', str(Path(__file__).resolve().parents[1] / 'my-themes')).load_module()
with TemporaryDirectory() as td:
    root = Path(td)
    app.USER_THEMES = root / 'user'
    app.STOCK_LOCATIONS = [root / 'stock']
    app.INCLUDE_FILE = root / 'settings/include.txt'
    app.EXCLUDE_FILE = root / 'settings/exclude.txt'
    for name in ('one', 'two'):
        (root / 'stock' / name).mkdir(parents=True)
    assert app.themes() == []
    def run_checklist(result, status=0):
        with patch.object(app.shutil, 'which', return_value='/mock'), patch.object(app.subprocess, 'run', return_value=subprocess.CompletedProcess([], status, result, '')) as run:
            result = app.manage_stock()
            return result, run.call_args.args[0]
    result, argv = run_checklist('["one"]')
    assert result == 0 and '--multiple' in argv
    assert app.themes() == ['one']  # No user theme directory required.
    result, argv = run_checklist('["one", "two"]')
    assert argv[-2:] == ['--selected', 'one']
    assert app.themes() == ['one', 'two']
    before = app.INCLUDE_FILE.read_bytes()
    assert run_checklist('', 1)[0] == 0
    assert app.INCLUDE_FILE.read_bytes() == before
    assert run_checklist('["not-a-theme"]')[0] == 1
    assert app.INCLUDE_FILE.read_bytes() == before
    app.INCLUDE_FILE.write_text('# keep comment\nmanual-custom\none\ntwo\n')
    assert run_checklist('[]')[0] == 0
    assert app.themes() == []
    assert app.INCLUDE_FILE.read_text() == '# keep comment\nmanual-custom\n'
    # Selected stock and a same-name user overlay are deduplicated, user path wins.
    run_checklist('["one"]')
    (app.USER_THEMES / 'one').mkdir(parents=True)
    (app.USER_THEMES / 'one/colors.toml').touch()
    assert app.themes() == ['one']
    assert app.theme_paths()['one'] == app.USER_THEMES / 'one'
    app.EXCLUDE_FILE.write_text('one\n')
    assert app.themes() == []
    with patch.object(app, 'picker', return_value='Cancel'), patch.object(app.subprocess, 'call') as call:
        assert app.hide_bar() == 0
        call.assert_not_called()
    with patch.object(app, 'picker', return_value='Hide top bar button'), patch.object(app.shutil, 'which', return_value='/mock'), patch.object(app.subprocess, 'call', return_value=0) as call:
        assert app.hide_bar() == 0
        call.assert_called_once_with(['omarchy', 'plugin', 'disable', 'io.github.robbieuk1.my-themes'])
print('PASS: stock checklist, persistence, cancellation, invalid output, clear-all, overlays, exclusions, bar opt-out')
