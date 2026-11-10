#!/usr/bin/env bash
# Seeds the workspace with the demo brand's guide and its seeded draft.
set -euo pipefail
case_dir="$(cd "$(dirname "$0")" && pwd)"
demo="$case_dir/../../examples/demo-brand"
mkdir -p brands/demo-brand drafts
cp "$demo/style-guide.md" brands/demo-brand/style-guide.md
cp "$demo/drafts/seeded-draft.md" drafts/seeded-draft.md
