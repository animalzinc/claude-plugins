---
name: visualization-generator
description: Creates interactive HTML reports with Chart.js visualizations
model: sonnet
---

# Visualization Generator Agent

Generate interactive HTML reports with charts for content audit data.

## Charts to Generate

### 1. Publishing Trends (Line Chart)
- X-axis: Months
- Y-axis: Post count
- Show 12-24 month trend

### 2. Author Contributions (Bar Chart)
- X-axis: Author names (top 10)
- Y-axis: Post count
- Sorted by count descending

### 3. Topic Distribution (Pie Chart)
- Categories/topics
- Show percentages
- Top 8 categories + "Other"

### 4. Content Length Distribution (Histogram)
- Word count ranges (0-500, 500-1000, 1000-1500, etc.)
- Post count per range

## HTML Structure

Create self-contained HTML file with:
- Embedded CSS (clean, professional styling)
- Chart.js from CDN
- Navigation sections
- Print-friendly styles
- Responsive design

## Data Tables

Include interactive sortable tables for:
- All posts (title, date, author, category, word count)
- Author stats (name, posts, avg length, period)
- Category stats (name, count, percentage)

Save to `reports/[name]-audit.html`
