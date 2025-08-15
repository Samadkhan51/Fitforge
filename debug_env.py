#!/usr/bin/env python3
"""
Debug script to check environment variables
"""
import os

print("=== ENVIRONMENT VARIABLE DEBUG ===")
print()

# Check for GOOGLE_API_KEY specifically
google_key = os.getenv("GOOGLE_API_KEY")
print(f"GOOGLE_API_KEY: {'Found' if google_key else 'NOT FOUND'}")
if google_key:
    print(f"  Value starts with: {google_key[:10]}...")
    print(f"  Length: {len(google_key)}")

print()
print("=== ALL ENVIRONMENT VARIABLES ===")

# Print all environment variables
for key, value in sorted(os.environ.items()):
    # Hide sensitive values
    if any(sensitive in key.upper() for sensitive in ['KEY', 'PASSWORD', 'SECRET', 'TOKEN']):
        display_value = f"{'*' * min(len(value), 10)}"
    else:
        display_value = value
    
    print(f"{key}: {display_value}")

print()
print("=== VARIABLES CONTAINING 'GOOGLE' OR 'API' ===")
for key, value in os.environ.items():
    if 'GOOGLE' in key.upper() or 'API' in key.upper():
        display_value = f"{'*' * min(len(value), 10)}" if 'KEY' in key.upper() else value
        print(f"{key}: {display_value}")
