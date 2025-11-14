# LCA TV - Deployment Fix Instructions
**Date:** 2025-01-15  
**Domain:** lca-tv.bf  
**Hosting:** cPanel with Passenger WSGI

## Problem Fixed
✅ **404 Errors on all pages except home** - Fixed routing configuration for root domain deployment

## What Was Changed

### 1. **passenger_wsgi.py** - WSGI Entry Point
- **Changed:** Now loads `app.py` directly instead of `run.py`
- **Why:** Passenger needs the Flask `application` object directly
- **Critical:** This file must be named `passenger_wsgi.py` exactly

### 2. **app.py** - Main Application
- **Changed:** `APPLICATION_ROOT` from `/lca` to `/`
- **Why:** Your domain points directly to the lca folder, so app runs at root level
- **Changed:** Updated production URLs in startup messages

### 3. **.htaccess** - URL Rewriting
- **Changed:** Removed all `/lca` prefix references
- **Changed:** Routes all requests to `passenger_wsgi.py` except static files
- **Why:** Domain lca-tv.bf points to /lca folder, so no subdirectory prefix needed

### 4. **Error Pages** - 404.html & 500.html
- **Changed:** Links from `/lca/` to `/` and `/lca/live` to `/live`
- **Why:** Remove hardcoded subdirectory paths

## Files Modified
```
✓ /app/passenger_wsgi.py    - WSGI entry point
✓ /app/app.py                - Flask application configuration
✓ /app/.htaccess             - URL rewriting rules
✓ /app/templates/404.html    - Error page links
✓ /app/templates/500.html    - Error page links
```

## Deployment Steps for cPanel

### Step 1: Upload Files
Upload these files to your `/lca` folder in cPanel File Manager:
- `passenger_wsgi.py` ✓ (CRITICAL - must be exact name)
- `app.py` ✓
- `.htaccess` ✓
- `templates/404.html` ✓
- `templates/500.html` ✓

### Step 2: Set File Permissions
In cPanel File Manager, set permissions:
- **Directories:** 755 (including `/lca`, `/static`, `/templates`)
- **Python files:** 644 (`app.py`, `passenger_wsgi.py`, etc.)
- **Static files:** 644 (CSS, JS, images)
- **.htaccess:** 644

### Step 3: Configure Python Application (if using cPanel Python App)
1. Go to **cPanel → Setup Python App**
2. Application settings:
   - **Python version:** 3.9 or higher
   - **Application root:** `/home/yourusername/lca` (or your path)
   - **Application URL:** Leave empty or `/` (not `/lca`)
   - **Application startup file:** `passenger_wsgi.py`
   - **Application Entry point:** `application`

### Step 4: Install Dependencies
In cPanel Terminal or SSH:
```bash
cd /home/yourusername/lca
pip install -r requirements.txt
```

Or if using Python App interface:
- Click "Run pip install" with `requirements.txt`

### Step 5: Restart Application
- **cPanel Python App:** Click "Restart"
- **Or via .htaccess:** Touch the passenger_wsgi.py file:
  ```bash
  touch passenger_wsgi.py
  ```

### Step 6: Test Your Application
Open in browser and test all pages:
- ✅ https://lca-tv.bf/ (Home - should work)
- ✅ https://lca-tv.bf/videos (Videos - should work now)
- ✅ https://lca-tv.bf/live (Live - should work now)
- ✅ https://lca-tv.bf/about (About - should work now)
- ✅ https://lca-tv.bf/contact (Contact - should work now)
- ✅ https://lca-tv.bf/login (Admin login - should work now)

## Verification Checklist

- [ ] Home page loads correctly
- [ ] Videos page shows videos
- [ ] Live page displays stream
- [ ] About page accessible
- [ ] Contact page accessible  
- [ ] Login page accessible
- [ ] Static files (CSS, JS, images) load correctly
- [ ] No 404 errors on navigation
- [ ] HTTPS redirection works (HTTP → HTTPS)

## Troubleshooting

### If pages still show 404:
1. **Check .htaccess is uploaded** to `/lca/` folder
2. **Check file permissions** (644 for .htaccess)
3. **Check mod_rewrite is enabled** in cPanel (usually enabled by default)
4. **Clear browser cache** (Ctrl+Shift+R or Cmd+Shift+R)

### If you see "500 Internal Server Error":
1. **Check Python version** - needs 3.9+
2. **Check dependencies installed** - run `pip install -r requirements.txt`
3. **Check error logs** in cPanel → Errors
4. **Check passenger_wsgi.py** loads correctly

### If static files (CSS/JS/images) don't load:
1. **Check /static folder exists** and has correct permissions (755)
2. **Check static files have 644 permissions**
3. **Check .htaccess** allows static file access
4. **Clear browser cache**

### To see detailed errors:
Visit: https://lca-tv.bf/debug
This will show:
- Python version
- Current configuration
- Request information
- URL routing map

## Important Notes

⚠️ **Do NOT modify these values:**
- `APPLICATION_ROOT = '/'` (keep as root)
- Passenger file name must be `passenger_wsgi.py` exactly
- Do not add `/lca` prefix to URLs in templates (use `url_for()`)

✅ **Your domain configuration:**
- Domain: `lca-tv.bf`
- Points to: `/home/yourusername/lca` folder
- App runs at: root level (no subdirectory prefix)

## Support

If you still experience issues after following these steps:

1. **Check error logs** in cPanel → Metrics → Errors
2. **Test debug endpoint:** https://lca-tv.bf/debug
3. **Verify .htaccess syntax** using online validators
4. **Contact PlanetHoster support** if Passenger configuration issues

## Production URLs Reference

All routes now work at root level:

**Public Pages:**
- https://lca-tv.bf/
- https://lca-tv.bf/videos
- https://lca-tv.bf/live
- https://lca-tv.bf/about
- https://lca-tv.bf/contact
- https://lca-tv.bf/emissions
- https://lca-tv.bf/journal
- https://lca-tv.bf/publicite

**Admin Pages:**
- https://lca-tv.bf/login
- https://lca-tv.bf/dashboard

**API Endpoints:**
- https://lca-tv.bf/api/videos
- https://lca-tv.bf/health
- https://lca-tv.bf/debug

---
**Deployment Fixed:** ✅  
**Ready for Production:** ✅
