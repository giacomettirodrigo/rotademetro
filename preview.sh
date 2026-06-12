#!/bin/bash
# Rota de Metrô — Local Preview
# Run this once to install Jekyll and start the server

cd "$(dirname "$0")"

echo "🚇 Rota de Metrô — Local Preview"
echo ""

# Install bundler if missing
if ! gem list bundler -i > /dev/null 2>&1; then
  echo "Installing bundler..."
  gem install bundler --no-document
fi

# Install dependencies
echo "Installing Jekyll dependencies..."
bundle install

# Start the server
echo ""
echo "✅ Starting server at http://localhost:4000"
echo "   Press Ctrl+C to stop."
echo ""
bundle exec jekyll serve --livereload
