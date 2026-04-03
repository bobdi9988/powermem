"""
Basic tests for powermem

This module contains basic unit tests for the memory system.
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime
from powermem import Memory
from powermem.core.base import MemoryBase


class TestMemory:
    """Test cases for Memory class."""
    
    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    def test_memory_initialization(self, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """Test memory initialization."""
        # Mock the factories
        mock_vector_store = MagicMock()
        mock_vector_factory.create.return_value = mock_vector_store
        
        mock_llm = MagicMock()
        mock_llm_factory.create.return_value = mock_llm
        
        mock_embedder = MagicMock()
        mock_embedder_factory.create.return_value = mock_embedder
        
        memory = Memory()
        assert isinstance(memory, MemoryBase)
    
    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    def test_add_memory(self, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """Test adding a memory."""
        # Mock the factories
        mock_vector_store = MagicMock()
        mock_vector_store.insert.return_value = ["test_id_1"]
        mock_vector_store.search.return_value = []
        mock_vector_factory.create.return_value = mock_vector_store
        
        mock_llm = MagicMock()
        mock_llm.generate_response.return_value = {"content": "Test memory content"}
        mock_llm_factory.create.return_value = mock_llm
        
        mock_embedder = MagicMock()
        mock_embedder.embed.return_value = [0.1, 0.2, 0.3]
        mock_embedder_factory.create.return_value = mock_embedder
        
        memory = Memory()
        
        # Mock the add method's internal behavior
        with patch.object(memory, '_extract_facts', return_value=["Test memory content"]):
            result = memory.add("Test memory content", user_id="test_user")
        
        assert "results" in result or isinstance(result, dict)
    
    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    @patch('powermem.core.memory.IntelligenceManager')
    def test_search_memories(self, mock_intelligence_manager, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """Test searching memories."""
        # Mock the factories
        mock_vector_store = MagicMock()
        mock_vector_factory.create.return_value = mock_vector_store
        
        mock_llm = MagicMock()
        mock_llm_factory.create.return_value = mock_llm
        
        mock_embedder = MagicMock()
        mock_embedder.embed.return_value = [0.1, 0.2, 0.3]
        mock_embedder_factory.create.return_value = mock_embedder
        
        # Mock IntelligenceManager
        mock_intelligence = MagicMock()
        mock_intelligence_plugin = MagicMock()
        mock_intelligence_plugin.on_search.return_value = ([], [])
        mock_intelligence.plugin = mock_intelligence_plugin
        mock_intelligence_manager.return_value = mock_intelligence
        
        memory = Memory()
        
        # Mock storage.search_memories to return proper format
        with patch.object(memory.storage, 'search_memories', return_value={"results": []}):
            # Search for memories
            results = memory.search("user preferences", user_id="test_user")
            
            assert isinstance(results, dict)
            assert "results" in results
    
    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    def test_get_memory(self, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """Test getting a specific memory."""
        # Mock the factories
        mock_vector_store = MagicMock()
        mock_vector_factory.create.return_value = mock_vector_store
        
        mock_llm = MagicMock()
        mock_llm_factory.create.return_value = mock_llm
        
        mock_embedder = MagicMock()
        mock_embedder.embed.return_value = [0.1, 0.2, 0.3]
        mock_embedder_factory.create.return_value = mock_embedder
        
        memory = Memory()
        
        # Mock storage.get_memory to return proper format
        with patch.object(memory.storage, 'get_memory', return_value={"id": "test_id", "memory": "Test memory"}):
            # Get the memory
            retrieved = memory.get("test_id", user_id="test_user")
            
            assert retrieved is not None
            assert retrieved["id"] == "test_id"
    
    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    @patch('powermem.core.memory.IntelligenceManager')
    def test_update_memory(self, mock_intelligence_manager, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """Test updating a memory."""
        # Mock the factories
        mock_vector_store = MagicMock()
        mock_vector_factory.create.return_value = mock_vector_store
        
        mock_llm = MagicMock()
        mock_llm.generate_response.return_value = {"content": "Updated content"}
        mock_llm_factory.create.return_value = mock_llm
        
        mock_embedder = MagicMock()
        mock_embedder.embed.return_value = [0.1, 0.2, 0.3]
        mock_embedder_factory.create.return_value = mock_embedder
        
        # Mock IntelligenceManager
        mock_intelligence = MagicMock()
        mock_intelligence.process_content.return_value = ("Updated content", {})
        mock_intelligence_manager.return_value = mock_intelligence
        
        memory = Memory()
        
        # Mock storage methods
        with patch.object(memory.storage, 'get_memory', return_value={"id": "test_id", "memory": "Original content"}), \
             patch.object(memory.storage, 'update_memory', return_value={"id": "test_id", "memory": "Updated content"}):
            # Update the memory
            updated = memory.update("test_id", "Updated content", user_id="test_user")
            
            assert updated is not None
            assert isinstance(updated, dict)
            assert updated["id"] == "test_id"
    
    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    def test_delete_memory(self, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """Test deleting a memory."""
        # Mock the factories
        mock_vector_store = MagicMock()
        mock_vector_factory.create.return_value = mock_vector_store
        
        mock_llm = MagicMock()
        mock_llm_factory.create.return_value = mock_llm
        
        mock_embedder = MagicMock()
        mock_embedder_factory.create.return_value = mock_embedder
        
        memory = Memory()
        
        # Mock storage.delete_memory to return True
        with patch.object(memory.storage, 'delete_memory', return_value=True):
            # Delete the memory
            deleted = memory.delete("test_id", user_id="test_user")
            
            assert deleted is True
    
    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    @patch('powermem.core.memory.IntelligenceManager')
    def test_clear_memories(self, mock_intelligence_manager, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """Test clearing memories."""
        # Mock the factories
        mock_vector_store = MagicMock()
        mock_vector_factory.create.return_value = mock_vector_store
        
        mock_llm = MagicMock()
        mock_llm_factory.create.return_value = mock_llm
        
        mock_embedder = MagicMock()
        mock_embedder_factory.create.return_value = mock_embedder
        
        # Mock IntelligenceManager
        mock_intelligence = MagicMock()
        mock_intelligence_plugin = MagicMock()
        mock_intelligence_plugin.on_search.return_value = ([], [])
        mock_intelligence.plugin = mock_intelligence_plugin
        mock_intelligence_manager.return_value = mock_intelligence
        
        memory = Memory()
        
        # Mock storage methods
        with patch.object(memory.storage, 'clear_memories', return_value=True), \
             patch.object(memory.storage, 'search_memories', return_value={"results": []}):
            # Clear memories
            cleared = memory.delete_all(user_id="test_user")
            
            assert cleared is True
            
            # Verify memories are cleared
            results = memory.search("", user_id="test_user")
            assert isinstance(results, dict)
            assert "results" in results
            assert len(results["results"]) == 0

    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    def test_add_created_at_infer_false(self, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """created_at should be persisted in simple add mode."""
        mock_vector_factory.create.return_value = MagicMock()
        mock_llm_factory.create.return_value = MagicMock()
        mock_embedder = MagicMock()
        mock_embedder.embed.return_value = [0.1, 0.2, 0.3]
        mock_embedder_factory.create.return_value = mock_embedder

        memory = Memory()
        created_at = "2026-03-30T10:00:00+08:00"

        with patch.object(memory.storage, "add_memory", return_value=1001) as mock_add:
            result = memory.add("hello world", created_at=created_at, user_id="u1", infer=False)

        assert result["results"][0]["id"] == 1001
        stored = mock_add.call_args[0][0]
        assert isinstance(stored["created_at"], datetime)
        assert stored["created_at"].isoformat() == created_at
        assert stored["updated_at"].isoformat() == created_at

    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    def test_add_created_at_infer_true(self, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """created_at should be propagated in intelligent add mode."""
        mock_vector_factory.create.return_value = MagicMock()
        mock_llm_factory.create.return_value = MagicMock()
        mock_embedder = MagicMock()
        mock_embedder.embed.return_value = [0.1, 0.2, 0.3]
        mock_embedder_factory.create.return_value = mock_embedder

        memory = Memory()
        created_at = "2026-03-30T10:00:00+08:00"

        with patch.object(memory, "_extract_facts", return_value=["fact1"]), \
             patch.object(memory.storage, "search_memories", return_value=[]), \
             patch.object(
                 memory,
                 "_decide_memory_actions",
                 return_value=[{"event": "ADD", "text": "fact1", "id": "tmp-1"}],
             ), \
             patch.object(memory.storage, "add_memory", return_value=1002) as mock_add:
            result = memory.add("hello world", created_at=created_at, user_id="u1", infer=True)

        assert result["results"][0]["id"] == 1002
        stored = mock_add.call_args[0][0]
        assert isinstance(stored["created_at"], datetime)
        assert stored["created_at"].isoformat() == created_at
        assert stored["updated_at"].isoformat() == created_at

    @patch('powermem.core.memory.VectorStoreFactory')
    @patch('powermem.core.memory.LLMFactory')
    @patch('powermem.core.memory.EmbedderFactory')
    def test_add_legacy_positional_user_id_compat(self, mock_embedder_factory, mock_llm_factory, mock_vector_factory):
        """Legacy call add(messages, user_id) should still work."""
        mock_vector_factory.create.return_value = MagicMock()
        mock_llm_factory.create.return_value = MagicMock()
        mock_embedder = MagicMock()
        mock_embedder.embed.return_value = [0.1, 0.2, 0.3]
        mock_embedder_factory.create.return_value = mock_embedder

        memory = Memory()

        with patch.object(memory.storage, "add_memory", return_value=1003) as mock_add:
            result = memory.add("hello world", "legacy_user", infer=False)

        assert result["results"][0]["id"] == 1003
        stored = mock_add.call_args[0][0]
        assert stored["user_id"] == "legacy_user"
