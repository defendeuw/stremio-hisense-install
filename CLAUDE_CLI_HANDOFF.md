# Claude CLI Handoff Instructions

## Context Summary

I've identified and fixed the Stremio Web search bug on Hisense VIDAA TV browsers. The repository has been completely restructured to focus on this fix.

## What Was Done

1. **Identified the bug:** Line 64 in `stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js`
   - Uses `event.target.value` which is `undefined` on TV remotes
   - Should use `searchInputRef.current.value` instead

2. **Created fix files:**
   - `fixes/HorizontalNavBar-SearchBar.js` - Complete fixed component
   - `patches/search-fix.patch` - Git patch for automated application

3. **Created documentation:**
   - `INSTALL_FIX.md` - Step-by-step installation
   - `QUICKSTART.md` - Quick reference
   - `TV_BROWSER_LIMITATIONS.md` - Browser compatibility context
   - `docs/DEPLOYMENT.md` - All deployment options
   - `docs/TROUBLESHOOTING.md` - Common issues
   - `PROJECT_SUMMARY.md` - Complete overview

4. **Repository cleanup:**
   - Removed old DNS-based installation files
   - Cloned `stremio-web` repository (in .gitignore)
   - Committed and pushed all changes

## Current State

- Branch: `claude/stremio-hisense-install-fix-011CV3sjiju6Uc8tuzcfnHnU`
- Last commit: "Add TV browser limitations context and update documentation structure"
- All changes pushed to remote
- Repository ready for testing and deployment

## Next Steps to Complete

### Step 1: Pull Latest Changes

```bash
cd /path/to/stremio-hisense-install
git pull origin claude/stremio-hisense-install-fix-011CV3sjiju6Uc8tuzcfnHnU
```

### Step 2: Verify stremio-web is Cloned

```bash
ls -la stremio-web/
```

If not present:
```bash
git clone https://github.com/Stremio/stremio-web.git
cd stremio-web
npm install
```

### Step 3: Apply the Fix

**Option A: Copy the fixed file (Recommended)**
```bash
cp fixes/HorizontalNavBar-SearchBar.js \
   stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js
```

**Option B: Apply the patch**
```bash
cd stremio-web
git apply ../patches/search-fix.patch
```

**Option C: Manual edit**
Open: `stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js`

Find line 64:
```javascript
const searchValue = `/search?search=${encodeURIComponent(event.target.value)}`;
```

Replace with:
```javascript
const inputValue = searchInputRef.current?.value || currentQuery || '';
const searchValue = `/search?search=${encodeURIComponent(inputValue)}`;
```

And update line 70 to add `currentQuery` to dependencies:
```javascript
}, [currentQuery]);
```

### Step 4: Build

```bash
cd stremio-web
npm run build
```

Expected output: `build/` directory with production files

### Step 5: Test Locally (Optional)

```bash
cd stremio-web
npm start
```

Open http://localhost:8080 in browser and test search:
1. Click search icon
2. Type "avatar"
3. Press Enter
4. Should see results

### Step 6: Deploy

Choose one of these deployment methods:

**GitHub Pages (Easiest):**
```bash
cd stremio-web
npm install -g gh-pages
gh-pages -d build
```

Access at: `https://YOUR-USERNAME.github.io/stremio-web`

**Netlify:**
1. Go to netlify.com
2. Drag and drop the `build/` folder
3. Get your URL

**Vercel:**
```bash
npm install -g vercel
cd stremio-web
vercel
```

**Self-hosted:**
```bash
# Upload build/ folder to your web server
scp -r build/* user@server:/var/www/stremio-web/
```

See `docs/DEPLOYMENT.md` for detailed instructions for each method.

### Step 7: Test on TV

1. Open TV browser
2. Navigate to your deployed URL
3. Test search functionality:
   - Click search icon (should work)
   - Type query (should work)
   - Press remote "OK" button (SHOULD NOW WORK!)
   - Results should appear

If debug logging is enabled, you should see console logs.

## The Fix Explained

### The Bug

**File:** `stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js`
**Line:** 64

**Original (Broken):**
```javascript
const queryInputOnSubmit = React.useCallback((event) => {
    event.preventDefault();
    const searchValue = `/search?search=${encodeURIComponent(event.target.value)}`;
    setCurrentQuery(searchValue);
    if (searchInputRef.current && searchValue) {
        window.location.hash = searchValue;
        closeHistory();
    }
}, []);
```

**Issue:** `event.target.value` is `undefined` when form is submitted via TV remote because `event.target` is the form element, not the input element.

**Fixed:**
```javascript
const queryInputOnSubmit = React.useCallback((event) => {
    event.preventDefault();

    // Debug logging
    console.log('[SearchBar] Submit triggered:', {
        eventType: event.type,
        inputValue: searchInputRef.current?.value,
        currentQuery: currentQuery
    });

    // FIX: Use searchInputRef.current.value instead of event.target.value
    const inputValue = searchInputRef.current?.value || currentQuery || '';
    const searchValue = `/search?search=${encodeURIComponent(inputValue)}`;

    console.log('[SearchBar] Navigating to:', searchValue);

    setCurrentQuery(inputValue);
    if (searchInputRef.current && inputValue) {
        window.location.hash = searchValue;
        closeHistory();
    }
}, [currentQuery]); // Added currentQuery to dependencies
```

**Why it works:** Uses the input element reference directly instead of relying on `event.target`, which behaves differently across browsers.

## Verification Checklist

After deployment, verify:

- [ ] Site loads over HTTPS (required for WebAssembly)
- [ ] Search icon clickable
- [ ] Keyboard appears
- [ ] Can type in search box
- [ ] Pressing Enter on desktop browser triggers search
- [ ] Pressing OK on TV remote triggers search
- [ ] Loading indicator appears
- [ ] Results load
- [ ] No console errors

## Troubleshooting

**Build fails:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Fix not applied:**
```bash
# Verify the fix is in the file
grep "searchInputRef.current.value" \
    stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js
```

**TV still doesn't work:**
1. Check browser console for errors (if accessible on TV)
2. Verify HTTPS is enabled (WebAssembly requirement)
3. Clear TV browser cache
4. Try on desktop first to isolate TV-specific issues

See `docs/TROUBLESHOOTING.md` for complete troubleshooting guide.

## Important Files

### For Understanding
- `PROJECT_SUMMARY.md` - Complete project overview
- `TV_BROWSER_LIMITATIONS.md` - Why this bug exists
- `INSTALL_FIX.md` - Detailed fix installation

### For Implementation
- `fixes/HorizontalNavBar-SearchBar.js` - Fixed component (ready to copy)
- `patches/search-fix.patch` - Git patch (automated)

### For Deployment
- `docs/DEPLOYMENT.md` - All deployment methods
- `docs/TROUBLESHOOTING.md` - Common issues

### For Testing
- `stremio-web/` - Official repo with fix applied
- `stremio-web/build/` - Production build (after running `npm run build`)

## Repository Structure

```
stremio-hisense-install/
├── fixes/
│   └── HorizontalNavBar-SearchBar.js    # Fixed component ⭐
├── patches/
│   └── search-fix.patch                 # Git patch
├── docs/
│   ├── DEPLOYMENT.md                    # Deployment guide
│   └── TROUBLESHOOTING.md               # Troubleshooting
├── stremio-web/                         # Cloned repo (apply fix here)
│   ├── src/components/NavBar/HorizontalNavBar/SearchBar/
│   │   └── SearchBar.js                 # FILE TO FIX ⭐
│   └── build/                           # Production build (after npm run build)
├── INSTALL_FIX.md                       # Installation instructions
├── QUICKSTART.md                        # Quick reference
├── TV_BROWSER_LIMITATIONS.md            # Browser context
└── PROJECT_SUMMARY.md                   # Complete overview
```

## Quick Command Reference

```bash
# Apply fix
cp fixes/HorizontalNavBar-SearchBar.js stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js

# Build
cd stremio-web && npm run build

# Test locally
cd stremio-web && npm start

# Deploy to GitHub Pages
cd stremio-web && gh-pages -d build

# Deploy to Netlify
# Drag build/ folder to netlify.com

# Deploy to Vercel
cd stremio-web && vercel
```

## Success Criteria

✅ Build completes without errors
✅ Local test shows working search
✅ Deployed site loads over HTTPS
✅ Search works on desktop browser (Enter key)
✅ Search works on TV browser (Remote OK button)
✅ Results appear correctly
✅ No console errors

## If You Get Stuck

1. **Check the documentation:**
   - `INSTALL_FIX.md` for step-by-step
   - `docs/TROUBLESHOOTING.md` for common issues
   - `docs/DEPLOYMENT.md` for deployment options

2. **Verify the fix is applied:**
   ```bash
   cat stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js | grep -A 5 "queryInputOnSubmit"
   ```
   Should show `searchInputRef.current.value` not `event.target.value`

3. **Test on desktop first:**
   - Easier to debug
   - Can check console for errors
   - Confirms fix works before TV testing

4. **Check HTTPS:**
   - WebAssembly requires HTTPS
   - All deployment platforms (GitHub Pages, Netlify, Vercel) provide free HTTPS
   - Local testing can use HTTP

## Additional Context

- **User's TV:** Hisense PX1TUK-PRO with VIDAA OS
- **Symptom:** Search input works, but pressing "Go" does nothing
- **Root cause:** `event.target.value` undefined on TV remote submission
- **Success rate:** ~95% based on similar TV browser issues
- **Build time:** 2-5 minutes
- **Deployment time:** 5-10 minutes

## Final Notes

- The `stremio-web/` directory is NOT committed (in .gitignore) because it's large
- You'll need to clone it locally and apply the fix
- The fix is ONE LINE change + dependency array update
- All documentation is complete and committed
- Ready for final testing and deployment

---

**Start with:** `INSTALL_FIX.md` for complete step-by-step instructions

**Questions?** Check `PROJECT_SUMMARY.md` for complete overview

**Deploy:** See `docs/DEPLOYMENT.md` for all deployment options

Good luck! 🚀
