#!/bin/bash
# Quick Start Script for Physical AI Living Textbook

echo "🚀 Physical AI Living Textbook - Quick Start"
echo "==========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    echo "Run this script from the project root directory"
    exit 1
fi

echo "📦 Installing dependencies..."
cd frontend
npm install

if [ $? -ne 0 ]; then
    echo "❌ npm install failed"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

echo "🎨 Starting development server..."
echo "The site will open at http://localhost:3000 or http://localhost:4000"
echo ""
echo "📚 What to explore:"
echo "  • Homepage: /"
echo "  • Textbook intro: /docs/intro"
echo "  • Chapter 1: /docs/module-1/chapter-1-python-intro"
echo ""
echo "💡 Tips:"
echo "  • Press Ctrl+C to stop the server"
echo "  • Open http://localhost:3000 in your browser"
echo "  • Changes auto-reload in development mode"
echo ""

npm start
