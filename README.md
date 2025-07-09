# Automate-UI

A comprehensive framework for automating Web and Mobile UI testing using the Screenplay pattern. This framework provides a clean, maintainable approach to writing automated tests with support for both web browsers (via Playwright) and mobile devices (via Appium).

## Features

- **Screenplay Pattern**: Clean, maintainable test architecture
- **Web Automation**: Browser automation using Playwright
- **Mobile Automation**: iOS and Android automation using Appium
- **User Personas**: Generate realistic test data with Faker
- **Comprehensive Testing**: Support for pytest with various plugins
- **Code Quality**: Built-in linting, formatting, and type checking

Note: Type checking can be tweaked according to the comfort and understanding of the team.


## Prerequisites

- Python 3.11 or higher
- Make (for using the provided Makefile commands)
- For mobile testing:
  - Appium Server
  - Android SDK (for Android testing)
  - Xcode (for iOS testing)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd automate-web
```

### 2. Set Up Virtual Environment and Install Dependencies

The project provides several convenient Makefile commands for setup:

#### Quick Setup (Recommended)
```bash
make local-setup
```

This command will:
- Create a virtual environment
- Install all dependencies (including dev dependencies)
- Install Playwright browsers

#### Manual Setup Steps

If you prefer to run commands manually:

```bash
# Create virtual environment
make venv

# Install Playwright browsers
make install-playwright

# Or do everything at once
make build-ui
```

#### Alternative: Rebuild Everything
If you need to start fresh:
```bash
make rebuild-local
```

### 3. Verify Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests to verify everything works
make test
```


## Development Commands

### Code Quality
```bash
# Lint code
make lint

# Format code
make format

# Clean up generated files
make clean
```

### Testing
```bash
# Run all unit tests
make test

### Package Management
```bash
# Build package
make package

# Clean package artifacts
make package-clean
```

## Usage Examples

### Web Testing
For a complete example of web testing with the framework, see the test file `tests/unit/test_actor_factory.py`. This test demonstrates:
- Creating an actor with web browsing capabilities
- Navigating to a URL
- Taking screenshots
- Querying page information
- Working with user personas

### Mobile Testing
```python
from automate_ui.screenplay.abilities.use_phone import UsePhone, PhoneCapabilities

# Create phone capabilities
capabilities = PhoneCapabilities(
    platform_name='Android',
    automation_name='uiautomator2',
    device_name='Medium_Phone_API_35'
)

# Create actor with phone ability
actor = Actor("Mobile User")
actor.add_ability(UsePhone.with_capabilities(capabilities))
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting: `make test && make lint`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This project is currently under active development. Some features may be subject to change.

