#!/usr/bin/env python3
"""
Environment Variable Debug Script
This script helps diagnose issues with environment variable loading.
"""

import os
from dotenv import load_dotenv

def debug_env_vars():
    """Debug environment variables"""
    print("🔍 Environment Variable Debug Script")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ .env file found: {env_file}")
        
        # Read .env file content
        with open(env_file, 'r') as f:
            content = f.read()
            print(f"\n📄 .env file content:")
            for line in content.split('\n'):
                if 'GOOGLE_API_KEY' in line and not line.startswith('#'):
                    print(f"   {line}")
                    break
    else:
        print(f"❌ .env file NOT found: {env_file}")
    
    print(f"\n🔧 Loading environment variables...")
    
    # Load .env file explicitly
    loaded = load_dotenv()
    print(f"   dotenv loaded: {loaded}")
    
    # Check environment variable
    env_api_key = os.getenv('GOOGLE_API_KEY')
    print(f"   os.getenv('GOOGLE_API_KEY'): {env_api_key}")
    
    if env_api_key:
        print(f"   API Key length: {len(env_api_key)}")
        print(f"   API Key preview: {env_api_key[:8]}...{env_api_key[-4:]}")
    else:
        print("   API Key is None or empty")
    
    # Check all environment variables that might contain API key
    print(f"\n🔍 Checking all environment variables for API keys:")
    for key, value in os.environ.items():
        if 'API' in key.upper() or 'KEY' in key.upper():
            if 'AI' in value or 'AIza' in value:
                print(f"   {key}: {value[:8]}...{value[-4:] if len(value) > 12 else value}")
    
    # Check if there's a difference
    hardcoded_key = "AIzaSyDyGvRUJDd34R5iTj1ME_0HTSjGOVVLknc"  # Your working key
    
    if env_api_key == hardcoded_key:
        print(f"\n✅ Environment variable matches hardcoded key")
    else:
        print(f"\n❌ MISMATCH DETECTED!")
        print(f"   Hardcoded key: {hardcoded_key[:8]}...{hardcoded_key[-4:]}")
        print(f"   Env var key:   {env_api_key[:8] if env_api_key else 'None'}...{env_api_key[-4:] if env_api_key and len(env_api_key) > 12 else ''}")
        
        if env_api_key:
            print(f"\n📝 Detailed comparison:")
            print(f"   Hardcoded length: {len(hardcoded_key)}")
            print(f"   Env var length:   {len(env_api_key)}")
            print(f"   Keys equal: {env_api_key == hardcoded_key}")

if __name__ == "__main__":
    debug_env_vars()