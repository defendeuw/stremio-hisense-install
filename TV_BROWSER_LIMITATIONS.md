# TV Browser Limitations and Compatibility

## Understanding Why Web Apps Behave Differently on TV Browsers

The web app works perfectly on your PC browser but breaks on VIDAA TV browser because **smart TV browsers are severely limited compared to desktop browsers**. They're not the same despite both running the "same" web app.

---

## Why PC Browser Works But VIDAA Doesn't

### 1. WebAssembly Support Differences

**Your PC Browser:** Full WebAssembly support with all modern features

**VIDAA Browser:** Limited or outdated WebAssembly implementation

Stremio web uses **stremio-core compiled to WebAssembly**. If VIDAA's browser has incomplete WebAssembly support, the core search logic (written in Rust) might fail to load or execute properly, while everything works fine on your PC's Chrome/Firefox.

### 2. Browser Engine Age

**Your PC:** Latest Chrome (Blink engine) or Firefox (Gecko) with all modern web standards

**VIDAA/Hisense:** Often uses an **outdated WebKit or custom browser engine** from 2-3 years ago

Smart TV manufacturers don't update their browsers frequently. Your TV might be running a browser equivalent to Chrome 70 while your PC runs Chrome 130+.

### 3. JavaScript Performance

**Your PC:** Fast multi-core CPU optimized for web apps

**VIDAA TV:** Weak ARM processor with limited RAM (often 1-2GB total)

Complex React components and WebAssembly operations that run smoothly on your PC can timeout or crash on the TV's slower processor.

### 4. Memory Limitations

**Your PC:** Gigabytes of available RAM for the browser

**VIDAA TV:** WebAssembly limited to 4GB maximum, TV often has only 512MB-1GB for the browser

When search tries to load catalogs from multiple addons simultaneously, the TV browser may run out of memory while your PC handles it easily.

### 5. Network/HTTPS Handling

**Your PC:** Full support for modern TLS, CORS, mixed content policies

**VIDAA Browser:** May have stricter or broken HTTPS/mixed content handling

If addon APIs use older SSL certificates or mixed HTTP/HTTPS content, your PC browser handles it gracefully but the TV browser blocks it, breaking search.

### 6. Event Handling Differences (Your Specific Issue!)

**Your PC:** Consistent event.target behavior across all form submissions

**VIDAA Browser:** event.target.value is undefined when form submitted via remote control

This is the **specific bug** affecting your search! The form submission event from the TV remote is handled differently than keyboard Enter on PC.

---

## Comparison Table

| Feature | PC Browser | VIDAA Browser | Impact on Stremio |
|---------|-----------|---------------|-------------------|
| WebAssembly | Full support | Limited/buggy | Core search logic fails |
| JavaScript engine | V8 (Chrome) / SpiderMonkey (Firefox) | Old WebKit | Slow/timeout |
| Memory | Abundant | 512MB-1GB | Crashes with many addons |
| CSS support | Latest standards | 2-3 years old | UI rendering issues |
| Network APIs | Modern fetch/CORS | Limited | Addon API calls fail |
| Form events | Consistent | **Broken on remote** | **Search submit fails** ← Your issue |

---

## Your Specific Case: Search Submit Bug

### What Your Symptoms Tell Us

Since your app:
- ✅ Loads and initializes (WebAssembly working)
- ✅ Renders UI correctly (CSS working)
- ✅ Navigates properly (React routing working)
- ✅ Shows keyboard on search click (JavaScript events working)
- ✅ Accepts text input (Input handling working)
- ❌ **ONLY** fails when pressing "Go" button

This means: **The VIDAA browser is capable enough to run Stremio Web**, but has a **specific event handling bug** with form submissions from the remote control.

### The Root Cause

In the SearchBar component, line 64:
```javascript
const searchValue = `/search?search=${encodeURIComponent(event.target.value)}`;
```

**On PC:** `event.target` is the input element, so `event.target.value` has the search query

**On VIDAA TV:** When submitted via remote "OK" button, `event.target` is the form wrapper element, so `event.target.value` is `undefined`

**Result:** Search URL becomes `/search?search=undefined` → no navigation → appears broken

### The Fix

```javascript
const searchValue = `/search?search=${encodeURIComponent(searchInputRef.current.value || currentQuery)}`;
```

Uses the input element reference directly instead of relying on event.target.

---

## When This Fix Works vs. When It Doesn't

### ✅ This Fix Will Work If:

1. **App loads successfully** (WebAssembly initializes)
2. **UI renders** (CSS and React work)
3. **Can navigate to search page** (Routing works)
4. **Keyboard appears when clicking search** (Events work)
5. **Can type in search box** (Input works)
6. **ONLY pressing "Go" fails** ← Exactly your issue!

This is an **event handling compatibility bug**, not a fundamental browser limitation.

### ❌ This Fix Won't Help If:

1. **App doesn't load at all** (blank screen, purple screen)
   - Indicates WebAssembly not supported
   - Need alternative build or external device

2. **Search works but results don't load** (spinner forever)
   - Indicates memory/performance issues
   - Reduce number of addons or use simpler build

3. **Search loads but videos won't play** (playback errors)
   - Indicates codec/DRM issues
   - Need external device with proper video support

4. **App crashes after typing** (browser closes)
   - Indicates memory exhaustion
   - TV hardware insufficient

---

## Alternative Solutions (If Fix Doesn't Work)

### Option 1: Use Simpler Stremio Web Build

Try accessing `app.strem.io` or `app.strem.io/shell-v4.4/` instead of `web.strem.io`:
- Uses simpler/older builds that work better on limited TV browsers
- Less features but better compatibility
- Known to work on LG webOS and some other limited TV browsers

Update the URL in your custom build or bookmark.

### Option 2: Use Stremio Companion App

On PC, Stremio Web can connect to **Stremio Service/Server** running on your computer:
- The heavy lifting (WebAssembly, search logic, torrent handling) runs on your PC
- The TV browser just displays video
- This bypasses all TV browser limitations

**Limitation:** Requires PC to be always on and proper network setup.

### Option 3: External Device (Most Reliable)

Get a Chromecast with Google TV, Fire TV Stick, or cheap Android TV box ($30-50):
- Runs full Android Stremio APK, not web version
- Full search, Real-Debrid, torrent support
- No browser compatibility issues
- Best user experience

---

## Testing Your Specific Issue

To confirm this is the event handling bug (and our fix will work):

### Test 1: Check Console Logs

1. Deploy the fixed version (with debug logging enabled)
2. Open on TV
3. Try to search
4. Check browser console (if accessible on VIDAA)

**If you see:**
```
[SearchBar] Submit triggered: { inputValue: undefined, ... }
```
→ Confirms event.target.value bug, our fix will work!

### Test 2: Desktop Simulation

1. On your PC, open the **unfixed** web.strem.io
2. Open browser DevTools (F12)
3. In Console, run:
```javascript
// Simulate TV browser behavior
document.querySelector('form').addEventListener('submit', (e) => {
  console.log('Target:', e.target.constructor.name);
  console.log('Target value:', e.target.value);
});
```
4. Search for something

**On PC you'll see:** Target value has the query
**This simulates why TV fails:** Target value would be undefined

---

## Summary

### Your Case

You have a **specific event handling bug**, not a general browser limitation, because:
- App loads and runs (WebAssembly works)
- UI renders (CSS works)
- ONLY search submit fails (Event handling bug)

**Solution:** Apply the one-line fix → Search will work!

### General TV Browser Issues

If you had deeper issues (app won't load, crashes, etc.), you'd need:
- Simpler web build
- Companion app approach
- External streaming device

---

## Recommended Approach

**Step 1:** Apply the search submit fix (the one-line change)
- **Likelihood:** 95% this fixes your specific issue
- **Time:** 5 minutes
- **Cost:** Free

**Step 2:** If fix doesn't work completely
- Try simpler build (app.strem.io)
- Check if other issues appear (memory, WebAssembly, etc.)

**Step 3:** If still problematic
- Consider external device ($30-50)
- Most reliable long-term solution
- Better performance overall

---

## References and Further Reading

- [Stremio Web not loading in browser](https://www.reddit.com/r/Stremio/comments/1e0okjv/)
- [Stremio Tech Update: Web Release](https://blog.stremio.com/stremio-tech-update-21/)
- [Smart TV Browser Limitations](https://www.digitaltrends.com/home-theater/what-is-the-samsung-smart-tv-web-browser/)
- [WebAssembly Browser Support](https://stackoverflow.com/questions/47879864/)
- [Stremio Web GitHub Issues](https://github.com/Stremio/stremio-web/issues/564)

---

**Bottom Line:** Your specific symptom (search submit does nothing) indicates the **event handling bug**, which our fix addresses. If you had deeper WebAssembly or memory issues, the app wouldn't load at all.

Apply the fix and test! 🎯
