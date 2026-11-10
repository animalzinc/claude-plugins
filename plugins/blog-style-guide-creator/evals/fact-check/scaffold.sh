#!/usr/bin/env bash
# Seeds the workspace with the demo brand's guide and a short draft with two planted factual errors.
set -euo pipefail
case_dir="$(cd "$(dirname "$0")" && pwd)"
demo="$case_dir/../../examples/demo-brand"
mkdir -p brands/demo-brand drafts
cp "$demo/style-guide.md" brands/demo-brand/style-guide.md
cp "$case_dir/fixtures/example-domains.md" drafts/example-domains.md
