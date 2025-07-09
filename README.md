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
- Node.js (for mobile testing with uiautomator2 and Appium)
- For mobile testing:
  - Appium Server
  - Android SDK (for Android testing)
  - Xcode (for iOS testing)

## Environment Setup

### Node.js Installation

Node.js is required for mobile testing with uiautomator2 and Appium:

1. **Install Node.js**:
   ```bash
   # On macOS with Homebrew
   brew install node

   # Or download from https://nodejs.org/
   ```

2. **Verify Node.js installation**:
   ```bash
   node --version
   npm --version
   ```

3. **Install Appium globally** (optional, can be installed per project):
   ```bash
   npm install -g appium
   ```

### Java Configuration

The framework requires Java for Appium and Android testing. Follow these steps to configure Java:
Ignore if mobile testing is not required.

1. **Install Java JDK** (if not already installed):
   ```bash
   # On macOS with Homebrew
   brew install openjdk

   # Or download from Oracle/OpenJDK website. Better to download and install, cause it handles the ENV VARS and PATH setup.
   ```

2. **Set JAVA_HOME and PATH** (automatically configured in your `.zshrc`):
   ```bash
   # Java Configuration
   export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home
   export PATH=$JAVA_HOME/bin:$PATH
   ```

3. **Verify Java installation**:
   ```bash
   java -version
   echo $JAVA_HOME
   ```

### Android SDK Configuration

For Android mobile testing, configure the Android SDK:

1. **Install Android Studio** (includes Android SDK) or download standalone SDK

2. **Set ANDROID_HOME and PATH** (automatically configured in your `.zshrc`):
   ```bash
   # Android SDK Configuration
   export ANDROID_HOME=$HOME/Library/Android/sdk
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/tools/bin
   ```

3. **Verify Android SDK setup**:
   ```bash
   echo $ANDROID_HOME
   adb version
   ```

4. **Install required Android SDK components**:
   - Platform Tools (latest version)
   - Build Tools
   - Android Platform (API level for your target devices)
   - Android Emulator
   - System Images (for emulator testing)

### Complete Environment Configuration

Your `.zshrc` file should include these configurations:

```bash
# Python aliases
alias python=python3
alias pip=pip3

# Java Configuration
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home
export PATH=$JAVA_HOME/bin:$PATH

# Android SDK Configuration
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
```

After updating `.zshrc`, reload the configuration:
```bash
source ~/.zshrc
```

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

## Mobile Automation Setup (Node.js & Appium)

To streamline mobile environment setup, this project uses a `package.json` and Makefile targets for Appium and driver installation.

### One-Step Mobile Setup

To install Appium and the uiautomator2 driver:
```bash
make mobile-setup
```
This will:
- Install Appium locally (in `node_modules`)
- Install the uiautomator2 driver for Android automation

### Clean Mobile Environment

To remove all Node.js/Appium dependencies and lock files:
```bash
make clean-mobile
```

### Rebuild Mobile Environment

To fully clean and reinstall the mobile automation environment:
```bash
make rebuild-mobile-setup
```

### How it works
- The `package.json` declares Appium as a dependency and provides a script to install the uiautomator2 driver.
- The Makefile targets automate the install, clean, and rebuild steps for mobile automation.

### Customization
- To add more Appium drivers (e.g., for iOS), extend the `install-appium-drivers` script in `package.json` or add new scripts.

