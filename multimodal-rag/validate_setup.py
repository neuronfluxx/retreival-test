#!/usr/bin/env python3
"""
Setup Validation Script
Run this to verify your installation is correct
"""

import sys
from pathlib import Path


def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def check_python_version():
    """Check Python version"""
    print("\n✓ Checking Python version...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("  ✓ Python version OK")
        return True
    else:
        print("  ✗ Python 3.10+ required")
        return False


def check_imports():
    """Check if core modules can be imported"""
    print("\n✓ Checking core imports...")
    
    imports = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("chromadb", "ChromaDB"),
        ("openai", "OpenAI"),
        ("PIL", "Pillow"),
        ("easyocr", "EasyOCR"),
        ("transformers", "Transformers"),
        ("torch", "PyTorch"),
    ]
    
    all_ok = True
    for module, name in imports:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - not installed")
            all_ok = False
    
    return all_ok


def check_app_modules():
    """Check if app modules can be imported"""
    print("\n✓ Checking app modules...")
    
    modules = [
        "app.config",
        "app.main",
        "app.core.embeddings",
        "app.core.vector_store",
        "app.core.document_processor",
        "app.core.rag_engine",
        "app.models.clip_model",
        "app.models.ocr_models",
        "app.agents.orchestrator",
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except Exception as e:
            print(f"  ✗ {module} - {e}")
            all_ok = False
    
    return all_ok


def check_directories():
    """Check if required directories exist"""
    print("\n✓ Checking directories...")
    
    dirs = [
        "app",
        "app/api",
        "app/core",
        "app/models",
        "app/agents",
        "data",
        "logs",
        "tests",
    ]
    
    all_ok = True
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - missing")
            all_ok = False
    
    return all_ok


def check_env_file():
    """Check .env file"""
    print("\n✓ Checking environment configuration...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("  ✗ .env file not found")
        return False
    
    print("  ✓ .env file exists")
    
    # Check key variables
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT",
        "CHROMA_PERSIST_DIR",
    ]
    
    with open(env_path) as f:
        content = f.read()
    
    all_ok = True
    for var in required_vars:
        if var in content:
            # Check if it has a value (not empty)
            for line in content.split('\n'):
                if line.startswith(var):
                    if '=' in line and len(line.split('=')[1].strip()) > 0:
                        print(f"  ✓ {var} configured")
                    else:
                        print(f"  ✗ {var} is empty")
                        all_ok = False
                    break
        else:
            print(f"  ✗ {var} not found")
            all_ok = False
    
    return all_ok


def check_models():
    """Check if models can be initialized"""
    print("\n✓ Checking model initialization...")
    
    try:
        from app.config import get_settings
        settings = get_settings()
        print("  ✓ Settings loaded")
    except Exception as e:
        print(f"  ✗ Settings failed: {e}")
        return False
    
    try:
        from app.models import get_clip_embedder
        embedder = get_clip_embedder()
        print("  ✓ CLIP model loaded")
    except Exception as e:
        print(f"  ✗ CLIP model failed: {e}")
        return False
    
    try:
        from app.core.vector_store import get_vector_store
        vector_store = get_vector_store()
        print("  ✓ Vector store initialized")
    except Exception as e:
        print(f"  ✗ Vector store failed: {e}")
        return False
    
    return True


def test_embedding_generation():
    """Test embedding generation"""
    print("\n✓ Testing embedding generation...")
    
    try:
        from app.core.embeddings import get_embedding_generator
        
        generator = get_embedding_generator()
        
        # Test text embedding
        text = "This is a test"
        embedding = generator.generate_text_embedding(text)
        
        if embedding and len(embedding) > 0:
            print(f"  ✓ Text embedding generated (dim: {len(embedding)})")
        else:
            print("  ✗ Text embedding failed")
            return False
        
        # Test CLIP embedding
        from app.models import get_clip_embedder
        clip = get_clip_embedder()
        clip_emb = clip.encode_text("test")
        
        if clip_emb is not None and len(clip_emb) > 0:
            print(f"  ✓ Image embedding ready (dim: {clip_emb.shape[1]})")
        else:
            print("  ✗ Image embedding failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Embedding test failed: {e}")
        return False


def main():
    """Run all checks"""
    print_section("Multimodal RAG Setup Validation")
    
    checks = [
        ("Python Version", check_python_version),
        ("Core Dependencies", check_imports),
        ("App Modules", check_app_modules),
        ("Directory Structure", check_directories),
        ("Environment Config", check_env_file),
        ("Model Initialization", check_models),
        ("Embedding Generation", test_embedding_generation),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n✗ {name} check failed with error: {e}")
            results[name] = False
    
    # Summary
    print_section("Summary")
    
    all_passed = all(results.values())
    
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print()
    
    if all_passed:
        print("✓ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Start the service: make run")
        print("  2. Open API docs: http://localhost:8003/docs")
        print("  3. Upload a document and start querying!")
        return 0
    else:
        print("✗ Some checks failed. Please review the errors above.")
        print("\nTroubleshooting:")
        print("  1. Check SETUP.md for detailed instructions")
        print("  2. Verify .env file has correct values")
        print("  3. Run: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
