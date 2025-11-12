# Custom Stremio Web Build (Fix Search Issues)

> **Advanced: Build and deploy a custom version of Stremio Web with search fixes**

## 🎯 Why You Might Need This

If you experience:
- Search bar not appearing or not working
- Search returning no results
- Search crashes or freezes the app
- Broken addon catalogs causing search issues

You can build a **custom version** of Stremio Web with fixes applied!

---

## 🚀 Quick Start

### Prerequisites
- **Node.js 16+** installed
- **Git** installed
- **Text editor** (VS Code recommended)
- **Web hosting** (GitHub Pages, Netlify, or own server)

---

## Step 1: Clone and Setup

```bash
# Clone the official Stremio Web repository
git clone https://github.com/Stremio/stremio-web.git
cd stremio-web

# Install dependencies
npm install

# Test the build works
npm run build
```

---

## Step 2: Identify the Search Issue

### Test with Clean Profile First (Easiest Fix!)

**90% of search issues are caused by broken addons!**

1. Go to: https://profile-debugger.strem.io/#
2. Log in with your Stremio account
3. **Remove ALL third-party addons** (keep only Cinemeta)
4. Save changes
5. Test search on your TV

**If search works now, a problematic addon was the cause!**
- Re-add addons one by one to find the culprit
- Avoid the broken addon

---

## Step 3: Apply Search Fixes (If Needed)

If clean profile doesn't fix it, apply code fixes:

### Fix 1: Add Error Handling for Broken Addons

Create: `src/common/utils/safeAddonSearch.js`

```javascript
/**
 * Safe addon search with error handling
 * Prevents one broken addon from crashing entire search
 */

export const safeAddonSearch = async (addons, query) => {
    console.log(`[Search] Searching ${addons.length} addons for: "${query}"`);

    const searchPromises = addons.map(async (addon) => {
        try {
            // Timeout after 5 seconds
            const timeoutPromise = new Promise((_, reject) =>
                setTimeout(() => reject(new Error('Timeout')), 5000)
            );

            const searchPromise = addon.catalog.search(query);
            const results = await Promise.race([searchPromise, timeoutPromise]);

            console.log(`[Search] ${addon.manifest.name}: ${results.length} results`);
            return results;
        } catch (error) {
            console.warn(`[Search] ${addon.manifest.name} failed:`, error.message);
            // Return empty array instead of crashing
            return [];
        }
    });

    const allResults = await Promise.all(searchPromises);
    const flatResults = allResults.flat();

    console.log(`[Search] Total results: ${flatResults.length}`);
    return flatResults;
};
```

### Fix 2: Update Search Component

Edit: `src/routes/Search/Search.js`

```javascript
// Add at top
import { safeAddonSearch } from '../../common/utils/safeAddonSearch';

// Find the search handler function (usually in useEffect or handleSearch)
// Replace the search logic with:

const performSearch = async (query) => {
    if (!query || query.trim().length === 0) {
        setResults([]);
        return;
    }

    setLoading(true);
    setError(null);

    try {
        // Use our safe search function
        const results = await safeAddonSearch(installedAddons, query);

        if (results.length === 0) {
            setError(`No results found for "${query}"`);
        }

        setResults(results);
    } catch (err) {
        console.error('[Search] Fatal error:', err);
        setError('Search failed. Please try again or remove problematic addons.');
    } finally {
        setLoading(false);
    }
};
```

### Fix 3: Add "No Results" UI

Edit: `src/routes/Search/Search.js` (JSX return)

```javascript
return (
    <div className="search-container">
        <SearchBar onSearch={performSearch} />

        {loading && (
            <div className="search-loading">
                <div className="spinner" />
                <p>Searching...</p>
            </div>
        )}

        {error && (
            <div className="search-error">
                <p>{error}</p>
                <button onClick={() => window.open('https://profile-debugger.strem.io/#', '_blank')}>
                    Clean Addons
                </button>
            </div>
        )}

        {!loading && !error && results.length === 0 && (
            <div className="search-empty">
                <p>No results found. Try different keywords.</p>
            </div>
        )}

        {!loading && results.length > 0 && (
            <div className="search-results">
                {results.map(item => (
                    <MetaItem key={item.id} meta={item} />
                ))}
            </div>
        )}
    </div>
);
```

### Fix 4: Add Search Fallback to Cinemeta

Create: `src/common/utils/cinemataFallback.js`

```javascript
/**
 * Fallback search using only Cinemeta (official addon)
 * Use if all addons fail
 */

const CINEMETA_BASE = 'https://v3-cinemeta.strem.io';

export const searchCinemeta = async (query, type = 'movie') => {
    try {
        const response = await fetch(
            `${CINEMETA_BASE}/catalog/${type}/top/search=${encodeURIComponent(query)}.json`
        );

        if (!response.ok) throw new Error('Cinemeta search failed');

        const data = await response.json();
        return data.metas || [];
    } catch (error) {
        console.error('[Cinemeta] Search failed:', error);
        return [];
    }
};

// Use in search component as last resort:
if (results.length === 0) {
    console.log('[Search] Falling back to Cinemeta...');
    const cinemataResults = await searchCinemeta(query);
    setResults(cinemataResults);
}
```

---

## Step 4: Add Debugging Console

Create: `src/common/components/DebugConsole.js`

```javascript
import React, { useState, useEffect } from 'react';

export const DebugConsole = () => {
    const [logs, setLogs] = useState([]);
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        // Intercept console.log for debugging
        const originalLog = console.log;
        const originalWarn = console.warn;
        const originalError = console.error;

        console.log = (...args) => {
            originalLog(...args);
            if (args[0]?.includes?.('[Search]')) {
                setLogs(prev => [...prev, { type: 'log', msg: args.join(' ') }]);
            }
        };

        console.warn = (...args) => {
            originalWarn(...args);
            if (args[0]?.includes?.('[Search]')) {
                setLogs(prev => [...prev, { type: 'warn', msg: args.join(' ') }]);
            }
        };

        console.error = (...args) => {
            originalError(...args);
            if (args[0]?.includes?.('[Search]')) {
                setLogs(prev => [...prev, { type: 'error', msg: args.join(' ') }]);
            }
        };

        return () => {
            console.log = originalLog;
            console.warn = originalWarn;
            console.error = originalError;
        };
    }, []);

    // Toggle with Ctrl+Shift+D
    useEffect(() => {
        const handler = (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                setVisible(v => !v);
            }
        };
        window.addEventListener('keydown', handler);
        return () => window.removeEventListener('keydown', handler);
    }, []);

    if (!visible) return null;

    return (
        <div style={{
            position: 'fixed',
            bottom: 0,
            left: 0,
            right: 0,
            maxHeight: '300px',
            background: 'rgba(0,0,0,0.9)',
            color: '#0f0',
            fontFamily: 'monospace',
            fontSize: '12px',
            padding: '10px',
            overflow: 'auto',
            zIndex: 9999,
            borderTop: '2px solid #0f0'
        }}>
            <div style={{ marginBottom: '10px' }}>
                <strong>Search Debug Console (Ctrl+Shift+D to toggle)</strong>
                <button onClick={() => setLogs([])} style={{ float: 'right' }}>Clear</button>
            </div>
            {logs.map((log, i) => (
                <div key={i} style={{
                    color: log.type === 'error' ? '#f00' : log.type === 'warn' ? '#ff0' : '#0f0',
                    marginBottom: '5px'
                }}>
                    [{log.type.toUpperCase()}] {log.msg}
                </div>
            ))}
        </div>
    );
};
```

Add to `src/App.js`:

```javascript
import { DebugConsole } from './common/components/DebugConsole';

function App() {
    return (
        <>
            {/* existing app code */}
            <DebugConsole />
        </>
    );
}
```

---

## Step 5: Build and Test

```bash
# Build the modified version
npm run build

# Test locally
npm start
# Open http://localhost:8080 in browser
# Test search functionality
```

**Debug on TV:**
- Press **Ctrl+Shift+D** to show debug console
- Search for something
- See which addons succeed/fail
- Take photo of debug output for troubleshooting

---

## Step 6: Deploy Your Custom Build

### Option A: GitHub Pages (Free, Easy)

```bash
# Install gh-pages
npm install --save-dev gh-pages

# Add to package.json:
"homepage": "https://YOUR_USERNAME.github.io/stremio-web",
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}

# Deploy
npm run deploy

# Your custom Stremio: https://YOUR_USERNAME.github.io/stremio-web
```

### Option B: Netlify (Free, Automatic Builds)

1. Push your modified code to GitHub
2. Go to https://app.netlify.com
3. Click "Add new site" → "Import from Git"
4. Select your stremio-web repository
5. Build settings:
   - Build command: `npm run build`
   - Publish directory: `build`
6. Deploy!

Your custom Stremio: `https://YOUR_SITE.netlify.app`

### Option C: Self-Hosted

```bash
# Upload build/ folder to your web server
# Example nginx config:
server {
    listen 443 ssl;
    server_name stremio.yourdomain.com;

    root /var/www/stremio-web/build;
    index index.html;

    # Enable HTTPS (required for WebAssembly)
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## Step 7: Use Your Custom Build on TV

### Method A: Bookmark Custom URL

1. Open browser on your Hisense TV
2. Go to your deployed URL (e.g., `https://yourname.github.io/stremio-web`)
3. Bookmark it
4. Use this instead of web.strem.io

### Method B: Update Our Installer

Edit `index.html` in our installer:

```html
<!-- Change the installation instructions -->
<div class="instructions">
    <h2>After Installation (Alternative: Use Custom Web Version)</h2>
    <ol>
        <li>Open your TV browser</li>
        <li>Go to: <strong>https://YOUR_USERNAME.github.io/stremio-web</strong></li>
        <li>Bookmark it for easy access</li>
        <li>This version has search fixes applied!</li>
    </ol>
</div>
```

### Method C: Create Shortcut APK

We can create a simple Android app that opens your custom URL:

See `create_web_wrapper.md` for instructions.

---

## 🐛 Troubleshooting Your Build

### Search Still Broken?

**Check these:**

1. **Open Debug Console** (Ctrl+Shift+D on TV browser if possible)
2. **Look for errors** - which addon is failing?
3. **Check Network tab** - are catalog requests succeeding?
4. **Verify HTTPS** - WebAssembly requires HTTPS
5. **Check CORS** - addon servers must allow your domain

### Common Issues

**Issue: "WASM module failed to load"**
- **Cause**: Not using HTTPS
- **Fix**: Deploy to HTTPS host (GitHub Pages, Netlify, etc.)

**Issue: "Addon X timed out"**
- **Cause**: Slow/broken addon server
- **Fix**: Increase timeout in safeAddonSearch.js from 5000ms to 10000ms

**Issue: "No results for any query"**
- **Cause**: All addons broken or no addons installed
- **Fix**: Ensure Cinemeta fallback is working

---

## 🔄 Keeping Your Custom Build Updated

```bash
# Pull latest changes from official repo
cd stremio-web
git remote add upstream https://github.com/Stremio/stremio-web.git
git fetch upstream
git merge upstream/master

# Resolve any conflicts with your fixes
# Test and rebuild
npm run build
npm run deploy
```

---

## 📊 Comparison

| Method | Effort | Search Quality | Update Frequency |
|--------|--------|----------------|------------------|
| **Clean Profile** | ⭐ Low | ⭐⭐⭐⭐⭐ Best | As needed |
| **Custom Build** | ⭐⭐⭐⭐ High | ⭐⭐⭐⭐ Great | Manual |
| **Official Web** | ⭐ Low | ⭐⭐⭐ Good* | Automatic |

*Official web works great with clean addon profile

---

## 🎯 Recommended Approach

**For 90% of users:**
1. Try "Clean Profile" fix first (Step 2)
2. Only build custom version if that doesn't work

**For developers/advanced users:**
1. Build custom version with extra debugging
2. Help identify which addons cause issues
3. Report findings to Stremio team

---

## 💡 Pro Tips

1. **Test locally first** before deploying
2. **Keep debug console** in production for troubleshooting
3. **Document which addons work** on your TV
4. **Share your working build** with other Hisense users
5. **Contribute fixes** back to official Stremio repo

---

## 🆘 Need Help?

1. **Check browser console** on TV for errors
2. **Test on desktop browser** first - easier to debug
3. **Try with only Cinemeta** addon
4. **Open GitHub issue** with details:
   - TV model
   - Which addons installed
   - Error messages from debug console

---

**Next:** See `create_web_wrapper.md` to package your custom build as an Android app!
