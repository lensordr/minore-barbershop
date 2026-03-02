#!/bin/bash
# Pre-commit hook to run tests before allowing commit
# Install: cp pre-commit.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

echo "🧪 Running pre-commit checks..."

# Run critical tests
echo "Running critical tests..."
pytest tests/test_critical_logic.py -m critical -q 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Critical tests failed! Commit blocked."
    echo "Fix the issues or use 'git commit --no-verify' to skip (not recommended)"
    exit 1
fi

# Check for common issues
echo "Checking for common issues..."

# Check for print statements in production code (should use logging)
if grep -r "print(" main.py crud.py | grep -v "# DEBUG" | grep -v "#.*print"; then
    echo "⚠️  Warning: Found print() statements. Consider using logging instead."
fi

# Check for hardcoded credentials
if grep -r "password.*=.*['\"]" main.py crud.py | grep -v "Form("; then
    echo "⚠️  Warning: Possible hardcoded credentials found!"
fi

echo "✅ Pre-commit checks passed!"
exit 0
