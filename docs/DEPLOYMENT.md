# Deployment Guide

## Quick Deployment Options

### Option 1: GitHub Pages (Recommended - Free & Easy)

**Step 1: Build the project**
```bash
cd stremio-web
npm run build
```

**Step 2: Install gh-pages**
```bash
npm install -g gh-pages
```

**Step 3: Deploy**
```bash
gh-pages -d build
```

Your fixed Stremio Web will be available at:
```
https://YOUR-USERNAME.github.io/stremio-web
```

**Step 4: Bookmark on your TV**
- Open TV browser
- Navigate to your GitHub Pages URL
- Bookmark it for easy access

---

### Option 2: Netlify (Free with Auto-Deploy)

**Step 1: Create account**
- Go to https://netlify.com
- Sign up (free)

**Step 2: Deploy**

**Method A: Drag & Drop**
1. Build your project: `npm run build`
2. Go to Netlify dashboard
3. Drag the `build/` folder to Netlify
4. Done!

**Method B: Git Integration (Auto-updates)**
1. Push your modified stremio-web to GitHub
2. In Netlify: "New site from Git"
3. Connect to your repository
4. Build settings:
   - Build command: `npm run build`
   - Publish directory: `build`
5. Deploy!

Your site will be at: `https://YOUR-SITE.netlify.app`

**Enable HTTPS (Required for WebAssembly):**
- Automatically enabled by Netlify
- No configuration needed

---

### Option 3: Vercel (Free with Edge Network)

**Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

**Step 2: Deploy**
```bash
cd stremio-web
vercel
```

Follow the prompts, and you'll get a URL like:
```
https://stremio-web-fixed.vercel.app
```

**Custom Domain:**
```bash
vercel --prod
vercel alias YOUR-DEPLOYMENT.vercel.app stremio.yourdomain.com
```

---

### Option 4: Self-Hosted (Full Control)

#### Requirements
- Web server (nginx, Apache, or Node.js)
- HTTPS certificate (required for WebAssembly)
- Domain or IP address

#### Using Nginx

**Step 1: Build**
```bash
cd stremio-web
npm run build
```

**Step 2: Copy files to server**
```bash
scp -r build/* user@your-server:/var/www/stremio-web/
```

**Step 3: Configure Nginx**

Create `/etc/nginx/sites-available/stremio-web`:

```nginx
server {
    listen 443 ssl http2;
    server_name stremio.yourdomain.com;

    # SSL certificates (required!)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    root /var/www/stremio-web;
    index index.html;

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript application/wasm;

    # SPA routing - serve index.html for all routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|wasm)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # WASM MIME type (important!)
    types {
        application/wasm wasm;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name stremio.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

**Step 4: Enable site**
```bash
sudo ln -s /etc/nginx/sites-available/stremio-web /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Using Apache

**httpd.conf or virtual host:**

```apache
<VirtualHost *:443>
    ServerName stremio.yourdomain.com
    DocumentRoot /var/www/stremio-web

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/yourdomain.com/chain.pem

    <Directory /var/www/stremio-web>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted

        # SPA routing
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>

    # WASM MIME type
    AddType application/wasm .wasm
</VirtualHost>
```

#### Getting Free HTTPS Certificate

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate (for nginx)
sudo certbot --nginx -d stremio.yourdomain.com

# Or for Apache
sudo certbot --apache -d stremio.yourdomain.com

# Auto-renewal (certbot sets this up automatically)
sudo certbot renew --dry-run
```

---

### Option 5: Docker Container

**Dockerfile:**

```dockerfile
FROM node:16-alpine AS builder

WORKDIR /app
COPY stremio-web/package*.json ./
RUN npm install
COPY stremio-web .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf:**

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|wasm)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Build and run:**

```bash
docker build -t stremio-web-fixed .
docker run -d -p 8080:80 stremio-web-fixed
```

Access at: `http://localhost:8080`

**For HTTPS with Docker:**
Use a reverse proxy like Traefik or nginx-proxy with Let's Encrypt companion.

---

## Post-Deployment Checklist

### 1. Test HTTPS
- ✅ Site loads over HTTPS (required for WebAssembly)
- ✅ No SSL certificate errors
- ✅ Mixed content warnings resolved

### 2. Test Search Functionality
- ✅ Search icon clickable
- ✅ Keyboard appears when clicked
- ✅ Can type in search box
- ✅ **Pressing Enter triggers search**
- ✅ Loading indicator appears
- ✅ Results display correctly

### 3. Test on TV Browser
- ✅ Site loads on TV
- ✅ Remote control navigation works
- ✅ Search works with TV remote "OK" button
- ✅ Video playback works

### 4. Performance
- ✅ Initial load < 5 seconds
- ✅ Search results load < 3 seconds
- ✅ No console errors (press F12 on desktop browser)

### 5. Debug Console
- ✅ Can open with Ctrl+Shift+D
- ✅ Shows search logs
- ✅ Displays any errors

---

## Troubleshooting Deployment

### Issue: "Failed to load WASM"

**Cause**: Not served over HTTPS or wrong MIME type

**Solution:**
1. Ensure HTTPS is enabled
2. Add WASM MIME type:
   ```nginx
   types {
       application/wasm wasm;
   }
   ```

### Issue: "404 on page refresh"

**Cause**: Server not configured for SPA routing

**Solution:** Add rewrite rules (see nginx/Apache config above)

### Issue: "Mixed content" warnings

**Cause**: Loading HTTP resources on HTTPS page

**Solution:**
1. Check browser console for mixed content
2. Update all resource URLs to HTTPS
3. Use protocol-relative URLs: `//domain.com/resource`

### Issue: Slow loading

**Solutions:**
1. Enable gzip compression
2. Add caching headers
3. Use a CDN (Cloudflare is free)
4. Optimize build:
   ```bash
   npm run build -- --production
   ```

---

## CDN Integration (Optional)

### Cloudflare (Free Tier)

**Benefits:**
- Free SSL
- DDoS protection
- Caching
- Global CDN

**Steps:**
1. Sign up at cloudflare.com
2. Add your domain
3. Update nameservers
4. Enable "Full SSL" mode
5. Turn on caching

**Cloudflare Settings:**
- SSL/TLS: Full
- Auto Minify: JS, CSS, HTML
- Brotli compression: On
- Browser cache TTL: 4 hours

---

## Updating Your Deployment

### GitHub Pages
```bash
npm run build
gh-pages -d build
```

### Netlify
- **Drag & Drop**: Upload new `build/` folder
- **Git**: Push to repository (auto-deploys)

### Vercel
```bash
vercel --prod
```

### Self-Hosted
```bash
npm run build
scp -r build/* user@server:/var/www/stremio-web/
```

---

## Multiple Environments

### Development
```bash
npm start
# http://localhost:8080
```

### Staging
```bash
npm run build
# Deploy to staging.yourdomain.com
```

### Production
```bash
npm run build -- --production
# Deploy to yourdomain.com
```

---

## Custom Domain Setup

### For GitHub Pages

**Add CNAME file:**
```bash
echo "stremio.yourdomain.com" > build/CNAME
```

**Update DNS:**
- Type: CNAME
- Name: stremio (or @)
- Value: yourusername.github.io

### For Netlify

**In Netlify Dashboard:**
1. Domain settings
2. Add custom domain
3. Follow DNS instructions

### For Vercel

```bash
vercel alias YOUR-DEPLOYMENT.vercel.app stremio.yourdomain.com
```

Then update DNS as instructed.

---

## Monitoring

### Check if site is up
- https://uptimerobot.com (free monitoring)
- https://statuscake.com (free tier)

### Analytics (Optional)
- Google Analytics
- Plausible (privacy-friendly)
- Self-hosted Matomo

---

## Backup Strategy

**Automated backups:**

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/stremio-web"

# Backup web files
tar -czf "$BACKUP_DIR/stremio-web-$DATE.tar.gz" /var/www/stremio-web

# Keep last 7 days
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
```

Add to cron:
```bash
0 2 * * * /usr/local/bin/backup.sh
```

---

## Need Help?

**Common issues:**
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- GitHub Issues: https://github.com/YOUR-REPO/issues

**Test your deployment:**
```
✅ HTTPS enabled
✅ Search works on desktop
✅ Search works on TV
✅ No console errors
✅ Debug console accessible
```

If all checked, you're good to go! 🎉
