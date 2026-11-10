#!/usr/bin/env bash
# Seeds the workspace with a version 1 guide and a draft that breaks several of its rules.
set -euo pipefail
case_dir="$(cd "$(dirname "$0")" && pwd)"
fixtures="$case_dir/../../tests/fixtures"
mkdir -p brands/demo-co drafts
cp "$fixtures/guide-v1.md" brands/demo-co/style-guide.md
cp "$fixtures/article-violations.md" drafts/strong-wind.md
