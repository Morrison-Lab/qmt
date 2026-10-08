#!/usr/bin/env python3
"""
Script to add banners to pages with links to alternative formats and changed pages.
"""

import os
import sys
import json
import re
from pathlib import Path

# Markers gha's preview step writes into a page it highlights (gha
# preview/highlight-html-changes.py) and into the home page when its own
# changed-chapters banner is on (gha preview/add-home-banner.py).
GHA_PAGE_BANNER = "<!-- gha-preview-page-banner:start -->"
GHA_HOME_BANNER = "<!-- gha-preview-banner:start -->"


def get_page_title(html_path):
    """Extract the page title from an HTML file."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for h1 heading with or without chapter number
            h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
            if h1_match:
                title_html = h1_match.group(1)
                # Remove chapter number span if present
                title_html = re.sub(r'<span class="chapter-number">(\d+)</span>\s*', '', title_html)
                # Strip HTML tags
                title = re.sub(r'<[^>]+>', '', title_html).strip()
                return title
            # Fall back to title tag
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                return title_match.group(1).strip()
    except Exception as e:
        print(f"  Warning: Could not extract title from {html_path}: {e}", file=sys.stderr)
    return html_path.stem

def add_page_banner(html_path, html_dir, changed_pages):
    """Add banners to a page with links to its alternative formats and changed pages."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Calculate the relative path from html_dir
    try:
        rel_path = html_path.relative_to(html_dir)
    except ValueError:
        print(f"Warning: {html_path} is not under {html_dir}", file=sys.stderr)
        return
    
    # Get the stem (filename without extension)
    stem = html_path.stem
    
    banners = []
    
    # Banner 1: Changed pages (if any exist). Skip it on a page that already
    # carries gha's own home-page banner, so the list never appears twice.
    if changed_pages and GHA_HOME_BANNER not in html:
        page_links = []
        for page_info in changed_pages:
            page_rel_path = page_info['rel_path']
            page_html_path = html_dir / page_rel_path
            
            # Calculate relative link from current page to changed page
            try:
                current_dir = html_path.parent
                link_path = os.path.relpath(page_html_path, current_dir)
                page_links.append(f'<a href="{link_path}">{page_info["title"]}</a>')
            except Exception as e:
                print(f"  Warning: Could not create link to {page_rel_path}: {e}", file=sys.stderr)
        
        if page_links:
            links_html = ', '.join(page_links)
            banners.append(f'''
<div class="preview-changes-banner" style="background-color: #fff3cd; border: 1px solid #ffc107; border-radius: 4px; padding: 12px; margin: 16px 0;">
    <p style="margin: 0;">
        <strong>📋 Changes in this PR:</strong> {links_html}
        <br>
        <strong>💡 Tip:</strong> If change highlighting is glitchy, add the <code>no-preview-highlights</code> label to this PR to disable it.
    </p>
</div>
''')
    
    # Banner 2: This page's alternative formats
    # Construct paths to alternative formats relative to the HTML file's directory
    docx_tracked_file = f"{stem}-tracked-changes.docx"
    slides_file = f"{stem}-slides.html"
    
    # Build the banner with links to alternative formats
    links = []
    
    # Check if tracked changes DOCX exists - prioritize this over regular DOCX
    docx_tracked_path = html_path.parent / docx_tracked_file
    if docx_tracked_path.exists():
        links.append(f'<a href="{docx_tracked_file}" download>📝 MS Word (tracked changes)</a>')
    
    # Check if slides file exists
    slides_path = html_path.parent / slides_file
    if slides_path.exists():
        links.append(f'<a href="{slides_file}">🎞️ Slides</a>')
    
    if links:
        links_html = ' | '.join(links)
        banners.append(f'''
<div class="preview-page-formats-banner" style="background-color: #e7f3ff; border: 1px solid #b3d9ff; border-radius: 4px; padding: 12px; margin: 16px 0;">
    <p style="margin: 0;">
        <strong>📋 Other Formats:</strong> {links_html}
    </p>
</div>
''')
    
    # Only modify if we have at least one banner
    if not banners:
        print(f"  No banners to add for {rel_path}")
        return
    
    combined_banners = '\n'.join(banners)
    
    # Find insertion point (after <main> tag)
    main_match = re.search(r'(<main[^>]*>)', html)
    if main_match:
        insertion_point = main_match.end()
        html = html[:insertion_point] + combined_banners + html[insertion_point:]
        
        # Write back
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  Added {len(banners)} banner(s) to {rel_path}")
    else:
        print(f"  Could not find insertion point for {rel_path}", file=sys.stderr)

def main():
    # Get the HTML directory
    html_dir = Path(os.getenv('HTML_DIR', './_site'))
    
    if not html_dir.exists():
        print(f"HTML directory {html_dir} does not exist", file=sys.stderr)
        return
    
    print("="*60)
    print("Adding Format Banners to Pages")
    print("="*60)
    
    # gha writes a tracked-changes DOCX for every DOCX it finds, changed or not
    # (preview/create-docx-tracked-changes.py), so the DOCX files cannot say
    # which pages changed. gha's highlighter marks each page it finds modified
    # or new, so the changed pages are the HTML files carrying that marker.
    # Nothing is marked while the `no-preview-highlights` label is on.
    changed_pages = []
    for html_file in sorted(html_dir.rglob('*.html')):
        try:
            if GHA_PAGE_BANNER not in html_file.read_text(encoding='utf-8'):
                continue
            changed_pages.append({
                'rel_path': html_file.relative_to(html_dir),
                'stem': html_file.stem,
                'title': get_page_title(html_file),
                'html_path': html_file
            })
        except Exception as e:
            print(f"  Warning: Could not process {html_file}: {e}", file=sys.stderr)

    if changed_pages:
        print(f"\nFound {len(changed_pages)} changed page(s):")
        for page in changed_pages:
            print(f"  - {page['title']} ({page['rel_path']})")
    else:
        print("\nNo changed pages detected (no page carries gha's highlight marker)")
        if os.getenv("HIGHLIGHT_CHANGES") == "true":
            print("::warning::Highlighting is on but no page carries gha's highlight marker; if the PR changes pages, gha may have renamed it.")
    
    # Find all HTML files recursively
    html_files = list(html_dir.rglob('*.html'))
    
    if not html_files:
        print(f"No HTML files found in {html_dir}")
        return
    
    print(f"\nProcessing {len(html_files)} HTML file(s)")
    
    # Process each HTML file
    for html_file in html_files:
        add_page_banner(html_file, html_dir, changed_pages)
    
    print("\n" + "="*60)
    print("Format banner addition complete")
    print("="*60)

if __name__ == '__main__':
    main()
