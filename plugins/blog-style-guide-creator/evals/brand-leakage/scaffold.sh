#!/usr/bin/env bash
# Seeds the workspace with the demo brand's guide and one of its own published articles.
set -euo pipefail
case_dir="$(cd "$(dirname "$0")" && pwd)"
demo="$case_dir/../../examples/demo-brand"
mkdir -p brands/demo-brand drafts
cp "$demo/style-guide.md" brands/demo-brand/style-guide.md
cp "$demo/sources/articles/the-dashboard-nobody-opens.md" drafts/the-dashboard-nobody-opens.md
