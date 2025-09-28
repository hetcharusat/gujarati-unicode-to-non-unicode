import requests
from pathlib import Path
import os
import time
import random
import json
import argparse
from datetime import datetime
from font_mapping import GUJARATI_FONTS, get_font_list, get_font_info

# Chunk size limit (API max = 200 chars)
CHUNK_SIZE = 200

# Rate limiting settings
MIN_DELAY = 2  # Minimum seconds between requests
MAX_DELAY = 5  # Maximum seconds between requests
MAX_RETRIES = 3  # Maximum retry attempts per chunk

def chunk_text(text, size=CHUNK_SIZE):
    """Split text into fixed-size chunks (≤200 chars)."""
    return [text[i:i+size] for i in range(0, len(text), size)]

def convert_chunk_with_session(session, chunk, api_url, attempt=1):
    """Send one chunk to the API using session with retry logic."""
    for retry in range(MAX_RETRIES):
        try:
            # Add random delay to avoid rate limiting
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            if retry > 0:
                # Exponential backoff for retries
                delay = delay * (2 ** retry)
                print(f"  Retry {retry + 1}/{MAX_RETRIES} after {delay:.1f}s delay...")
            
            time.sleep(delay)
            
            # Rotate user agents to appear as different browsers
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
            ]
            
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            
            # Ensure proper encoding for the request
            data = {"modify_string": chunk}
            
            resp = session.post(api_url, data=data, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                # Debug: Check response content type and encoding
                print(f"  Response encoding: {resp.encoding}")
                print(f"  Content type: {resp.headers.get('content-type', 'unknown')}")
                
                # Try to decode properly
                try:
                    # First try with response encoding
                    if resp.encoding:
                        resp.encoding = 'utf-8'  # Force UTF-8 encoding
                    
                    converted_text = resp.text
                    
                    # Validate that we got actual text (not binary)
                    if len(converted_text.strip()) == 0:
                        print(f"  ⚠️ Empty response received")
                        converted_text = chunk  # Fallback to original
                    elif any(ord(char) < 32 and char not in '\n\r\t' for char in converted_text[:100]):
                        print(f"  ⚠️ Response contains binary/control characters")
                        # Try different encoding approaches
                        try:
                            converted_text = resp.content.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                converted_text = resp.content.decode('latin1')
                            except UnicodeDecodeError:
                                print(f"  ❌ Could not decode response, using original text")
                                converted_text = chunk  # Fallback to original
                    
                    print(f"  ✅ Converted text sample: {converted_text[:50]}...")
                    return converted_text
                    
                except Exception as decode_error:
                    print(f"  ❌ Decoding error: {decode_error}")
                    return chunk  # Fallback to original chunk
                    
            elif resp.status_code == 429:  # Too Many Requests
                print(f"  Rate limited (429), attempt {retry + 1}/{MAX_RETRIES}")
                if retry == MAX_RETRIES - 1:
                    raise RuntimeError(f"Rate limited after {MAX_RETRIES} attempts")
                continue
            elif resp.status_code == 403:  # Forbidden (IP ban)
                print(f"  IP banned (403), attempt {retry + 1}/{MAX_RETRIES}")
                if retry == MAX_RETRIES - 1:
                    raise RuntimeError(f"IP banned after {MAX_RETRIES} attempts. Try using VPN or wait.")
                continue
            else:
                print(f"  API error {resp.status_code}: {resp.text}")
                if retry == MAX_RETRIES - 1:
                    raise RuntimeError(f"API error {resp.status_code}: {resp.text}")
                continue
                
        except requests.exceptions.RequestException as e:
            print(f"  Network error on attempt {retry + 1}/{MAX_RETRIES}: {e}")
            if retry == MAX_RETRIES - 1:
                raise RuntimeError(f"Network error after {MAX_RETRIES} attempts: {e}")
            continue
    
    raise RuntimeError(f"Failed to convert chunk after {MAX_RETRIES} attempts")

def get_next_output_filename(font_name):
    """Generate next available output filename with font name"""
    counter = 1
    while True:
        filename = f"converted_{font_name.lower().replace(' ', '_')}_{counter}.txt"
        if not Path(filename).exists():
            return filename
        counter += 1

def save_progress(filename, completed_chunks, total_chunks, results):
    """Save conversion progress to resume later if interrupted"""
    progress_file = f"{filename}.progress.json"
    progress_data = {
        "completed_chunks": completed_chunks,
        "total_chunks": total_chunks,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)
    print(f"Progress saved: {completed_chunks}/{total_chunks} chunks completed")

def load_progress(filename):
    """Load previous progress if exists"""
    progress_file = f"{filename}.progress.json"
    if Path(progress_file).exists():
        with open(progress_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def cleanup_progress(filename):
    """Remove progress file after successful completion"""
    progress_file = f"{filename}.progress.json"
    if Path(progress_file).exists():
        Path(progress_file).unlink()
        print(f"Progress file cleaned up: {progress_file}")

def convert_file(input_file, output_file, font_key):
    """Read input file, convert via API in chunks, save output file."""
    try:
        text = Path(input_file).read_text(encoding="utf-8")
        
        if not text.strip():
            print("Input file is empty!")
            return
        
        font_info = get_font_info(font_key)
        api_url = font_info['url']
        
        chunks = chunk_text(text)
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        print(f"Selected font: {font_info['name']} ({font_key})")
        print(f"Font family: {font_info['font_family']}")
        print(f"API URL: {api_url}")
        print(f"Text length: {len(text)} characters")
        print(f"Total chunks: {len(chunks)}")
        print(f"First chunk preview: {chunks[0][:50]}...")

        # Check for existing progress
        progress = load_progress(output_file)
        if progress:
            print(f"\n🔄 Resuming from previous progress:")
            print(f"   Completed: {progress['completed_chunks']}/{progress['total_chunks']} chunks")
            print(f"   Timestamp: {progress['timestamp']}")
            
            results = progress['results']
            start_chunk = progress['completed_chunks']
            
            user_input = input("Resume from where you left off? (y/n): ").lower().strip()
            if user_input != 'y':
                print("Starting fresh conversion...")
                results = []
                start_chunk = 0
        else:
            results = []
            start_chunk = 0

        # Use session for better connection management
        with requests.Session() as session:
            for i in range(start_chunk, len(chunks)):
                chunk = chunks[i]
                chunk_num = i + 1
                print(f"\n🔄 Converting chunk {chunk_num}/{len(chunks)} ({len(chunk)} chars)...")
                print(f"  Sending: {chunk[:30]}...")
                
                try:
                    converted = convert_chunk_with_session(session, chunk, api_url)
                    results.append(converted)
                    print(f"  ✅ Received: {converted[:30] if converted else 'EMPTY'}...")
                    
                    # Save progress every 5 chunks
                    if chunk_num % 5 == 0:
                        save_progress(output_file, chunk_num, len(chunks), results)
                        
                except Exception as e:
                    print(f"  ❌ Failed to convert chunk {chunk_num}: {e}")
                    print(f"  💾 Progress saved. You can resume later.")
                    save_progress(output_file, i, len(chunks), results)
                    return

        final_text = "".join(results)
        print(f"\nFinal converted text length: {len(final_text)} characters")
        
        if final_text.strip():
            print(f"Final text preview: {final_text[:100]}...")
            
            # Write to file
            Path(output_file).write_text(final_text, encoding="utf-8")
            
            # Verify file was created
            if Path(output_file).exists():
                file_size = Path(output_file).stat().st_size
                print(f"✅ File created successfully! Size: {file_size} bytes")
                print(f"✅ Output saved to: {output_file}")
                print(f"✅ Font used: {font_info['name']}")
                
                # Clean up progress file on success
                cleanup_progress(output_file)
            else:
                print("❌ File was not created!")
        else:
            print("❌ No converted text to save (empty result)")
        
    except FileNotFoundError:
        print(f"Input file '{input_file}' not found!")
        print("Please create the input file with your Gujarati Unicode text.")
    except Exception as e:
        print(f"Error: {e}")

def list_fonts():
    """List all available fonts"""
    print("\n📝 Available Gujarati Fonts:")
    print("=" * 50)
    
    for font_key, font_info in GUJARATI_FONTS.items():
        print(f"🔤 {font_info['name']} (key: {font_key})")
        print(f"   Font Family: {font_info['font_family']}")
        print(f"   API: {font_info['url']}")
        print()

def main():
    parser = argparse.ArgumentParser(description='Multi-Font Gujarati Unicode to Non-Unicode Converter')
    parser.add_argument('-i', '--input', default='txts/input.txt', 
                        help='Input file path (default: txts/input.txt)')
    parser.add_argument('-o', '--output', 
                        help='Output file path (auto-generated if not specified)')
    parser.add_argument('-f', '--font', default='shree0768', 
                        help='Font key to use for conversion (default: shree0768)')
    parser.add_argument('-l', '--list-fonts', action='store_true',
                        help='List all available fonts and exit')
    parser.add_argument('--min-delay', type=float, default=2.0,
                        help=f'Minimum delay between requests (default: 2.0)')
    parser.add_argument('--max-delay', type=float, default=5.0,
                        help=f'Maximum delay between requests (default: 5.0)')
    
    args = parser.parse_args()
    
    if args.list_fonts:
        list_fonts()
        return
    
    # Validate font
    if args.font not in GUJARATI_FONTS:
        print(f"❌ Unknown font key: {args.font}")
        print("Use --list-fonts to see available fonts")
        return
    
    # Update delay settings
    global MIN_DELAY, MAX_DELAY
    MIN_DELAY = args.min_delay
    MAX_DELAY = args.max_delay
    
    # Generate output filename if not specified
    if not args.output:
        font_info = get_font_info(args.font)
        args.output = f"txts/{get_next_output_filename(font_info['name'])}"
    
    print(f"🚀 Starting conversion...")
    print(f"   Input: {args.input}")
    print(f"   Output: {args.output}")
    print(f"   Font: {get_font_info(args.font)['name']}")
    print(f"   Delays: {MIN_DELAY}-{MAX_DELAY} seconds")
    
    convert_file(args.input, args.output, args.font)

if __name__ == "__main__":
    main()