"""
Simple test to verify the project structure and imports
Run with: python test_basic.py
"""

import sys
import os

def test_project_structure():
    """Test that all required files and directories exist"""
    print("Testing project structure...")
    
    required_files = [
        'config.py',
        'analyze.py',
        'requirements.txt',
        'README.md',
        'QUICK_START.md',
        'DOCUMENTATION.md',
        'setup.sh',
        'src/__init__.py',
        'src/data_loader.py',
        'src/text_analyzer.py',
        'src/visualizer.py',
        'data/ejemplo_formulario.csv',
        'notebooks/analisis_interactivo.ipynb',
    ]
    
    required_dirs = [
        'src',
        'data',
        'output',
        'notebooks',
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    for dir in required_dirs:
        if not os.path.isdir(dir):
            missing_dirs.append(dir)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✓ All required files and directories exist")
    return True


def test_config():
    """Test that config can be imported and has required attributes"""
    print("\nTesting config...")
    
    try:
        import config
        
        required_attrs = [
            'DATA_DIR',
            'OUTPUT_DIR',
            'SPACY_MODEL',
            'TEXT_COLUMN',
        ]
        
        missing_attrs = []
        for attr in required_attrs:
            if not hasattr(config, attr):
                missing_attrs.append(attr)
        
        if missing_attrs:
            print(f"❌ Missing config attributes: {missing_attrs}")
            return False
        
        print(f"✓ Config loaded successfully")
        print(f"  - Model: {config.SPACY_MODEL}")
        print(f"  - Data dir: {config.DATA_DIR}")
        print(f"  - Output dir: {config.OUTPUT_DIR}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False


def test_python_syntax():
    """Test that all Python files have valid syntax"""
    print("\nTesting Python syntax...")
    
    python_files = [
        'config.py',
        'analyze.py',
        'src/__init__.py',
        'src/data_loader.py',
        'src/text_analyzer.py',
        'src/visualizer.py',
    ]
    
    import py_compile
    
    for file in python_files:
        try:
            py_compile.compile(file, doraise=True)
        except Exception as e:
            print(f"❌ Syntax error in {file}: {e}")
            return False
    
    print(f"✓ All {len(python_files)} Python files have valid syntax")
    return True


def test_data_file():
    """Test that the example data file is valid"""
    print("\nTesting example data file...")
    
    data_file = 'data/ejemplo_formulario.csv'
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 2:
            print(f"❌ Data file has insufficient rows")
            return False
        
        header = lines[0].strip()
        if 'Respuesta' not in header:
            print(f"❌ Data file missing 'Respuesta' column")
            return False
        
        print(f"✓ Example data file is valid ({len(lines)} rows)")
        print(f"  - Columns: {header}")
        return True
        
    except Exception as e:
        print(f"❌ Error reading data file: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Project Structure Verification")
    print("=" * 60)
    
    tests = [
        test_project_structure,
        test_config,
        test_python_syntax,
        test_data_file,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All tests passed!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Download spaCy model: python -m spacy download es_core_news_sm")
        print("3. Run analysis: python analyze.py data/ejemplo_formulario.csv --text-column Respuesta")
        return 0
    else:
        print(f"❌ {sum(1 for r in results if not r)} test(s) failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
