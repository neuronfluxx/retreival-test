# Example Output

This document shows what you'll see when using the retrieval testing system with AI-powered answers.

## Interactive Mode Example

```bash
$ python test_retrieval.py

🤖 RAG Retrieval Testing with AI Answers
========================================
Namespace: (default)
Top K: 5
Generate answers: Yes ✓

Commands:
  - Type your question and press Enter
  - Type 'quit' or 'exit' to stop
  - Type 'filter:source=filename' to filter by source
  - Type 'clear' to remove filters
  - Type 'toggle' to enable/disable AI answers
----------------------------------------

❓ Question: What are the system requirements for Visual Studio Code?

⏳ Searching...
🤖 Generating answer...

================================================================================
🔍 Query: What are the system requirements for Visual Studio Code?
================================================================================

================================================================================
💡 AI ANSWER
================================================================================

Based on the provided context, Visual Studio Code requires:

**Operating System:**
- Windows 10 or 11 (64-bit)
- macOS 10.15 (Catalina) or later
- Linux with glibc 2.28 or later

**Hardware:**
- 1.6 GHz processor or faster
- 1 GB RAM minimum (8 GB recommended)
- 500 MB available disk space
- Graphics card supporting OpenGL 3.3 or higher

**Additional Requirements:**
- Internet connection for downloading and initial setup
- Administrator privileges for installation
- .NET Framework 4.5.2 or higher (Windows only)

The installation guide specifically mentions that Windows 7 and 8 are no longer 
supported as of version 1.70.

================================================================================

📊 Retrieved 5 relevant chunks:

────────────────────────────────────────────────────────────────────────────────
📄 Chunk 1 | Score: 0.8923
   Source: WINDOWS-Visual-Studio-Code-Installation-Guide.pdf (chunk #2)

System Requirements

Before installing Visual Studio Code, ensure your system meets the following 
minimum requirements:

Operating System: Windows 10 or Windows 11 (64-bit)
Processor: 1.6 GHz or faster processor
RAM: 1 GB (8 GB recommended for better performance)
Disk Space: 500 MB of available disk space
Graphics: Graphics card supporting OpenGL 3.3 or higher

────────────────────────────────────────────────────────────────────────────────
📄 Chunk 2 | Score: 0.8745
   Source: WINDOWS-Visual-Studio-Code-Installation-Guide.pdf (chunk #1)

Visual Studio Code Installation Guide for Windows

This comprehensive guide will walk you through the installation process of 
Visual Studio Code on Windows operating systems. VS Code is a lightweight but 
powerful source code editor that supports multiple programming languages.

Prerequisites:
- Administrator access to your Windows computer
- Active internet connection
- .NET Framework 4.5.2 or higher

────────────────────────────────────────────────────────────────────────────────
📄 Chunk 3 | Score: 0.8432
   Source: WINDOWS-Visual-Studio-Code-Installation-Guide.pdf (chunk #3)

Important Notes:
- Windows 7 and Windows 8 are no longer supported starting from VS Code version 1.70
- For optimal performance, we recommend at least 8 GB of RAM
- An SSD is recommended for faster startup and better responsiveness

────────────────────────────────────────────────────────────────────────────────
📄 Chunk 4 | Score: 0.7891
   Source: WINDOWS-Visual-Studio-Code-Installation-Guide.pdf (chunk #5)

Installation Steps

1. Download VS Code
   - Visit the official website: https://code.visualstudio.com
   - Click the "Download for Windows" button
   - The installer will automatically detect your system architecture

────────────────────────────────────────────────────────────────────────────────
📄 Chunk 5 | Score: 0.7654
   Source: WINDOWS-Visual-Studio-Code-Installation-Guide.pdf (chunk #8)

VS Code supports various platforms including Windows, macOS, and Linux. The 
Windows version provides native integration with Windows features and supports 
all major programming languages through extensions.


❓ Question: toggle
✅ AI answers disabled

❓ Question: How do I install extensions?

⏳ Searching...

================================================================================
🔍 Query: How do I install extensions?
================================================================================

📊 Retrieved 5 relevant chunks:

────────────────────────────────────────────────────────────────────────────────
📄 Chunk 1 | Score: 0.9012
   Source: WINDOWS-Visual-Studio-Code-Installation-Guide.pdf (chunk #12)

Installing Extensions

Visual Studio Code's functionality can be extended through extensions:

1. Open the Extensions view by clicking the Extensions icon in the Activity Bar
2. Search for the extension you need in the search box
3. Click "Install" on the extension you want to add
4. Reload VS Code if prompted

Popular extensions include:
- Python - For Python development
- ESLint - JavaScript linting
- Prettier - Code formatter
- Live Server - Local development server

────────────────────────────────────────────────────────────────────────────────
📄 Chunk 2 | Score: 0.8567
   Source: WINDOWS-Visual-Studio-Code-Installation-Guide.pdf (chunk #13)

You can also install extensions from the command line using:
code --install-extension <extension-id>

To view installed extensions, use:
code --list-extensions


❓ Question: quit

👋 Goodbye!
```

## Single Question Example

```bash
$ python test_retrieval.py --question "What is the installation process?"

⏳ Searching...
🤖 Generating answer...

================================================================================
🔍 Query: What is the installation process?
================================================================================

================================================================================
💡 AI ANSWER
================================================================================

The Visual Studio Code installation process on Windows involves these steps:

1. **Download the Installer:**
   - Visit https://code.visualstudio.com
   - Click "Download for Windows"
   - The correct version for your system will be detected automatically

2. **Run the Installer:**
   - Locate the downloaded VSCodeSetup.exe file
   - Double-click to launch the installer
   - Accept the license agreement

3. **Configure Installation Options:**
   - Choose installation location (default: C:\Program Files\Microsoft VS Code)
   - Select additional tasks:
     * Add "Open with Code" to context menu
     * Add to PATH environment variable
     * Create desktop shortcut
     * Register Code as editor for supported file types

4. **Complete Installation:**
   - Click "Install" to begin
   - Wait for the installation to complete (typically 2-3 minutes)
   - Click "Finish" to launch VS Code

Administrator privileges are required for installation.

================================================================================

📊 Retrieved 5 relevant chunks:
[... chunks displayed as shown above ...]
```

## Chunks-Only Mode (No AI Answer)

```bash
$ python test_retrieval.py --question "What are the features?" --no-generate

⏳ Searching...

================================================================================
🔍 Query: What are the features?
================================================================================

📊 Retrieved 5 relevant chunks:

────────────────────────────────────────────────────────────────────────────────
📄 Chunk 1 | Score: 0.8654
   Source: features-guide.pdf (chunk #1)

Visual Studio Code Features:
- IntelliSense code completion
- Built-in Git integration
- Integrated debugging
- Extension marketplace with thousands of extensions
...
```

## Filter Example

```bash
❓ Question: filter:source=installation-guide
✅ Filter set: {'source': 'installation-guide'}

❓ Question: What are the steps?

⏳ Searching...
🤖 Generating answer...
[... only shows results from installation-guide.pdf ...]
```

## Output Structure

Every query displays:

1. **🔍 Query** - Your question
2. **💡 AI ANSWER** - Generated answer using retrieved context (if enabled)
3. **📊 Retrieved Chunks** - Source documents with:
   - Similarity score (0-1, higher is better)
   - Source filename and chunk number
   - Full text content of the chunk

This allows you to:
- ✅ Get immediate answers
- ✅ Verify answer accuracy by reviewing source chunks
- ✅ Understand which parts of documents were most relevant
- ✅ Identify retrieval quality issues
