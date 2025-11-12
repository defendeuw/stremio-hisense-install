# Troubleshooting Guide

## Search Issues

### Issue: Search button does nothing when clicked

**Symptoms:**
- ✅ Search icon works
- ✅ Keyboard appears
- ✅ Can type
- ❌ Pressing "Go" or Enter does nothing
- ❌ No results appear

**Cause:** TV browser event handling differs from desktop browsers

**Solution:**
1. Ensure you're using our fixed SearchBar.js
2. Clear browser cache on TV:
   - Settings → Apps → Browser → Clear Data
3. Try force-refreshing the page (Ctrl+R or Ctrl+F5)
4. Enable debug console (Ctrl+Shift+D) to see if events are firing

**Verification:**
- Open debug console
- Type in search box
- Press Enter
- You should see: `[SearchBar] Enter detected, triggering search`

---

### Issue: Search returns no results

**Symptom:** Search works but always shows "No results found"

**Possible Causes:**

#### 1. No addons installed

**Check:**
- Go to https://web.strem.io
- Click Board → Add-ons
- Do you have any content addons?

**Solution:**
- Install Cinemeta (official addon)
- Install other content addons

#### 2. Broken addons

**Check:**
- Enable debug console (Ctrl+Shift+D)
- Search for something
- Look for errors like: `[useSearch] Addon X failed: Timeout`

**Solution:**
- Go to https://profile-debugger.strem.io/#
- Log in
- Remove broken addons
- Try search again

#### 3. Network issues

**Check:**
- Can you load videos?
- Is your internet working?

**Solution:**
- Check TV network connection
- Restart router
- Try different network

---

### Issue: Search is very slow

**Symptoms:**
- Search works but takes 30+ seconds
- Loading spinner shows for a long time

**Causes:**
1. Too many addons installed
2. Slow addons
3. Slow internet connection

**Solutions:**

**Quick fix:**
- Reduce number of addons (keep only 3-5)
- Remove slow/broken addons

**Identify slow addons:**
1. Enable debug console (Ctrl+Shift+D)
2. Search for something
3. Look for addons that show "Timeout" or take >5 seconds
4. Remove those addons from your profile

**Increase timeout (for slow connections):**
In `fixes/useSearch.js`, change line:
```javascript
setTimeout(() => reject(new Error('Timeout')), 10000)
// Change 10000 to 30000 (30 seconds)
```

---

### Issue: Some searches work, others don't

**Symptoms:**
- Search for "Avatar" works
- Search for "The Office" doesn't work
- Inconsistent behavior

**Cause:** Special characters or specific addon issues

**Solutions:**

**Try simpler queries:**
- Instead of "The Office" try "Office"
- Instead of "Spider-Man: No Way Home" try "Spider Man"
- Avoid special characters: - : ' "

**Check addon compatibility:**
- Enable debug console
- Search for failing query
- See which addon fails
- Remove that addon or try different addons

---

## WebAssembly Issues

### Issue: "Failed to load WASM module"

**Cause:** Not using HTTPS or wrong MIME type

**Solutions:**

**1. Enable HTTPS:**
- WebAssembly REQUIRES HTTPS
- Deploy to GitHub Pages, Netlify, or use SSL certificate
- `http://` will NOT work, must be `https://`

**2. Check WASM MIME type:**

For nginx, add to config:
```nginx
types {
    application/wasm wasm;
}
```

For Apache, add:
```apache
AddType application/wasm .wasm
```

**3. Verify in browser:**
- Open site
- Press F12 (developer console)
- Check Network tab
- Look for .wasm file
- Content-Type should be `application/wasm`

---

### Issue: "CORS error loading WASM"

**Symptoms:**
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```

**Solution:**

Add CORS headers to server config:

**Nginx:**
```nginx
add_header Access-Control-Allow-Origin * always;
add_header Access-Control-Allow-Methods "GET, OPTIONS" always;
```

**Apache:**
```apache
Header set Access-Control-Allow-Origin "*"
Header set Access-Control-Allow-Methods "GET, OPTIONS"
```

---

## TV Browser Issues

### Issue: Can't navigate with remote control

**Symptoms:**
- Mouse cursor appears but can't be controlled
- Remote buttons don't work
- Stuck on page

**Solutions:**

**1. Enable TV mode in browser:**
- Browser Settings → View Mode → TV Mode

**2. Try different browser:**
- Some Hisense TVs have multiple browsers
- Try "Internet" app vs "Browser" app

**3. Use USB mouse (temporary):**
- Plug in USB mouse
- Navigate and bookmark the site
- Remove mouse

---

### Issue: Keyboard doesn't appear for search

**Symptoms:**
- Click search icon
- No keyboard shows up
- Can't type

**Solutions:**

**1. Enable on-screen keyboard:**
- TV Settings → Accessibility → On-screen Keyboard → Enable

**2. Use external keyboard:**
- Plug USB keyboard into TV
- Type directly

**3. Try different browser:**
- Some browsers have better keyboard support

---

### Issue: Site loads but looks broken

**Symptoms:**
- Layout is messed up
- Buttons overlapping
- Text unreadable

**Solutions:**

**1. Clear browser cache:**
- Settings → Apps → Browser → Clear Data

**2. Check zoom level:**
- Browser might be zoomed in
- Reset zoom: Ctrl+0 or Menu → Zoom → 100%

**3. Update TV firmware:**
- Settings → System → Software Update

---

## Performance Issues

### Issue: Site is very slow/laggy

**Symptoms:**
- Clicking takes several seconds
- Animations stuttering
- Page freezing

**Solutions:**

**1. Close other apps:**
- TV has limited RAM
- Close all other apps before using Stremio

**2. Restart TV:**
- Full power cycle (unplug for 30 seconds)

**3. Clear browser data:**
- Settings → Apps → Browser → Clear Data

**4. Reduce addons:**
- Fewer addons = faster performance
- Keep only essential addons

---

## Deployment Issues

### Issue: 404 error when refreshing page

**Symptom:** Going to `/board` works, but refreshing gives 404

**Cause:** Server not configured for SPA routing

**Solution:**

**Nginx:**
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

**Apache:**
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```

---

### Issue: "Mixed content" warnings

**Symptom:**
```
Mixed Content: The page at 'https://...' was loaded over HTTPS,
but requested an insecure resource 'http://...'
```

**Cause:** Loading HTTP resources on HTTPS page

**Solution:**

**1. Update resource URLs:**
```javascript
// Bad
const url = 'http://example.com/image.jpg';

// Good
const url = 'https://example.com/image.jpg';
```

**2. Use protocol-relative URLs:**
```javascript
const url = '//example.com/image.jpg'; // Uses same protocol as page
```

---

### Issue: Build fails with errors

**Common build errors:**

#### Error: "Cannot find module"

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Error: "Out of memory"

**Solution:**
```bash
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

#### Error: "Permission denied"

**Solution:**
```bash
sudo chown -R $USER:$USER .
npm run build
```

---

## Debug Console Not Working

### Issue: Can't open debug console (Ctrl+Shift+D doesn't work)

**Solutions:**

**1. Try on desktop browser first:**
- Test on your computer
- Make sure it works there

**2. Alternative: URL parameter:**
- Add `?debug=true` to URL
- Example: `https://your-site.com/?debug=true`

**3. Check browser compatibility:**
- Some TV browsers don't support all keyboard shortcuts
- May need to implement alternative trigger (button in UI)

---

## Addon Issues

### Issue: Can't add/remove addons

**Symptom:** Changes to addons don't save

**Cause:** Not logged in or sync issue

**Solutions:**

**1. Log in to Stremio account:**
- Click profile icon
- Log in

**2. Force sync:**
- Log out
- Log back in
- Wait for sync to complete

**3. Use profile debugger:**
- Go to: https://profile-debugger.strem.io/#
- Log in
- Make changes there
- Refresh Stremio Web

---

### Issue: Addon returns no streams

**Symptom:** Movie/show found but no streams available

**Causes:**
1. Addon server is down
2. Addon doesn't have that content
3. Addon requires configuration

**Solutions:**

**1. Check addon status:**
- Try on desktop browser first
- Visit addon manifest URL directly

**2. Install more addons:**
- Cinemeta (metadata only)
- Torrentio (popular for streams)
- Other community addons

**3. Check addon configuration:**
- Some addons need API keys
- Configure in addon settings

---

## Emergency Fixes

### Nuclear option: Complete reset

If nothing works:

```bash
# Re-clone stremio-web
rm -rf stremio-web
git clone https://github.com/Stremio/stremio-web.git
cd stremio-web

# Fresh install
rm -rf node_modules
npm install

# Apply fixes again
cp ../fixes/* src/routes/Search/

# Rebuild
npm run build

# Redeploy
```

---

## Getting Debug Information

When reporting issues, include:

**1. Browser info:**
- TV model: _______
- Browser version: _______
- Vidaa OS version: _______

**2. Debug console output:**
- Enable debug console (Ctrl+Shift+D)
- Reproduce issue
- Take photo of console
- Include in bug report

**3. Network tab:**
- Press F12
- Go to Network tab
- Try to search
- Screenshot any red (failed) requests

**4. Console errors:**
- Press F12
- Go to Console tab
- Look for red error messages
- Copy/screenshot errors

---

## Still Not Working?

**Try the official web version:**
- https://web.strem.io
- Does search work there?
- If yes → Issue with our fixes
- If no → Issue with Stremio Web or your setup

**Test on different device:**
- Try on your phone
- Try on your computer
- Helps isolate if it's TV-specific

**Check Stremio status:**
- https://status.strem.io
- Are Stremio services up?

**Community help:**
- Stremio Reddit: r/Stremio
- Stremio Discord
- GitHub issues

---

## Reporting Bugs

When opening an issue, include:

```markdown
## Bug Description
[Describe what's wrong]

## Steps to Reproduce
1. Go to...
2. Click on...
3. See error

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- TV Model: Hisense PX1TUK-PRO
- Browser: [Version]
- Vidaa OS: [Version]
- Stremio Web Version: [Git commit hash]

## Debug Console Output
[Screenshot or text]

## Screenshots
[If applicable]

## Additional Context
[Anything else relevant]
```

---

## Quick Diagnostic Checklist

```
☐ HTTPS enabled
☐ Can load the site
☐ Can click search icon
☐ Keyboard appears
☐ Can type in search box
☐ Pressing Enter logs to debug console
☐ Loading indicator appears
☐ At least one addon installed
☐ Addons responding (check debug console)
☐ Results appear (or error message)
☐ Can click on results
☐ Videos play
```

If any step fails, that's where to focus troubleshooting!

---

**Most Common Fixes (Try These First):**

1. ✅ Use HTTPS (required for WASM)
2. ✅ Clear TV browser cache
3. ✅ Reduce number of addons (keep 3-5)
4. ✅ Remove broken addons via profile debugger
5. ✅ Restart TV
6. ✅ Use simpler search queries (no special characters)
7. ✅ Enable debug console to see what's happening

90% of issues are fixed by one of the above!
