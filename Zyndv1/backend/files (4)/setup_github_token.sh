#!/bin/bash

# GITHUB TOKEN SETUP - 2 MINUTE FIX
# This fixes the timeout issue by authenticating with GitHub

echo "=========================================="
echo "GitHub Token Setup for Fair Hiring System"
echo "=========================================="
echo ""

# Step 1: Check if token already exists
if grep -q "GITHUB_PAT=" backend/.env; then
    echo "✅ GITHUB_PAT already exists in .env"
    echo ""
    echo "Current value:"
    grep "GITHUB_PAT=" backend/.env
    echo ""
    echo "To update it, edit backend/.env manually"
else
    echo "❌ No GitHub token found in backend/.env"
    echo ""
    echo "📝 To fix the timeout issue, you need a GitHub Personal Access Token"
    echo ""
    echo "STEP 1: Generate a token"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token (classic)'"
    echo "  3. Name: 'Fair Hiring System'"
    echo "  4. Select scopes: ONLY check 'public_repo'"
    echo "  5. Click 'Generate token'"
    echo "  6. COPY the token (shown only once!)"
    echo ""
    echo "STEP 2: Add token to system"
    read -p "Paste your GitHub token here: " github_token
    
    if [ -n "$github_token" ]; then
        # Add to .env file
        echo "" >> backend/.env
        echo "# GitHub API Token (fixes timeout issues)" >> backend/.env
        echo "GITHUB_PAT=$github_token" >> backend/.env
        
        echo ""
        echo "✅ Token added to backend/.env"
        echo ""
        echo "STEP 3: Restart the GitHub service"
        echo "  Run: pkill -f github_service"
        echo "  Then: cd agents_services && python github_service.py &"
        echo ""
        echo "VERIFICATION:"
        echo "  Without token: 60 requests/hour (will timeout)"
        echo "  With token: 5,000 requests/hour (works perfectly)"
        echo ""
        
        # Verify token works
        echo "Testing token..."
        curl -s -H "Authorization: token $github_token" https://api.github.com/rate_limit | grep -A3 '"rate"'
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Token is valid and working!"
        else
            echo ""
            echo "⚠️ Token test failed - please verify the token is correct"
        fi
    else
        echo ""
        echo "❌ No token provided. Please run this script again with a token."
    fi
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo "1. Restart GitHub service (if not done)"
echo "2. Check logs: tail -f agents_services/github.log"
echo "3. Look for: '✅ Using authenticated GitHub API (5000 req/hour)'"
echo ""
echo "Expected improvement:"
echo "  Before: Timeout after 2 minutes"
echo "  After: Completes in 30-60 seconds"
echo ""
