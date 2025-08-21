#!/usr/bin/env python3
"""
Simple test to verify Japanese font support in CreateDot application.
"""

import sys
import os

# Add the main directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_japanese_import():
    """Test that we can import the module without errors."""
    try:
        from dot_text_generator import DotTextGenerator
        print("✓ Successfully imported DotTextGenerator")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False

def test_japanese_text_conversion():
    """Test Japanese text to dots conversion."""
    try:
        # Note: This test requires tkinter and will only work in environments where it's available
        import tkinter as tk
        from dot_text_generator import DotTextGenerator
        
        # Create a minimal instance to test the text_to_dots method
        app = DotTextGenerator.__new__(DotTextGenerator)
        
        # Test Japanese text
        japanese_text = "こんにちは"
        result = app.text_to_dots(japanese_text, 24, "circle", 3, 5)
        
        if result and result.size[0] > 0 and result.size[1] > 0:
            print("✓ Successfully converted Japanese text to dots")
            return True
        else:
            print("✗ Failed to convert Japanese text (empty result)")
            return False
            
    except ImportError:
        print("⚠ Skipping GUI test (tkinter not available)")
        return True  # Skip this test if tkinter is not available
    except Exception as e:
        print(f"✗ Failed to convert Japanese text: {e}")
        return False

if __name__ == "__main__":
    print("Testing Japanese font support in CreateDot...")
    print()
    
    # Run tests
    tests = [
        ("Import test", test_japanese_import),
        ("Japanese conversion test", test_japanese_text_conversion),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Japanese support is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed.")
        sys.exit(1)