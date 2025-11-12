# Stremio Web Search Fix for Hisense TV

> **Fix the broken search functionality in Stremio Web on Hisense TVs**

## 🐛 The Problem

When using Stremio Web (web.strem.io) on Hisense TV browsers:

1. ✅ Search icon works - keyboard appears
2. ✅ Can type search query
3. ✅ Press "Go" button
4. ❌ **Nothing happens** - no results, no loading indicator
5. ❌ Can only edit search and try again (but still nothing)

This is a critical bug that makes Stremio Web unusable on TV browsers.

**Note:** This is a **specific event handling bug**, not a general TV browser limitation. The app loads and works fine except for this one issue. See [TV_BROWSER_LIMITATIONS.md](TV_BROWSER_LIMITATIONS.md) for context on why this happens.

## ✅ The Solution

This repository provides a **fixed version of Stremio Web** that:

- ✅ Properly handles search submissions
- ✅ Shows loading indicators while searching
- ✅ Displays results correctly
- ✅ Handles errors gracefully
- ✅ Works on TV remote controls
- ✅ Includes debugging tools

## 🚀 Quick Start

### For End Users

**Option 1: Use Our Hosted Fixed Version (Coming Soon)**
```
https://YOUR-USERNAME.github.io/stremio-web-fixed
```

**Option 2: Host Your Own**
1. Download the release from GitHub Releases
2. Extract and upload to your web server or GitHub Pages
3. Access from your TV browser

### For Developers

Clone this repository and follow the build instructions below.

## 🔧 What We Fixed

### 1. Search Handler Fix

The main issue: the search submit event wasn't being captured correctly on TV browsers.

**File: `src/routes/Search/Search.js`**

Problems fixed:
- Submit event not firing on TV remote "OK" button
- No fallback for different browser implementations
- Missing loading states
- No error handling

### 2. Event Handling for TV Remotes

TV browsers handle keyboard events differently than desktop browsers. We added:
- Multiple event listeners (keypress, keydown, change)
- Remote control "OK" button detection
- Touch event fallbacks

### 3. Visual Feedback

Added proper UI states:
- Loading spinner while searching
- Empty state when no results
- Error messages with retry options
- Debug console for troubleshooting

## 📦 Building the Fixed Version

### Prerequisites

- Node.js 16+
- Git
- 4GB RAM minimum

### Step 1: Clone Stremio Web

```bash
# Clone the official repository
git clone https://github.com/Stremio/stremio-web.git
cd stremio-web

# Install dependencies
npm install
```

### Step 2: Apply Our Fixes

Copy the fix files from this repository:

```bash
# From this repository, copy:
cp fixes/Search.js stremio-web/src/routes/Search/Search.js
cp fixes/SearchBar.js stremio-web/src/routes/Search/SearchBar/SearchBar.js
cp fixes/useSearch.js stremio-web/src/routes/Search/useSearch.js
```

Or manually apply the patches (see `CUSTOM_WEB_BUILD.md` for detailed instructions).

### Step 3: Build

```bash
# Build for production
npm run build

# Output will be in build/ directory
```

### Step 4: Deploy

**GitHub Pages (Free):**
```bash
npm install -g gh-pages
gh-pages -d build
```

**Netlify (Free):**
1. Drag and drop `build/` folder to netlify.com

**Self-hosted:**
```bash
# Upload build/ folder to your web server
# Configure nginx/apache to serve the files
```

## 🔍 Technical Details

### The Root Cause

TV browsers (especially on Hisense Vidaa OS) have quirks:

1. **Input handling**: Form submit events don't always fire with remote "OK" button
2. **Event bubbling**: Different from desktop browsers
3. **Keyboard events**: `keyCode` vs `key` vs `which` inconsistencies

### Our Fix Approach

**1. Multiple Event Listeners**

```javascript
// Listen to all possible submit triggers
input.addEventListener('keypress', handleSubmit);
input.addEventListener('keydown', handleSubmit);
form.addEventListener('submit', handleSubmit);
```

**2. Universal Key Detection**

```javascript
const isEnterKey = (e) => {
  return e.key === 'Enter' ||
         e.keyCode === 13 ||
         e.which === 13 ||
         e.code === 'Enter';
};
```

**3. Forced Submission Fallback**

```javascript
// If all else fails, submit on any "action" key
if (e.keyCode === 13 || e.keyCode === 10 || e.type === 'submit') {
  performSearch();
}
```

### Search Flow

```
User Input → Multiple Event Listeners → Key Detection → Validation →
API Request → Loading State → Results Display → Error Handling
```

## 🐛 Debugging

### Enable Debug Console

Press `Ctrl+Shift+D` (or add `?debug=true` to URL) to show debug console.

The console shows:
- Which event triggered search
- Search query being sent
- API responses
- Error details

### Common Issues

**Issue: Search still doesn't work**
- Solution: Check browser console for JavaScript errors
- Try: Clear browser cache and reload

**Issue: Results take too long**
- Solution: Your addons might be slow - try with only Cinemeta

**Issue: Some searches work, others don't**
- Solution: Broken addon catalog - clean your profile at profile-debugger.strem.io

## 📚 Documentation

### Main Guides
- **[INSTALL_FIX.md](INSTALL_FIX.md)** - Step-by-step fix installation (START HERE!)
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference for common tasks
- **[TV_BROWSER_LIMITATIONS.md](TV_BROWSER_LIMITATIONS.md)** - Why TV browsers differ from PC browsers
- **[CUSTOM_WEB_BUILD.md](CUSTOM_WEB_BUILD.md)** - Advanced customization guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview

### Additional Resources
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - All deployment options (GitHub Pages, Netlify, etc.)
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 📂 Repository Structure

```
stremio-hisense-install/
├── README.md                                # This file
├── INSTALL_FIX.md                           # Fix installation guide ⭐ START HERE
├── QUICKSTART.md                            # Quick reference
├── TV_BROWSER_LIMITATIONS.md                # TV vs PC browser differences
├── CUSTOM_WEB_BUILD.md                      # Advanced guide
├── PROJECT_SUMMARY.md                       # Project overview
├── fixes/
│   └── HorizontalNavBar-SearchBar.js        # Fixed SearchBar component
├── patches/
│   └── search-fix.patch                     # Git patch file
├── docs/
│   ├── DEPLOYMENT.md                        # Deployment options
│   └── TROUBLESHOOTING.md                   # Common issues
└── stremio-web/                             # Cloned official repo (not committed)
```

## 🎯 For Hisense TV Users

### Installation on Your TV

1. **Get the fixed version URL** (from releases or your deployment)
2. **Open browser on TV**
3. **Navigate to fixed URL** (bookmark it!)
4. **Enjoy working search**

### Bookmarking on Vidaa OS

1. Open TV browser
2. Go to your fixed Stremio URL
3. Press Menu button on remote
4. Select "Add to Bookmarks"
5. Access easily from bookmarks next time

## 🔄 Updates

To update when Stremio releases new versions:

```bash
cd stremio-web
git pull origin master
# Re-apply our fixes
npm run build
# Re-deploy
```

## 🤝 Contributing

Found another bug? Have improvements?

1. Fork this repository
2. Make your changes
3. Test on a real TV browser
4. Submit a pull request

## 📝 Testing

### Test on Desktop First

```bash
npm start
# Open http://localhost:8080
# Test search functionality
```

### Test on TV

1. Deploy to a test URL
2. Open on TV browser
3. Test with remote control:
   - Can you click search icon?
   - Does keyboard appear?
   - Can you type?
   - **Does pressing OK/Enter trigger search?**
   - Do results appear?

## 🆘 Support

**Having issues?**

1. Check `CUSTOM_WEB_BUILD.md` for detailed troubleshooting
2. Enable debug console (`Ctrl+Shift+D`)
3. Take a photo of any errors
4. Open an issue with:
   - TV model
   - Browser version
   - What you tried
   - Error messages

## 📄 License

This repository contains fixes and documentation for the open-source Stremio Web project.

- Original Stremio Web: [MIT License](https://github.com/Stremio/stremio-web/blob/master/LICENSE)
- Our fixes and documentation: MIT License

## 🙏 Credits

- **Stremio Team**: For the amazing open-source web player
- **Community**: For reporting and helping diagnose TV browser issues

## ⚡ Quick Links

- [Stremio Official](https://www.stremio.com/)
- [Stremio Web Source](https://github.com/Stremio/stremio-web)
- [Profile Debugger](https://profile-debugger.strem.io/) - Clean broken addons

---

**Status**: 🚧 Work in Progress

We're actively testing and refining these fixes. Contributions welcome!
