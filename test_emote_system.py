#!/usr/bin/env python3
"""
Test script for the emote catalog and numbered emotes system
"""
from functions.numbered_emotes import initialize_numbered_emotes, get_emote_by_number, format_numbered_emotes
import sys

def test_numbered_emotes():
    """Test that numbered emotes are correctly initialized and accessible"""
    print("=== Testing Numbered Emotes ===")
    
    # Initialize the system
    emotes = initialize_numbered_emotes()
    print(f"Initialized {len(emotes)} numbered emotes")
    
    # Test specific emotes
    test_numbers = ['1', '5', '10', '15', '20', '25', '30', '31']
    for num in test_numbers:
        emote = get_emote_by_number(num)
        if emote:
            print(f"Emote #{num}: {emote}")
        else:
            print(f"Emote #{num}: Not found (expected for numbers > 30)")
    
    # Test paging
    page1 = format_numbered_emotes(1)
    print("\nPage 1 messages:")
    for msg in page1:
        print(f"  {msg}")
    
    page2 = format_numbered_emotes(2)
    print("\nPage 2 messages:")
    for msg in page2:
        print(f"  {msg}")
    
if __name__ == "__main__":
    test_numbered_emotes()
