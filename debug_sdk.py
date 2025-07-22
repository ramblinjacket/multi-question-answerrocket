#!/usr/bin/env python3
"""
Debug script to explore AnswerRocket SDK methods
"""

from answer_rocket import AnswerRocketClient
import os

# Check environment variables
ar_url = os.environ.get('AR_URL', '').rstrip('/')
ar_token = os.environ.get('AR_TOKEN')

print(f"AR_URL: {ar_url}")
print(f"AR_TOKEN: {'***' if ar_token else 'Not set'}")

if not ar_url or not ar_token:
    print("Environment variables not properly set!")
    exit(1)

# Create client
client = AnswerRocketClient(url=ar_url, token=ar_token)

print("=== AnswerRocket Client Inspection ===")
print(f"Client class: {type(client)}")

# Check what's available on client.chat
print(f"\n=== Client.chat attributes ===")
if hasattr(client, 'chat'):
    chat_attrs = [attr for attr in dir(client.chat) if not attr.startswith('_')]
    for attr in chat_attrs:
        attr_obj = getattr(client.chat, attr)
        print(f"  {attr}: {type(attr_obj)}")
        if callable(attr_obj):
            try:
                import inspect
                sig = inspect.signature(attr_obj)
                print(f"    Signature: {attr}{sig}")
            except:
                print(f"    Signature: Could not inspect")

# Check main client attributes
print(f"\n=== Main client attributes ===")
main_attrs = [attr for attr in dir(client) if not attr.startswith('_')]
for attr in main_attrs:
    attr_obj = getattr(client, attr)
    if not callable(attr_obj):
        print(f"  {attr}: {attr_obj}")
    else:
        print(f"  {attr}: {type(attr_obj)} (method)")