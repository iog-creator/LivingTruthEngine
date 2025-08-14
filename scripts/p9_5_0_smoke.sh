#!/bin/bash

# Phase 9.5.0 Smoke Test Script
# Tests real adapters with deduplication and transcript mode persistence

set -e

echo "=== Phase 9.5.0 Smoke Test - Real Adapters ==="
echo ""

# Check if system is running
echo "1. Checking system health..."
if ! curl -s http://localhost:8050/api/health/full | jq -e '.data.all_gates_passed' > /dev/null; then
    echo "❌ Health check failed"
    exit 1
fi
echo "✅ Health check passed"

# Test YouTube adapter
echo ""
echo "2. Testing YouTube adapter..."
YOUTUBE_RESULT=$(curl -s -X POST http://localhost:8050/api/test/youtube_adapter \
  -H 'Content-Type: application/json' \
  -d '{"channel_url":"https://www.youtube.com/@imaginationpodcastofficial","limit":2,"transcript_mode":"autosubs"}')

if echo "$YOUTUBE_RESULT" | jq -e '.status == "ok"' > /dev/null; then
    DOC_COUNT=$(echo "$YOUTUBE_RESULT" | jq '.data.documents_count')
    echo "✅ YouTube adapter test passed: $DOC_COUNT documents"
else
    echo "❌ YouTube adapter test failed"
    echo "$YOUTUBE_RESULT" | jq '.error.message'
    exit 1
fi

# Test web adapter
echo ""
echo "3. Testing web adapter..."
WEB_RESULT=$(curl -s -X POST http://localhost:8050/api/test/web_adapter \
  -H 'Content-Type: application/json' \
  -d '{"urls":["https://example.com"],"max_depth":1,"js_render":false}')

if echo "$WEB_RESULT" | jq -e '.status == "ok"' > /dev/null; then
    DOC_COUNT=$(echo "$WEB_RESULT" | jq '.data.documents_count')
    EXTRACTION_METHOD=$(echo "$WEB_RESULT" | jq -r '.data.documents[0].metadata.extraction_method')
    echo "✅ Web adapter test passed: $DOC_COUNT documents (method: $EXTRACTION_METHOD)"
else
    echo "❌ Web adapter test failed"
    echo "$WEB_RESULT" | jq '.error.message'
    exit 1
fi

# Test PDF adapter
echo ""
echo "4. Testing PDF adapter..."
PDF_RESULT=$(curl -s -X POST http://localhost:8050/api/test/pdf_adapter \
  -H 'Content-Type: application/json' \
  -d '{"urls":["https://example.com/sample.pdf"],"ocr_required":false,"auto_retry":true}')

if echo "$PDF_RESULT" | jq -e '.status == "ok"' > /dev/null; then
    DOC_COUNT=$(echo "$PDF_RESULT" | jq '.data.documents_count')
    EXTRACTION_METHOD=$(echo "$PDF_RESULT" | jq -r '.data.documents[0].metadata.extraction_method')
    echo "✅ PDF adapter test passed: $DOC_COUNT documents (method: $EXTRACTION_METHOD)"
else
    echo "❌ PDF adapter test failed"
    echo "$PDF_RESULT" | jq '.error.message'
    exit 1
fi

# Test multi-source run
echo ""
echo "5. Testing multi-source run..."
MULTI_RESULT=$(curl -s -X POST http://localhost:8050/api/test/multi_source_run \
  -H 'Content-Type: application/json' \
  -d '{"job_label":"Phase 9.5.0 Smoke Test"}')

if echo "$MULTI_RESULT" | jq -e '.status == "ok"' > /dev/null; then
    JOB_ID=$(echo "$MULTI_RESULT" | jq -r '.data.job_id')
    JOB_STATUS=$(echo "$MULTI_RESULT" | jq -r '.data.job_status.status')
    echo "✅ Multi-source run test passed: Job $JOB_ID ($JOB_STATUS)"
else
    echo "❌ Multi-source run test failed"
    echo "$MULTI_RESULT" | jq '.error.message'
    exit 1
fi

# Test deduplication
echo ""
echo "6. Testing deduplication..."
DEDUP_RESULT=$(curl -s -X POST http://localhost:8050/api/test/deduplication \
  -H 'Content-Type: application/json' \
  -d '{"test_content":"This is duplicate content","iterations":3}')

if echo "$DEDUP_RESULT" | jq -e '.status == "ok"' > /dev/null; then
    UNIQUE_COUNT=$(echo "$DEDUP_RESULT" | jq '.data.unique_documents')
    TOTAL_COUNT=$(echo "$DEDUP_RESULT" | jq '.data.total_documents')
    echo "✅ Deduplication test passed: $UNIQUE_COUNT unique from $TOTAL_COUNT total"
else
    echo "❌ Deduplication test failed"
    echo "$DEDUP_RESULT" | jq '.error.message'
    exit 1
fi

# Test transcript mode persistence
echo ""
echo "7. Testing transcript mode persistence..."
TRANSCRIPT_RESULT=$(curl -s -X POST http://localhost:8050/api/test/transcript_persistence \
  -H 'Content-Type: application/json' \
  -d '{"transcript_mode":"autosubs","channel_url":"https://www.youtube.com/@imaginationpodcastofficial"}')

if echo "$TRANSCRIPT_RESULT" | jq -e '.status == "ok"' > /dev/null; then
    PERSISTED_MODE=$(echo "$TRANSCRIPT_RESULT" | jq -r '.data.persisted_transcript_mode')
    echo "✅ Transcript mode persistence test passed: $PERSISTED_MODE"
else
    echo "❌ Transcript mode persistence test failed"
    echo "$TRANSCRIPT_RESULT" | jq '.error.message'
    exit 1
fi

# Test enhanced extraction with real URLs
echo ""
echo "8. Testing enhanced extraction with real URLs..."
ENHANCED_RESULT=$(curl -s -X POST http://localhost:8050/api/test/enhanced_extraction \
  -H 'Content-Type: application/json' \
  -d '{"web_url":"https://httpbin.org/html","pdf_url":"https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"}')

if echo "$ENHANCED_RESULT" | jq -e '.status == "ok"' > /dev/null; then
    WEB_METHOD=$(echo "$ENHANCED_RESULT" | jq -r '.data.web_extraction_method')
    WEB_DETAIL=$(echo "$ENHANCED_RESULT" | jq -r '.data.web_extraction_detail')
    PDF_METHOD=$(echo "$ENHANCED_RESULT" | jq -r '.data.pdf_extraction_method')
    PDF_DETAIL=$(echo "$ENHANCED_RESULT" | jq -r '.data.pdf_extraction_detail')
    echo "✅ Enhanced extraction test passed: Web($WEB_METHOD: $WEB_DETAIL), PDF($PDF_METHOD: $PDF_DETAIL)"
else
    echo "❌ Enhanced extraction test failed"
    echo "$ENHANCED_RESULT" | jq '.error.message'
    exit 1
fi

echo ""
echo "=== Phase 9.5.0a Smoke Test Results ==="
echo "✅ All tests passed"
echo "✅ Real adapters working"
echo "✅ Enhanced extraction functional"
echo "✅ Deduplication functional"
echo "✅ Transcript mode persisted"
echo "✅ Multi-source runs operational"
echo ""
echo "Phase 9.5.0a - Adapter Internals Upgrade: COMPLETED"
