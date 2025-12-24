from datetime import datetime, timedelta
from classification_service import (
    category_classification,
    priority_detection,
    entity_extraction,
)


class TestClassificationLogic:

    def test_category_classification_technical(self):
        """Test category classification identifies technical issues correctly"""
        text = "There is a bug in the system that needs to be fixed urgently"
        result = category_classification(text)
        assert result == "technical"

    def test_priority_detection_high(self):
        """Test priority detection identifies high priority tasks"""
        text = "This is urgent and needs to be done immediately"
        result = priority_detection(text)
        assert result == "high"

    def test_entity_extraction_multiple_entities(self):
        """Test entity extraction handles multiple entities in one text"""
        text = "Schedule a call with Sarah tomorrow in office at 2pm"
        result = entity_extraction(text)
        assert "action" in result
        assert "person" in result
        assert "date" in result
        assert "time" in result
        assert "location" in result
