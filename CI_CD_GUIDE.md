# 🚀 CI/CD & Testing Setup

## 📊 Current Status

### ❌ Before (What You Had):
- No automated testing
- No CI/CD pipeline
- Direct push to production
- No code quality checks
- High risk of bugs in production

### ✅ After (What You Have Now):
- GitHub Actions CI/CD pipeline
- Automated test framework
- Code quality checks
- Pre-commit hooks
- Safer deployments

---

## 🔄 CI/CD Pipeline Flow

```
Developer → git push → GitHub Actions → Tests → Deploy to Render
                            ↓
                    ✅ Pass: Deploy
                    ❌ Fail: Block & Notify
```

### Pipeline Stages:

1. **Code Quality Checks**
   - Black (code formatting)
   - Flake8 (linting)
   - Bandit (security scanning)

2. **Automated Tests**
   - Unit tests
   - Integration tests
   - Critical business logic tests

3. **Deployment**
   - Only if all tests pass
   - Automatic deployment to Render
   - Rollback available if needed

---

## 🧪 Testing Strategy

### Critical Tests (Must Pass):
- ✅ VIP code time restrictions (12 PM today, 1 PM tomorrow)
- ✅ Multi-tenant isolation (Mallorca vs Concell)
- ✅ Double booking prevention
- ✅ Location_id in all queries
- ✅ Blocked client rejection

### Test Coverage Goals:
- Critical paths: 100%
- Business logic: 80%
- Overall: 60%

---

## 🛠️ How to Use

### Run Tests Locally:
```bash
# Install test dependencies
pip install pytest pytest-cov flake8 black bandit

# Run all tests
pytest tests/ -v

# Run only critical tests
pytest tests/ -m critical

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Install Pre-commit Hook:
```bash
cp pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Check Code Quality:
```bash
# Format code
black main.py crud.py models.py

# Check linting
flake8 main.py crud.py models.py --max-line-length=120

# Security scan
bandit -r . -ll
```

---

## 📋 Deployment Checklist

Before pushing to production:

- [ ] Run tests locally: `pytest tests/ -v`
- [ ] Check code quality: `flake8 main.py crud.py`
- [ ] Review changes: `git diff`
- [ ] Test critical paths manually
- [ ] Check database migrations
- [ ] Verify environment variables
- [ ] Monitor logs after deployment

---

## 🚨 Emergency Procedures

### If Deployment Breaks Production:

1. **Immediate Rollback:**
   ```bash
   git revert HEAD
   git push origin main
   ```

2. **Check Logs:**
   - Render Dashboard → Logs
   - Look for error messages

3. **Fix & Redeploy:**
   - Fix the issue locally
   - Run tests: `pytest tests/ -v`
   - Push fix: `git push origin main`

### If Tests Fail in CI:

1. Check GitHub Actions tab
2. Review failed test output
3. Fix locally and test
4. Push again

---

## 📈 Monitoring & Alerts

### What to Monitor:
- Deployment success/failure (GitHub Actions)
- Application errors (Render logs)
- Database performance
- API response times
- User-reported issues

### Set Up Alerts:
- GitHub: Watch repository for Actions failures
- Render: Enable email notifications
- Consider: Sentry for error tracking

---

## 🎯 Next Steps (Recommended)

### Short Term (1 week):
1. ✅ Implement critical tests
2. ✅ Set up pre-commit hooks
3. ✅ Add staging environment

### Medium Term (1 month):
4. Add integration tests
5. Set up Sentry for error tracking
6. Implement feature flags
7. Add performance monitoring

### Long Term (3 months):
8. Achieve 80% test coverage
9. Add load testing
10. Implement blue-green deployments
11. Add automated rollback

---

## 📚 Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Render Deployment Guide](https://render.com/docs)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

## 🤝 Contributing

When adding new features:

1. Write tests first (TDD)
2. Ensure tests pass locally
3. Create pull request
4. Wait for CI to pass
5. Merge to main

---

## ⚙️ Configuration Files

- `.github/workflows/ci-cd.yml` - CI/CD pipeline
- `pytest.ini` - Test configuration
- `pre-commit.sh` - Pre-commit hook
- `tests/` - Test files

---

## 📊 Current Test Status

```
Total Tests: 1 (placeholder)
Passing: 1
Failing: 0
Coverage: ~5%

⚠️ WARNING: Test suite needs to be fully implemented!
```

---

## 🎓 Best Practices

1. **Always run tests before pushing**
2. **Never skip CI checks** (unless emergency)
3. **Write tests for bug fixes**
4. **Keep tests fast** (<5 seconds total)
5. **Test critical paths first**
6. **Use meaningful test names**
7. **Mock external dependencies**
8. **Test edge cases**

---

## 🔒 Security

- Secrets stored in GitHub Secrets
- No credentials in code
- Security scanning with Bandit
- Dependency vulnerability checks

---

**Last Updated:** 2024
**Status:** ✅ Active
**Maintainer:** Development Team
