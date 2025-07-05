#!/usr/bin/env python3
"""
Test script for YouTube Downloader language functionality
"""

import os
import sys
import gettext
import locale
from pathlib import Path

def test_gettext_setup():
    print("Testing gettext setup...")
    locales_dir = Path("locales")
    if not locales_dir.exists():
        print("ERROR: locales directory not found")
        return False
    print("OK: locales directory found")
    ja_mo = locales_dir / "ja/LC_MESSAGES/messages.mo"
    en_mo = locales_dir / "en/LC_MESSAGES/messages.mo"
    if not ja_mo.exists():
        print("ERROR: ja/LC_MESSAGES/messages.mo not found")
        return False
    print("OK: ja/LC_MESSAGES/messages.mo found")
    if not en_mo.exists():
        print("ERROR: en/LC_MESSAGES/messages.mo not found")
        return False
    print("OK: en/LC_MESSAGES/messages.mo found")
    return True

def test_japanese_translation():
    print("\nTesting Japanese translation...")
    try:
        t = gettext.translation('messages', localedir='locales', languages=['ja'])
        _ = t.gettext
        test_strings = [
            ("=== YouTube Downloader ===", "=== YouTube ダウンローダー ==="),
            ("1. Download Video/Audio", "1. 動画/音声をダウンロード"),
            ("2. Help", "2. ヘルプ"),
            ("3. Language Settings", "3. 言語設定"),
            ("4. Exit", "4. 終了")
        ]
        for src, expected in test_strings:
            translated = _(src)
            print(f"  '{src}' -> '{translated}'")
            if translated == expected:
                print(f"    OK: Correctly translated")
            else:
                print(f"    ERROR: Incorrect translation: expected '{expected}'")
                return False
        return True
    except Exception as e:
        print(f"ERROR: Error loading Japanese translation: {e}")
        return False

def test_english_translation():
    print("\nTesting English translation...")
    try:
        t = gettext.translation('messages', localedir='locales', languages=['en'])
        _ = t.gettext
        test_strings = [
            "=== YouTube Downloader ===",
            "1. Download Video/Audio",
            "2. Help",
            "3. Language Settings",
            "4. Exit"
        ]
        for src in test_strings:
            translated = _(src)
            print(f"  '{src}' -> '{translated}'")
            if translated == src:
                print(f"    OK: English fallback working")
            else:
                print(f"    ERROR: Unexpected translation: got '{translated}'")
                return False
        return True
    except Exception as e:
        print(f"ERROR: Error loading English translation: {e}")
        return False

def main():
    print("YouTube Downloader Language Test Suite")
    print("=" * 50)
    tests = [
        ("Gettext Setup", test_gettext_setup),
        ("Japanese Translation", test_japanese_translation),
        ("English Translation", test_english_translation)
    ]
    passed = 0
    total = len(tests)
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"OK: {test_name}: PASSED")
            else:
                print(f"ERROR: {test_name}: FAILED")
        except Exception as e:
            print(f"ERROR: {test_name}: ERROR - {e}")
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    if passed == total:
        print("SUCCESS: All tests passed!")
        return True
    else:
        print("WARNING: Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 