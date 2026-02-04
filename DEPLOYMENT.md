# DEPLOYMENT INSTRUCTIONS

Dr. Carter, follow these exact steps to deploy the new system.

## Step 1: Backup Old System (30 seconds)

In your terminal at `C:\crownwell-publishing`:

```cmd
git checkout -b archive-old-system
git add .
git commit -m "Archive old HTML pipeline before migration"
git push -u origin archive-old-system
```

**Purpose**: This creates a backup branch. If anything goes wrong, you can recover.

---

## Step 2: Return to Working Branch (10 seconds)

```cmd
git checkout Obsidian
```

---

## Step 3: Copy New Files (Instructions Below)

You will receive a file called `crownwell-new-system.zip` from me.

**Windows instructions**:

1. Download `crownwell-new-system.zip` (I will provide download link)
2. Right-click the zip file → **Extract All**
3. Extract to a temporary location (e.g., `C:\temp\crownwell-new-system\`)
4. Open File Explorer to: `C:\temp\crownwell-new-system\`
5. Select ALL files and folders inside (Ctrl+A)
6. Copy (Ctrl+C)
7. Navigate to: `C:\crownwell-publishing\`
8. Paste (Ctrl+V)
9. When asked "Replace files?", click **Yes to All**

---

## Step 4: Add Cartwright DOCX (5 minutes)

**Important**: The new system needs the Cartwright DOCX file.

**If you still have it from the old system**:

1. Find the old location: `C:\crownwell-publishing\runs\2026-02-03_cartwright-autobiography\input\book.docx`
2. Copy it
3. Paste to NEW location: `C:\crownwell-publishing\books\cartwright-autobiography\input\original.docx`

**If you don't have it**:
- Tell me and I will help you retrieve it from GitHub or find another source

---

## Step 5: Commit New System (2 minutes)

In terminal at `C:\crownwell-publishing`:

```cmd
git add .
git commit -m "Migrate to EPUB-first publishing pipeline"
git push
```

---

## Step 6: Test GitHub Actions (5 minutes)

1. Go to: https://github.com/PeterCarterSr/crownwell-publishing/actions
2. Click: **Build EPUB** (in left sidebar)
3. Click: **Run workflow** (top right)
4. In "Book directory name" field, enter: `cartwright-autobiography`
5. Click: **Run workflow** (green button)

**Wait 3-5 minutes** for the workflow to complete.

---

## Step 7: Download Your First EPUB (2 minutes)

1. When workflow shows green checkmark, click on the run
2. Scroll to **Artifacts** section
3. Download: `epub-cartwright-autobiography.zip`
4. Extract the zip file
5. Open: `cartwright-autobiography.epub` in an EPUB reader

**Suggested EPUB readers**:
- **Windows**: Calibre (free, download from calibre-ebook.com)
- **Browser**: EPUBReader extension for Firefox/Chrome
- **Mobile**: Apple Books (iOS) or Google Play Books (Android)

---

## Step 8: Verify Quality (10 minutes)

Open the EPUB and check:

- [ ] Title page shows "Crownwell Press"
- [ ] Copyright page is correct
- [ ] Table of contents works (clickable links)
- [ ] Text is well-formatted
- [ ] Chapter headings are clear
- [ ] No "Delmarva Publications" text appears (NOTE: automated cleaning not yet implemented, you may still see old publisher - I will fix this next)

---

## Step 9: Report Back to Me

Tell me ONE of these:

**Success**: "EPUB looks good, ready to proceed with other books"

**Problems**: Describe what's wrong (e.g., "EPUB won't open", "Missing chapters", "Formatting broken")

**Need help**: "Stuck at Step X" (tell me which step)

---

## What Happens Next

After successful Cartwright build:

1. I will implement DOCX cleaning (remove old publisher automatically)
2. We will batch-process your other books
3. We will set up cover design pipeline
4. We will prepare KDP upload process

---

## Emergency Rollback (If Anything Goes Wrong)

If you need to go back to the old system:

```cmd
git checkout archive-old-system
git checkout -b Obsidian-rollback
git push -u origin Obsidian-rollback
```

Then contact me immediately.

---

## Questions?

Do NOT proceed if you are unsure about any step. Ask me first.

I am managing this project. You do not need to understand the technical details.
Just follow these instructions exactly as written.
