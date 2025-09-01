"""
Z-WAIF Modern Vision Implementation

This module provides the working vision solution using Mistral-Small-3.2-24B-Instruct-2506 
with oobabooga text-generation-webui and the correct OpenAI-compatible multimodal API format.

Requirements:
- Vision-capable model (Mistral-Small-3.2-24B-Instruct-2506 or Skyfall-31B-v4j-Q8_0.gguf)
- mmproj file loaded in oobabooga
- OpenAI-compatible /v1/chat/completions endpoint

Critical Success Factors:
- "mode": "chat" parameter is ESSENTIAL for oobabooga vision processing
- Standard OpenAI multimodal format (no custom oobabooga image embedding)
- Base64 encoding with data URL format
"""

import requests
import base64
import os
import html
from dotenv import load_dotenv

load_dotenv()


def view_image_modern_working(direct_talk_transcript="", image_path="LiveImage.png"):
    """
    Working modern vision implementation for Z-WAIF
    Uses the correct oobabooga parameters for native vision models with mmproj
    
    Args:
        direct_talk_transcript: User's voice input while taking image
        image_path: Path to image file (defaults to LiveImage.png)
    
    Returns:
        String description of the image from the AI model
    """
    host_port = os.environ.get("HOST_PORT", "192.168.0.69:5000")
    api_url = f"http://{host_port}/v1/chat/completions"
    your_name = os.environ.get("YOUR_NAME", "User")
    
    if not os.path.exists(image_path):
        return "Error: No image found to process"
    
    try:
        # Encode image to base64
        with open(image_path, 'rb') as f:
            img_str = base64.b64encode(f.read()).decode('utf-8')
        
        # Prepare the prompt
        if direct_talk_transcript and len(direct_talk_transcript.strip()) > 0:
            base_prompt = direct_talk_transcript
        else:
            base_prompt = f"{your_name}, please view and describe this image in detail:"
        
        # CRITICAL: The working format with oobabooga-specific parameters
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": base_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
                    ]
                }
            ],
            "max_tokens": 500,
            "temperature": 0.6,
            "mode": "chat",              # ← ESSENTIAL for oobabooga vision
            "truncation_length": 2048,
            "stop": []
        }
        
        response = requests.post(api_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return html.unescape(content)
        else:
            return f"Error: API request failed with status {response.status_code}"
            
    except Exception as e:
        return f"Error processing image: {str(e)}"


def view_image_modern_streaming(direct_talk_transcript="", image_path="LiveImage.png"):
    """
    Streaming version of the modern vision implementation
    
    For now, this uses the same function as the standard version.
    Can be extended later to support true streaming responses if needed.
    
    Args:
        direct_talk_transcript: User's voice input while taking image
        image_path: Path to image file (defaults to LiveImage.png)
    
    Returns:
        String description of the image from the AI model
    """
    # TODO: Implement true streaming support if needed
    # For now, use same function - maintains compatibility
    return view_image_modern_working(direct_talk_transcript, image_path)


def view_image_modern_with_context(direct_talk_transcript="", image_path="LiveImage.png", 
                                 history_context=None, use_character_card=True):
    """
    Enhanced version with conversation history context
    
    This version can include conversation history for better contextual responses,
    similar to how the original Z-WAIF vision system worked.
    
    Args:
        direct_talk_transcript: User's voice input while taking image
        image_path: Path to image file (defaults to LiveImage.png)
        history_context: List of recent message pairs for context
        use_character_card: Whether to include character card in system message
    
    Returns:
        String description of the image from the AI model
    """
    host_port = os.environ.get("HOST_PORT", "192.168.0.69:5000")
    api_url = f"http://{host_port}/v1/chat/completions"
    your_name = os.environ.get("YOUR_NAME", "User")
    
    if not os.path.exists(image_path):
        return "Error: No image found to process"
    
    try:
        # Encode image to base64
        with open(image_path, 'rb') as f:
            img_str = base64.b64encode(f.read()).decode('utf-8')
        
        # Build messages array with optional context
        messages = []
        
        # Add character card if requested
        if use_character_card:
            try:
                import API.character_card
                system_content = API.character_card.visual_character_card
                if system_content and system_content.strip():
                    messages.append({"role": "system", "content": system_content})
            except (ImportError, AttributeError):
                # Fallback if character card module not available
                pass
        
        # Add recent conversation history for context
        if history_context and len(history_context) > 0:
            # Add last few exchanges for context (limit to avoid token overflow)
            recent_history = history_context[-2:]  # Last 2 exchanges
            for exchange in recent_history:
                if len(exchange) >= 2:
                    messages.append({"role": "user", "content": exchange[0]})
                    messages.append({"role": "assistant", "content": exchange[1]})
        
        # Prepare the prompt
        if direct_talk_transcript and len(direct_talk_transcript.strip()) > 0:
            base_prompt = direct_talk_transcript
        else:
            base_prompt = f"{your_name}, please view and describe this image in detail:"
        
        # Add the image message
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": base_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
            ]
        })
        
        # CRITICAL: The working format with oobabooga-specific parameters
        payload = {
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.6,
            "mode": "chat",              # ← ESSENTIAL for oobabooga vision
            "truncation_length": 2048,
            "stop": []
        }
        
        response = requests.post(api_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return html.unescape(content)
        else:
            return f"Error: API request failed with status {response.status_code}"
            
    except Exception as e:
        return f"Error processing image: {str(e)}"


# Legacy compatibility functions for easier migration
def view_image_legacy_compatible(direct_talk_transcript=""):
    """
    Drop-in replacement for the original view_image function in api_controller.py
    Maintains exact same interface while using modern implementation
    """
    return view_image_modern_working(direct_talk_transcript, "LiveImage.png")


def view_image_streaming_legacy_compatible(direct_talk_transcript=""):
    """
    Drop-in replacement for the original view_image_streaming function in api_controller.py
    Maintains exact same interface while using modern implementation
    """
    return view_image_modern_streaming(direct_talk_transcript, "LiveImage.png")
