import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sgclib import lint  # noqa: E402
from sgclib.article import Article  # noqa: E402


def hits(check, params, text):
    rule = {"id": "T-1", "check": check, "params": params, "scope": "all"}
    return lint.run_rule(rule, Article(text))


def quotes(check, params, text):
    return [(f["quote"], f["replacement"]) for f in hits(check, params, text)]


class TempDir(object):
    def __enter__(self):
        self.path = Path(tempfile.mkdtemp(prefix="sgc-test-"))
        return self.path

    def __exit__(self, *exc):
        shutil.rmtree(str(self.path), ignore_errors=True)
