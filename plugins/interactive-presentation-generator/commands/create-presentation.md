---
description: Generate interactive HTML presentation from materials folder
argument-hint: [presentation-name] [materials-directory] [--style-reference]
---

# Create Interactive Presentation

Generate a self-contained interactive HTML presentation from your materials.

## Step 1: Validate Input Materials

**Required Structure:**
- Materials directory must exist at path: $2
- Look for common subdirectories:
  - `materials/` or `data/` - Source content (reports, transcripts, findings, copy variants)
  - `style/` or `branding/` - Optional brand guidelines or design references

**Validate:**
- Confirm materials directory exists
- Count total files available for presentation
- Identify file types (markdown, JSON, CSV, text, images)
- Check for optional style references at $3 (if provided)

**Report to user:**
```markdown
## 📊 Materials Found

**Directory:** $2
**Files discovered:** [number] files
- Markdown: [count]
- JSON/CSV: [count]
- Images: [count]
- Other: [count]

**Style reference:** [path if $3 provided, or "None - will use default styling"]
```

**Ask user to confirm:** "Would you like to proceed with these materials?"

---

## Step 2: Analyze Content & Propose Structure

Use the **structure-planner agent** to:
- Read all materials from $2
- Identify key themes, data points, and insights
- Propose a logical presentation structure

**The agent should propose:**
1. **Title** for the presentation
2. **Section structure** (3-7 sections recommended)
3. **Content allocation** (which materials go in which section)
4. **Interactive elements** needed (charts, comparisons, tabs, accordions)
5. **Estimated slide/section count**

**Present proposal to user:**
```markdown
## 📋 Proposed Structure

**Title:** [suggested title]

**Sections:**
1. [Section name] - [brief description] - [materials included]
2. [Section name] - [brief description] - [materials included]
3. [etc.]

**Interactive Elements:**
- [Element 1]: [purpose]
- [Element 2]: [purpose]

**Estimated length:** [number] sections

Would you like me to:
1. ✅ Proceed with this structure
2. 🔄 Revise the structure (tell me what to change)
3. ❌ Cancel
```

**Wait for user approval or revision instructions.**

---

## Step 3: Build Content Sections

Once structure is approved, use the **html-generator agent** to:

**For each section:**
1. Extract relevant content from materials
2. Create compelling narrative text
3. Format data for readability (tables, lists, highlights)
4. Identify where interactive elements are needed
5. Generate HTML structure

**Progress reporting:**
```markdown
## 🔨 Building Presentation

- ✅ Section 1: [name] - Complete
- 🔄 Section 2: [name] - In progress
- ⏳ Section 3: [name] - Pending
- ⏳ Section 4: [name] - Pending
```

---

## Step 4: Apply Styling

Use the **style-applier agent** to:

**If style reference provided ($3):**
- Read style guide/brand guidelines
- Extract color schemes, fonts, and visual patterns
- Apply brand-appropriate styling to HTML

**If no style reference:**
- Apply clean, professional default styling
- Use readable fonts and accessible color contrast
- Ensure mobile-responsive layout

**CSS Features to include:**
- Smooth scrolling navigation
- Section transitions
- Print-friendly styles
- Dark mode option (optional)

---

## Step 5: Add Interactive Elements

Use the **interactive-element-creator agent** to add:

**Common interactive elements:**
- **Tabs** - For comparing multiple options/variants
- **Accordions** - For detailed data that can be expanded
- **Charts** - Bar, line, pie charts using Chart.js or similar
- **Filters/Search** - For large datasets
- **Side-by-side comparisons** - For A/B content
- **Tooltips** - For definitions and context

**Show preview of elements to user:**
```markdown
## 🎨 Interactive Elements Added

1. **Section 2:** Tabbed comparison of 3 content variants
2. **Section 3:** Bar chart showing publishing trends
3. **Section 4:** Accordion with detailed findings (12 items)

Would you like to adjust any interactive elements?
```

**Wait for user feedback before finalizing.**

---

## Step 6: Generate Final HTML File

**Create self-contained HTML file:**
- Single file with embedded CSS and JavaScript
- No external dependencies (all scripts inline or from CDNs)
- Optimized for sharing (can be opened directly in browser)

**File naming:**
- Save to: `presentations/[presentation-name].html`
- Or if no presentations/ folder exists: `$1.html` in current directory

**Include in HTML:**
- Metadata (title, author, date)
- Navigation menu (if multiple sections)
- Print button
- Share button (optional)
- Footer with generation date

---

## Step 7: Validation & Delivery

**Validate final HTML:**
- [ ] Opens correctly in browser
- [ ] All interactive elements work
- [ ] No broken links or missing assets
- [ ] Mobile responsive
- [ ] Print-friendly

**Report to user:**
```markdown
## ✅ Presentation Complete!

**File:** presentations/[presentation-name].html
**Sections:** [number]
**Interactive elements:** [number]
**File size:** [size in KB/MB]

**To view:**
1. Open `presentations/[presentation-name].html` in your browser
2. Or drag the file to a browser window

**To share:**
- Email the HTML file directly (self-contained)
- Host on any web server
- Upload to Google Drive/Dropbox and share link

**Next steps:**
- Review content for accuracy
- Test interactive elements
- Share with stakeholders
```

---

## Error Handling

**If materials directory doesn't exist:**
```
❌ Materials directory not found: $2

Please provide a valid directory path containing your materials.

Example structure:
  my-presentation/
    ├── materials/
    │   ├── report.md
    │   ├── data.csv
    │   └── findings.txt
    └── style/
        └── brand-guide.md
```

**If insufficient materials:**
```
⚠️ Warning: Only [number] files found

Interactive presentations work best with multiple materials (3+ files).

Would you like to:
1. Proceed anyway (may result in short presentation)
2. Add more materials first
```

**If HTML generation fails:**
- Save partial progress
- Report which section failed
- Offer to retry that section only

---

## Usage Examples

```bash
# Basic presentation from materials folder
/create-presentation content-audit ./audit-materials/

# With style reference
/create-presentation q4-report ./reports/q4/ --style-reference ./brand/style-guide.md

# From nested directory structure
/create-presentation competitor-analysis ./research/competitive/materials/
```

---

## Tips for Best Results

**Materials organization:**
- Use clear, descriptive file names
- Group related materials in subdirectories
- Include images/charts if available
- Provide context documents (ICP, strategy docs)

**Style references:**
- Brand guidelines work well
- Previous presentations can serve as style examples
- Color hex codes and font names are helpful

**Interactive elements:**
- Use tabs for side-by-side comparisons (up to 5 variants)
- Use accordions for lists of 6+ items
- Use charts for numerical trends
- Keep it simple - don't over-complicate
