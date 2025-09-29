# scripts/setup_test_data.sh
#!/bin/bash
# Creates test data structure for development

mkdir -p test_art/TestArtist/"2024-01-01 Test Post"
echo "Test content" > test_art/TestArtist/"2024-01-01 Test Post"/links-test.txt
echo "✅ Test data created in test_art/"