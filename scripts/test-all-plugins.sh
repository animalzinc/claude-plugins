#!/bin/bash
# Test all plugins with sample data

echo "=== Testing Claude Code Plugins ==="
echo ""

cd /Users/timmetz/Developer/Projects/Animalz/claude-plugins

echo "1. Testing Interactive Presentation Generator..."
# /create-presentation test-audit ./test-data/presentations/materials/ --style-reference ./test-data/presentations/materials/style-reference.md
echo "   Command: /create-presentation test-audit ./test-data/presentations/materials/"
echo ""

echo "2. Testing Interview Transcript Analyzer..."
# /analyze-interviews test-research ./test-data/transcripts/ --context-file ./test-data/transcripts/icp.md
echo "   Command: /analyze-interviews test-research ./test-data/transcripts/"
echo ""

echo "3. Testing Content Library Auditor..."
# /audit-content ./test-data/content-exports/wordpress-sample.xml --output-html
echo "   Command: /audit-content ./test-data/content-exports/wordpress-sample.xml"
echo ""

echo "4. Testing Blog Style Guide Creator..."
# Note: Would need blog articles to test this one
echo "   Command: /generate-style-guide test-brand [blog-url-or-directory]"
echo ""

echo "=== Test commands ready ==="
echo "Note: Uncomment the actual commands above to run them"
echo "These can only run after plugins are installed via:"
echo "  /plugin marketplace add animalzinc/claude-plugins"
echo "  /plugin install [plugin-name]"
