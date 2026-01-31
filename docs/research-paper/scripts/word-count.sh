#!/bin/bash
# Word Count Tracking Script for Research Paper

PAPER_FILE="${1:-docs/research-paper/ai-k12-efficiency-paper.md}"

if [ ! -f "$PAPER_FILE" ]; then
    echo "Error: Paper file not found at $PAPER_FILE"
    exit 1
fi

# Count words excluding YAML frontmatter and markdown formatting
word_count=$(sed '/^---$/,/^---$/d' "$PAPER_FILE" | \
             sed 's/^#\+\s*//g' | \
             sed 's/\*\*//g' | \
             sed 's/__//g' | \
             sed 's/\*//g' | \
             sed 's/_//g' | \
             wc -w)

echo "==================================="
echo "Research Paper Word Count"
echo "==================================="
echo "File: $PAPER_FILE"
echo "Word Count: $word_count"
echo ""
echo "Target Range: 3,000 - 5,000 words"
echo ""

if [ "$word_count" -lt 3000 ]; then
    remaining=$((3000 - word_count))
    echo "Status: UNDER TARGET"
    echo "Need to add: $remaining words"
elif [ "$word_count" -gt 5000 ]; then
    excess=$((word_count - 5000))
    echo "Status: OVER TARGET"
    echo "Need to reduce: $excess words"
else
    echo "Status: ✓ WITHIN TARGET RANGE"
fi

echo "==================================="
