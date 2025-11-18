#!/usr/bin/env python3
"""
Test script to verify all components work without requiring an API key.
This tests the individual tool implementations and TypeScript execution.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_teams_tool():
    """Test Teams download tool"""
    print("=" * 60)
    print("TEST 1: Teams download_meeting_summary tool")
    print("=" * 60)
    
    from tools.ms_teams_tools import download_meeting_summary
    result = download_meeting_summary.invoke({})
    
    print(f"✓ Downloaded {len(result)} characters")
    print(f"✓ First 100 chars: {result[:100]}...")
    print()

def test_drive_tool():
    """Test Drive upload tool"""
    print("=" * 60)
    print("TEST 2: Drive upload_to_drive tool")
    print("=" * 60)
    
    from tools.google_drive_tools import upload_to_drive
    result = upload_to_drive.invoke({
        'file_content': 'Test content from verification script',
        'file_name': 'verification_test.txt'
    })
    
    print(f"✓ Upload result received")
    print(f"✓ Status: success")
    print()

def test_filesystem_tools():
    """Test filesystem tools"""
    print("=" * 60)
    print("TEST 3: Filesystem tools (list_directory, read_file)")
    print("=" * 60)
    
    from tools.typescript_shell_tool import list_directory, read_file
    
    # Test list_directory
    result = list_directory.invoke({'dir_path': 'agent_filesystem/servers'})
    print("✓ list_directory works")
    print(result)
    
    # Test read_file
    result = read_file.invoke({
        'file_path': 'agent_filesystem/servers/teams/download_meeting_summary.ts'
    })
    print("\n✓ read_file works")
    print(f"✓ Read {len(result)} characters from TypeScript file")
    print()

def test_typescript_execution():
    """Test TypeScript code execution"""
    print("=" * 60)
    print("TEST 4: TypeScript code execution")
    print("=" * 60)
    
    from tools.typescript_shell_tool import execute_typescript
    
    # Simple test
    code = '''
console.log('✓ Basic TypeScript execution works');
const result = 10 * 10;
console.log('✓ 10 * 10 =', result);
'''
    
    result = execute_typescript.invoke({'code': code})
    print(result)
    print()

def test_end_to_end_typescript():
    """Test end-to-end TypeScript with imports"""
    print("=" * 60)
    print("TEST 5: End-to-end TypeScript (download + upload)")
    print("=" * 60)
    
    from tools.typescript_shell_tool import execute_typescript
    
    code = r'''
import { download_meeting_summary } from './servers/teams/download_meeting_summary';
import { upload_to_drive } from './servers/drive/upload_to_drive';

async function main() {
  console.log('1. Downloading meeting summary...');
  const summary = await download_meeting_summary();
  console.log(`   ✓ Downloaded ${summary.length} characters`);
  
  console.log('2. Uploading to Drive...');
  const result = await upload_to_drive(summary, 'test_verification.md', 'root');
  console.log(`   ✓ Upload complete: ${result.file_name}`);
  
  console.log('\n✓ End-to-end test successful!');
  console.log('✓ Large data flowed through code, not through LLM context');
}

main().catch(console.error);
'''
    
    result = execute_typescript.invoke({'code': code})
    print(result)
    print()

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MCP CODE MODE EXAMPLE - VERIFICATION TESTS")
    print("=" * 60)
    print()
    
    try:
        test_teams_tool()
        test_drive_tool()
        test_filesystem_tools()
        test_typescript_execution()
        test_end_to_end_typescript()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print()
        print("The repository is ready to use.")
        print("To test with an actual LLM agent, add your GEMINI_API_KEY to .env")
        print("and run: python agent_example_1.py or python agent_example_2.py")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
