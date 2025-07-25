# Contributing to Multi-Lingual Product Catalog Translator

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Multi-Lingual Product Catalog Translator.

## 🤝 How to Contribute

### 1. Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/BharatMLStack.git
   cd BharatMLStack
   ```

### 2. Set Up Development Environment
Follow the setup instructions in the [README.md](README.md) to get your development environment running.

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Write clean, documented code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes
```bash
# Test backend
cd backend
python -m pytest

# Test frontend manually
cd ../frontend
streamlit run app.py
```

### 6. Commit Your Changes
Use conventional commit messages:
```bash
git commit -m "feat: add new translation feature"
git commit -m "fix: resolve translation accuracy issue"
git commit -m "docs: update API documentation"
```

### 7. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a pull request on GitHub.

## 🐛 Reporting Issues

### Bug Reports
When reporting bugs, please include:
- **Environment**: OS, Python version, browser
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Error messages**: Full error text/stack traces

### Feature Requests
When requesting features, please include:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought of
- **Additional context**: Any other relevant information

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

### Commit Message Format
We use conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Documentation Style
- Use clear, concise language
- Include code examples where helpful
- Update relevant documentation with code changes
- Use proper Markdown formatting

## 🧪 Testing Guidelines

### Backend Testing
- Write unit tests for all business logic
- Test error conditions and edge cases
- Mock external dependencies (AI models, database)
- Aim for high test coverage

### Frontend Testing
- Test user workflows manually
- Verify responsiveness across devices
- Test error handling and edge cases
- Ensure accessibility compliance

## 🔍 Review Process

### Pull Request Guidelines
- Keep PRs focused on a single feature/fix
- Write clear PR descriptions
- Include screenshots for UI changes
- Link related issues using keywords (fixes #123)
- Ensure all tests pass
- Request reviews from maintainers

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No sensitive information is committed
- [ ] Performance impact is considered
- [ ] Security implications are reviewed

## 📚 Development Resources

### AI/ML Components
- [IndicTrans2 Documentation](https://github.com/AI4Bharat/IndicTrans2)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [PyTorch Documentation](https://pytorch.org/docs/)

### Web Development
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Deployment
- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)

## 🏷️ Release Process

### Version Numbering
We follow semantic versioning (SemVer):
- **MAJOR.MINOR.PATCH**
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Version numbers are bumped
- [ ] Tag is created and pushed
- [ ] Release notes are written

## 🙋‍♀️ Getting Help

### Community Support
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check existing docs first

### Maintainer Contact
- Create an issue for technical questions
- Use discussions for general inquiries
- Be patient and respectful in all interactions

## 📄 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code.

### Our Standards
- **Be respectful**: Treat everyone with kindness and respect
- **Be inclusive**: Welcome people of all backgrounds and experience levels
- **Be constructive**: Provide helpful feedback and suggestions
- **Be patient**: Remember that everyone is learning

Thank you for contributing to make this project better! 🚀
