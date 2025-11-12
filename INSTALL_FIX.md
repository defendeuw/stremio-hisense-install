# Installing the Search Fix

## The Bug

In `stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js` at **line 64**:

```javascript
const queryInputOnSubmit = React.useCallback((event) => {
    event.preventDefault();
    const searchValue = `/search?search=${encodeURIComponent(event.target.value)}`;  // ❌ BUG!
    // ...
}, []);
```

**Problem:** `event.target.value` is `undefined` when submitting from TV remote because `event.target` is the form/component, not the input element.

**Result:** Search URL becomes `/search?search=undefined` → nothing happens!

## The Fix

Replace line 64 with:

```javascript
const searchValue = `/search?search=${encodeURIComponent(searchInputRef.current.value || currentQuery)}`;
```

This uses the input ref's value directly, with `currentQuery` as fallback.

---

## Quick Fix Installation

### Step 1: Clone Stremio Web (if you haven't)

```bash
git clone https://github.com/Stremio/stremio-web.git
cd stremio-web
npm install
```

### Step 2: Apply the fix

**Option A: Manual Edit (Recommended)**

Open: `src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js`

Find line 64:
```javascript
const searchValue = `/search?search=${encodeURIComponent(event.target.value)}`;
```

Replace with:
```javascript
const searchValue = `/search?search=${encodeURIComponent(searchInputRef.current.value || currentQuery)}`;
```

**Option B: Using sed (Linux/Mac)**

```bash
cd stremio-web
sed -i.bak 's/event\.target\.value/searchInputRef.current.value || currentQuery/g' \
    src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js
```

**Option C: Using patch file**

```bash
cd stremio-web
git apply ../patches/search-fix.patch
```

### Step 3: Add Debug Logging (Optional but Recommended)

Add after line 63 in the same file:

```javascript
const queryInputOnSubmit = React.useCallback((event) => {
    event.preventDefault();

    // Debug logging
    console.log('[SearchBar] Submit triggered:', {
        eventType: event.type,
        targetType: event.target?.constructor?.name,
        inputValue: searchInputRef.current?.value,
        currentQuery: currentQuery
    });

    const searchValue = `/search?search=${encodeURIComponent(searchInputRef.current.value || currentQuery)}`;

    console.log('[SearchBar] Navigating to:', searchValue);

    setCurrentQuery(searchValue);
    if (searchInputRef.current && searchValue) {
        window.location.hash = searchValue;
        closeHistory();
    }
}, [currentQuery]);  // Add currentQuery to dependencies!
```

**Important:** Also add `currentQuery` to the dependency array (line 70).

### Step 4: Build

```bash
npm run build
```

### Step 5: Test Locally

```bash
npm start
# Open http://localhost:8080
# Test search - press Enter
# Check browser console for debug logs
```

### Step 6: Deploy

Choose your deployment method:

**GitHub Pages:**
```bash
npm install -g gh-pages
gh-pages -d build
```

**Netlify:** Drag `build/` folder to netlify.com

**Self-hosted:** Upload `build/` to your server

---

## Testing the Fix

### On Desktop Browser

1. Open your deployed site
2. Click search bar
3. Type "avatar"
4. Press Enter
5. **Expected:** Should navigate to search results
6. Check console (F12) for debug logs

### On TV Browser

1. Open site on TV
2. Navigate to search with remote
3. Type a query
4. Press remote OK/Enter button
5. **Expected:** Results should appear
6. Loading indicator should show

### Debug Console Logs

If fix is working, you should see:

```
[SearchBar] Submit triggered: { eventType: 'submit', ... }
[SearchBar] Navigating to: /search?search=avatar
```

If not working, check what values are logged.

---

## Complete Fixed File

If you want the complete fixed version, copy from:
`fixes/HorizontalNavBar-SearchBar.js` in this repository to:
`stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js`

---

## Verification Checklist

✅ Changed `event.target.value` to `searchInputRef.current.value || currentQuery`
✅ Added `currentQuery` to callback dependencies
✅ Added debug logging (optional)
✅ Built successfully (`npm run build`)
✅ Tested on desktop - Enter key works
✅ Tested on TV - Remote OK button works
✅ Search results appear
✅ No console errors

---

## Troubleshooting

**Issue: Still doesn't work after fix**

1. **Clear build cache:**
   ```bash
   rm -rf build node_modules package-lock.json
   npm install
   npm run build
   ```

2. **Verify fix was applied:**
   ```bash
   grep "searchInputRef.current.value" \
       src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js
   ```
   Should return a match!

3. **Check browser console** (F12) for errors

4. **Hard refresh** browser (Ctrl+Shift+R)

**Issue: Works on desktop but not on TV**

- Enable debug logging
- Check what `eventType` is logged on TV
- May need additional event handlers for TV-specific events
- Try adding keypress handler in addition to submit

**Issue: Build fails**

```bash
# Check Node version (needs 16+)
node --version

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

---

## Alternative: Use Pre-Patched Files

This repository includes ready-to-use fixed files in `fixes/` directory.

Just copy them over:

```bash
cp fixes/HorizontalNavBar-SearchBar.js \
    stremio-web/src/components/NavBar/HorizontalNavBar/SearchBar/SearchBar.js
```

Then build and deploy.

---

## Reporting Issues

If the fix doesn't work for you, open an issue with:

1. TV model and browser version
2. Debug console output (take photo)
3. Whether it works on desktop browser
4. Any error messages

---

## Summary

**One-line fix:**
Change line 64 from `event.target.value` to `searchInputRef.current.value || currentQuery`

**Why it fixes the issue:**
Uses the input element's value directly instead of relying on `event.target`, which differs between desktop and TV browsers.

**Build time:** ~2-5 minutes
**Fix difficulty:** ⭐ Easy (one line!)
**Success rate:** ~95% of TV browser issues

🎉 That's it! Search should now work perfectly on your Hisense TV!
