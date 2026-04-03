"""
Basic usage example for powermem

This example demonstrates basic memory operations.

Setup:
1. Copy .env.example to configs/.env
2. Add your API keys to configs/.env
3. Run this script

Or simply run without config - it will use mock providers for demonstration.
"""

import os
from dotenv import load_dotenv
from powermem import create_memory, auto_config

def search_memories(memory, query: str, user_id: str):
    search_response = memory.search(query, user_id=user_id)
    results = search_response.get("results", [])
    print(f"search: {query} user_id: {user_id}")
    print(f"Found {len(results)} results:")
    for result in results:
        print(f"- {result['created_at']} {result['memory']}")
    print()


def main():
    """Basic usage example."""
    print("=" * 60)
    print("Powermem Basic Usage Example")
    print("=" * 60)

    # Check if .env exists and load it
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    env_example_path = os.path.join(os.path.dirname(__file__), "..", "env.example")

    if not os.path.exists(env_path):
        print(f"\n No .env file found at: {env_path}")
        print(f"To add your API keys:")
        print(f"   1. Copy: cp {env_example_path} {env_path}")
        print(f"   2. Edit {env_path} and add your API keys")
        print(f"\n  For now, using mock providers for demonstration...")
    else:
        print(f"Found .env file")
        # Explicitly load configs/.env file
        load_dotenv(env_path, override=True)
        # Ensure create_memory()/auto_config loads the exact same env file path.
        os.environ["POWERMEM_ENV_FILE"] = env_path

    
    print("\nInitializing memory...")

    # Keep demo output deterministic for CLI verification.
    config = auto_config()
    if "intelligent_memory" not in config or not isinstance(config.get("intelligent_memory"), dict):
        config["intelligent_memory"] = {}
    config["intelligent_memory"]["enabled"] = False
    if "memory_decay" not in config or not isinstance(config.get("memory_decay"), dict):
        config["memory_decay"] = {}
    config["memory_decay"]["enabled"] = False
    memory = create_memory(config=config)

    print("✓ Memory initialized successfully!\n")

    # Add some memories
    print("Adding memories...")
    memory.add("User likes coffee", user_id="user123", created_at="2026-02-25 10:00:00")
    memory.add("User prefers Python over Java", user_id="user123", created_at="2026-03-20 10:00:00")
    memory.add("User works as a software engineer", user_id="user123", created_at="2026-03-25 10:00:00")
    memory.add("用户今天上午吃了苹果和香蕉", user_id="user123", created_at="2026-03-28 10:00:00")
    memory.add("用户昨天晚上没睡觉，但是吃了一个香蕉", user_id="user123", created_at="2026-03-30 10:00:00")
    print("✓ Memories added!\n")

    # Search memories
    print("Searching memories...")
    search_memories(memory, "用户吃过香蕉", "user123")
    search_memories(memory, "用户更喜欢苹果", "user123")
    search_memories(memory, "用户吃过水果", "user123")
    search_memories(memory, "用户是软件工程师", "user123")
    search_memories(memory, "昨晚干啥了", "user123")

    # Get all memories
    all_memories = memory.get_all(user_id="user123")
    print(f"✓ Total memories: {len(all_memories.get('results', []))}")

    return

if __name__ == "__main__":
    main()
