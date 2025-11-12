# Quick Start Guide

## For End Users (Just want to use fixed Stremio Web)

### Option 1: Use hosted version (when available)
```
https://YOUR-GITHUB-USERNAME.github.io/stremio-web
```

### Option 2: Deploy your own in 5 minutes

**Step 1:** Download this release
**Step 2:** Extract the files
**Step 3:** Run these commands:

```bash
# Clone Stremio Web
git clone https://github.com/Stremio/stremio-web.git
cd stremio-web

# Install dependencies
npm install

# Copy our fixes
cp ../fixes/SearchBar.js src/routes/Search/SearchBar/SearchBar.js
cp ../fixes/useSearch.js src/routes/Search/useSearch.js

# Build
npm run build

# Deploy to GitHub Pages
npm install -g gh-pages
gh-pages -d build
```

**Step 4:** Access at `https://YOUR-USERNAME.github.io/stremio-web`

---

## For Developers (Want to modify/improve)

### Setup

```bash
# Clone this repository
git clone https://github.com/YOUR-USERNAME/stremio-hisense-install.git
cd stremio-hisense-install

# Clone Stremio Web
git clone https://github.com/Stremio/stremio-web.git
cd stremio-web

# Install
npm install
```

### Apply fixes

```bash
# From stremio-web directory
cp ../fixes/SearchBar.js src/routes/Search/SearchBar/SearchBar.js
cp ../fixes/useSearch.js src/routes/Search/useSearch.js
```

### Test locally

```bash
npm start
# Open http://localhost:8080
# Test search functionality
```

### Build for production

```bash
npm run build
# Output in build/ directory
```

### Deploy

**GitHub Pages:**
```bash
gh-pages -d build
```

**Netlify:**
- Drag `build/` folder to netlify.com

**Self-hosted:**
```bash
scp -r build/* user@server:/var/www/stremio-web/
```

---

## What Gets Fixed

✅ **Search button actually works** on TV remotes
✅ **Multiple event listeners** for compatibility
✅ **Loading indicators** show while searching
✅ **Error handling** prevents crashes
✅ **Debug console** for troubleshooting (Ctrl+Shift+D)

---

## Testing on TV

1. Deploy to HTTPS URL (required)
2. Open TV browser
3. Navigate to your URL
4. Click search icon
5. Type something
6. Press remote "OK" button or Enter
7. **Should show loading → results**

If step 7 fails, enable debug console (Ctrl+Shift+D) and check for errors.

---

## Common Issues

**Search still doesn't work:**
- Check you're using HTTPS (WebAssembly requires it)
- Clear TV browser cache
- Enable debug console to see errors

**No results found:**
- Install Cinemeta addon
- Remove broken addons at profile-debugger.strem.io

**Build fails:**
```bash
rm -rf node_modules
npm install
npm run build
```

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more.

---

## File Structure

```
stremio-hisense-install/
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
├── CUSTOM_WEB_BUILD.md    # Detailed build guide
├── fixes/
│   ├── SearchBar.js       # Fixed search input component
│   └── useSearch.js       # Fixed search logic
├── docs/
│   ├── DEPLOYMENT.md      # All deployment options
│   └── TROUBLESHOOTING.md # Common issues
└── stremio-web/           # Clone from GitHub (not in repo)
```

---

## Quick Commands Reference

```bash
# Clone Stremio Web
git clone https://github.com/Stremio/stremio-web.git

# Install dependencies
cd stremio-web && npm install

# Apply our fixes
cp ../fixes/*.js src/routes/Search/

# Test locally
npm start

# Build
npm run build

# Deploy to GitHub Pages
gh-pages -d build

# Deploy to Netlify
# Drag build/ folder to netlify.com

# Check for errors in browser
# Press F12 → Console tab
```

---

## Need Help?

1. **Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Most common issues
2. **Enable debug console** (Ctrl+Shift+D) - See what's happening
3. **Test on desktop first** - Easier to debug
4. **Open GitHub issue** - Include debug console output

---

## Next Steps

1. ✅ Deploy fixed version
2. ✅ Test on TV browser
3. ✅ Bookmark for easy access
4. ✅ Share with other Hisense users!

---

**Most important:** Use HTTPS! WebAssembly won't work over HTTP.

GitHub Pages and Netlify provide free HTTPS automatically. ✨
