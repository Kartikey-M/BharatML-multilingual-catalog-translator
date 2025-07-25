# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The Multi-Lingual Product Catalog Translator team takes security seriously. We appreciate your efforts to responsibly disclose any security vulnerabilities you may find.

### How to Report a Security Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **GitHub Security Advisories** (Preferred)
   - Go to the repository's Security tab
   - Click "Report a vulnerability"
   - Fill out the security advisory form

2. **Email** (Alternative)
   - Send details to the repository maintainer
   - Include the word "SECURITY" in the subject line
   - Provide detailed information about the vulnerability

### What to Include in Your Report

To help us better understand and resolve the issue, please include:

- **Type of issue** (e.g., injection, authentication bypass, etc.)
- **Full paths of source file(s) related to the vulnerability**
- **Location of the affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions to reproduce the issue**
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the issue**, including how an attacker might exploit it

### Response Timeline

- We will acknowledge receipt of your vulnerability report within **48 hours**
- We will provide a detailed response within **7 days**
- We will work with you to understand and validate the vulnerability
- We will release a fix as soon as possible, depending on complexity

### Security Update Process

1. **Confirmation**: We confirm the vulnerability and determine its severity
2. **Fix Development**: We develop and test a fix for the vulnerability
3. **Release**: We release the security update and notify users
4. **Disclosure**: We coordinate public disclosure of the vulnerability

## Security Considerations

### Data Protection
- **Translation Data**: User input is processed in memory and not permanently stored unless explicitly saved
- **Database**: SQLite database stores translation history locally - no external data transmission
- **API Security**: Input validation and sanitization to prevent injection attacks

### Infrastructure Security
- **Dependencies**: Regular updates to address known vulnerabilities
- **Environment Variables**: Sensitive configuration stored in environment files (not committed)
- **CORS**: Proper Cross-Origin Resource Sharing configuration
- **Input Validation**: Comprehensive validation using Pydantic models

### Deployment Security
- **Docker**: Containerized deployment with minimal attack surface
- **Cloud Deployment**: Secure configuration for cloud platforms
- **Network**: Proper network configuration and access controls

### Known Security Limitations
- **AI Model**: Translation models are loaded locally - ensure sufficient system resources
- **File System**: Local file storage - implement proper access controls in production
- **Rate Limiting**: Not implemented by default - consider adding for production use

## Security Best Practices for Users

### Development Environment
- Use virtual environments to isolate dependencies
- Keep dependencies updated with `pip install -U`
- Use environment variables for sensitive configuration
- Never commit `.env` files with real credentials

### Production Deployment
- Use HTTPS in production environments
- Implement proper authentication and authorization
- Configure firewall rules to restrict access
- Monitor logs for suspicious activity
- Regular security updates and patches

### API Usage
- Validate all user inputs before processing
- Implement rate limiting for public APIs
- Use proper error handling to avoid information disclosure
- Log security-relevant events for monitoring

## Vulnerability Disclosure Policy

We follow responsible disclosure practices:

1. **Private Disclosure**: Security issues are handled privately until a fix is available
2. **Coordinated Release**: We coordinate the release of security fixes with disclosure
3. **Public Acknowledgment**: We acknowledge security researchers who report vulnerabilities
4. **CVE Assignment**: We work with CVE authorities for significant vulnerabilities

## Security Contact

For security-related questions or concerns that are not vulnerabilities:
- Check our documentation for security best practices
- Create a GitHub issue with the `security` label
- Join our community discussions for general security questions

## Third-Party Security

This project uses several third-party dependencies:

### AI/ML Components
- **IndicTrans2**: AI4Bharat's translation models
- **PyTorch**: Machine learning framework
- **Transformers**: Hugging Face model library

### Web Framework
- **FastAPI**: Modern web framework with built-in security features
- **Streamlit**: Interactive web app framework
- **Pydantic**: Data validation and serialization

### Database
- **SQLite**: Lightweight database engine

We regularly monitor security advisories for these dependencies and update them as needed.

## Compliance

This project aims to follow security best practices including:
- **OWASP Top 10**: Protection against common web application vulnerabilities
- **Input Validation**: Comprehensive validation of all user inputs
- **Error Handling**: Secure error handling that doesn't leak sensitive information
- **Logging**: Security event logging for monitoring and auditing

---

Thank you for helping keep the Multi-Lingual Product Catalog Translator secure! 🔒
