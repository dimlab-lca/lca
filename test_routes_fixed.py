#!/usr/bin/env python3
"""
Test script to verify all routes work correctly
Run this to test before deploying to production
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

def test_routes():
    """Test all application routes"""
    
    print("🧪 Testing LCA TV Routes - Root Domain Configuration")
    print("=" * 70)
    
    # Create test client
    with app.test_client() as client:
        
        # Test public routes
        public_routes = [
            ('/', 'Home Page'),
            ('/videos', 'Videos Page'),
            ('/live', 'Live Stream Page'),
            ('/about', 'About Page'),
            ('/contact', 'Contact Page'),
            ('/emissions', 'Emissions Page'),
            ('/journal', 'Journal Page'),
            ('/publicite', 'Publicite Page'),
        ]
        
        print("\n📄 Testing Public Routes:")
        print("-" * 70)
        for route, name in public_routes:
            response = client.get(route)
            status = "✅ OK" if response.status_code == 200 else f"❌ FAILED ({response.status_code})"
            print(f"{status:12} | {route:30} | {name}")
        
        # Test admin routes (without login)
        admin_routes = [
            ('/login', 'Login Page'),
            ('/dashboard', 'Dashboard (should redirect)'),
        ]
        
        print("\n🔐 Testing Admin Routes:")
        print("-" * 70)
        for route, name in admin_routes:
            response = client.get(route, follow_redirects=False)
            if route == '/login':
                status = "✅ OK" if response.status_code == 200 else f"❌ FAILED ({response.status_code})"
            else:
                # Dashboard should redirect to login (302) or return 401
                status = "✅ OK" if response.status_code in [302, 401] else f"❌ FAILED ({response.status_code})"
            print(f"{status:12} | {route:30} | {name}")
        
        # Test API routes
        api_routes = [
            ('/api/videos', 'API Videos'),
            ('/health', 'Health Check'),
            ('/debug', 'Debug Info'),
        ]
        
        print("\n📡 Testing API Routes:")
        print("-" * 70)
        for route, name in api_routes:
            response = client.get(route)
            status = "✅ OK" if response.status_code == 200 else f"❌ FAILED ({response.status_code})"
            print(f"{status:12} | {route:30} | {name}")
        
        # Test 404 handling
        print("\n🔍 Testing Error Handling:")
        print("-" * 70)
        response = client.get('/nonexistent-page')
        status = "✅ OK" if response.status_code == 404 else f"❌ FAILED ({response.status_code})"
        print(f"{status:12} | /nonexistent-page            | 404 Error Page")
        
        # Check configuration
        print("\n⚙️  Application Configuration:")
        print("-" * 70)
        print(f"APPLICATION_ROOT: {app.config.get('APPLICATION_ROOT')}")
        print(f"DEBUG: {app.config.get('DEBUG')}")
        print(f"PREFERRED_URL_SCHEME: {app.config.get('PREFERRED_URL_SCHEME')}")
        
        # Show URL map
        print("\n🗺️  Available Routes:")
        print("-" * 70)
        routes_list = []
        for rule in app.url_map.iter_rules():
            if not str(rule).startswith('/static'):
                routes_list.append(str(rule))
        
        for route in sorted(routes_list):
            print(f"   {route}")
        
    print("\n" + "=" * 70)
    print("✅ Route testing complete!")
    print("=" * 70)

if __name__ == '__main__':
    test_routes()
