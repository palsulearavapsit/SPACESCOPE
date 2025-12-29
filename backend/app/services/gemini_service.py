import google.generativeai as genai
import base64
from io import BytesIO
from typing import Optional, Dict, List, Any
from app.core.config import get_settings
import json

settings = get_settings()


class GeminiAIService:
    """Gemini 2.5 Flash AI service for SpaceScope."""
    
    def __init__(self):
        genai.configure(api_key=getattr(settings, "GEMINI_API_KEY", ""))
        model_name = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
        self.model = genai.GenerativeModel(model_name)
    
    # ============ 1. CONVERSATIONAL CHAT ============
    async def conversational_chat(
        self,
        user_message: str,
        context_type: Optional[str] = None,
        context_data: Optional[Dict[str, Any]] = None
    ) -> tuple[str, int]:
        """
        Conversational chat about space events, missions, and data.
        
        Args:
            user_message: User's question
            context_type: Type of context ("events", "weather", "missions", "learning")
            context_data: Additional context (sky events, weather alerts, etc.)
        
        Returns:
            (ai_response, tokens_used)
        """
        try:
            # Build context prompt
            context_prompt = self._build_context_prompt(context_type, context_data)
            
            full_prompt = f"""You are SpaceScope's expert space assistant. 
You provide accurate, engaging explanations about space, astronomy, missions, and space weather.
Keep responses concise but informative. Use analogies when helpful.

{context_prompt}

User Question: {user_message}

Provide a helpful, accurate response:"""
            
            response = self.model.generate_content(full_prompt)
            
            # Extract text safely
            text = ""
            if hasattr(response, "text") and response.text:
                text = response.text
            elif hasattr(response, "candidates") and response.candidates:
                try:
                    text = response.candidates[0].content.parts[0].text
                except (IndexError, AttributeError):
                    text = ""
            
            # Extract token count safely
            tokens = 0
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                tokens = getattr(response.usage_metadata, "total_token_count", 0) or getattr(response.usage_metadata, "total_tokens", 0)
            
            return text, tokens
        
        except Exception as e:
            return f"I encountered an error: {str(e)}", 0
    
    # ============ 2. VISION INTELLIGENCE ============
    async def analyze_satellite_image(
        self,
        image_data: bytes,
        image_format: str = "jpeg",
        analysis_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze satellite/telescope images for auroras, storms, launches, anomalies.
        
        Args:
            image_data: Image bytes
            image_format: Image format (jpeg, png, webp)
            analysis_type: Type of analysis to perform
        
        Returns:
            Analysis results with detections and insights
        """
        try:
            # Convert to base64
            image_b64 = base64.standard_b64encode(image_data).decode('utf-8')
            mime_type = f"image/{image_format}"
            
            analysis_prompts = {
                "aurora": "Detect and describe any auroras. Identify colors, intensity, location patterns.",
                "storm": "Identify storm systems, cloud formations, and weather patterns. Estimate severity.",
                "launch": "Detect spacecraft launches, plumes, or orbital events. Identify spacecraft type if possible.",
                "anomaly": "Identify any unusual phenomena, anomalies, or notable features.",
                "general": "Analyze this space/satellite image and provide insights about what you see."
            }
            
            prompt = f"""Analyze this satellite/space image as an expert astronomer and space scientist.
{analysis_prompts.get(analysis_type, analysis_prompts['general'])}

Provide structured analysis with:
1. Main detections/features
2. Scientific significance
3. Any anomalies
4. Predicted impact/implications"""
            
            response = self.model.generate_content([
                prompt,
                {
                    "mime_type": mime_type,
                    "data": image_b64
                }
            ])
            
            # Extract text safely
            text = ""
            if hasattr(response, "text") and response.text:
                text = response.text
            elif hasattr(response, "candidates") and response.candidates:
                try:
                    text = response.candidates[0].content.parts[0].text
                except (IndexError, AttributeError):
                    text = ""
            
            # Extract token count safely
            tokens = 0
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                tokens = getattr(response.usage_metadata, "total_token_count", 0) or getattr(response.usage_metadata, "total_tokens", 0)
            
            return {
                "analysis": text,
                "image_format": image_format,
                "analysis_type": analysis_type,
                "tokens_used": tokens
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "analysis": None
            }
    
    # ============ 3. TEXT GENERATION & SUMMARIZATION ============
    async def generate_alert_message(
        self,
        alert_type: str,
        event_data: Dict[str, Any]
    ) -> str:
        """
        Generate alert messages for space weather or events.
        
        Args:
            alert_type: Type of alert (solar_flare, geomagnetic_storm, etc.)
            event_data: Event data with details
        
        Returns:
            Formatted alert message
        """
        try:
            prompt = f"""Generate a clear, impactful alert message for space enthusiasts about a {alert_type}.
            
Event Data: {json.dumps(event_data, indent=2)}

Create a message that:
- Explains what's happening in simple terms
- States the impact (e.g., visible auroras, communication disruption)
- Suggests what users should do/watch for
- Is 2-3 sentences, urgent and informative"""
            
            response = self.model.generate_content(prompt)
            
            # Extract text safely
            if hasattr(response, "text") and response.text:
                return response.text
            elif hasattr(response, "candidates") and response.candidates:
                try:
                    return response.candidates[0].content.parts[0].text
                except (IndexError, AttributeError):
                    return f"Alert: {alert_type} detected"
            return f"Alert: {alert_type} detected"
        
        except Exception as e:
            return f"Alert: {alert_type} detected"
    
    async def summarize_learning_content(
        self,
        raw_content: str,
        target_audience: str = "students"
    ) -> str:
        """
        Convert raw data into readable explanations.
        
        Args:
            raw_content: Technical or raw data content
            target_audience: Audience type (students, educators, general_public)
        
        Returns:
            Summarized, student-friendly content
        """
        try:
            audience_guides = {
                "students": "Explain for high school students. Use analogies and relatable examples.",
                "educators": "Provide detailed explanation suitable for classroom teaching.",
                "general_public": "Explain for general public with no scientific background."
            }
            
            prompt = f"""{audience_guides.get(target_audience, audience_guides['students'])}

Content to explain:
{raw_content}

Create engaging, educational content that:
1. Breaks down complex concepts
2. Uses relevant examples
3. Explains the significance
4. Suggests related topics to explore"""
            
            response = self.model.generate_content(prompt)
            
            # Extract text safely
            if hasattr(response, "text") and response.text:
                return response.text
            elif hasattr(response, "candidates") and response.candidates:
                try:
                    return response.candidates[0].content.parts[0].text
                except (IndexError, AttributeError):
                    return ""
            return ""
        
        except Exception as e:
            return f"Error summarizing content: {str(e)}"
    
    # ============ 4. PREDICTIVE ANALYTICS ============
    async def predict_solar_activity(
        self,
        historical_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Forecast solar storms and geomagnetic activity.
        
        Args:
            historical_data: Historical solar/geomagnetic indices
        
        Returns:
            Prediction with probability and confidence
        """
        try:
            prompt = f"""You are an expert space weather analyst with access to solar activity data.
            
Historical Data: {json.dumps(historical_data, indent=2)}

Analyze this data and predict:
1. Probability of solar flare in next 24-48 hours (0.0-1.0)
2. Confidence level of prediction (0.0-1.0)
3. Expected severity if event occurs
4. Geomagnetic storm probability
5. Aurora visibility likelihood

Respond in JSON format:
{{
  "solar_flare_probability": <float>,
  "confidence_score": <float>,
  "expected_severity": "<low|moderate|high|extreme>",
  "geomagnetic_storm_probability": <float>,
  "aurora_visibility_probability": <float>,
  "reasoning": "<explanation>"
}}"""
            
            response = self.model.generate_content(prompt)
            
            # Extract text safely
            text = ""
            if hasattr(response, "text") and response.text:
                text = response.text
            elif hasattr(response, "candidates") and response.candidates:
                try:
                    text = response.candidates[0].content.parts[0].text
                except (IndexError, AttributeError):
                    text = ""
            
            # Parse JSON response
            try:
                result = json.loads(text)
            except:
                result = {
                    "solar_flare_probability": 0.3,
                    "confidence_score": 0.7,
                    "expected_severity": "moderate",
                    "geomagnetic_storm_probability": 0.4,
                    "aurora_visibility_probability": 0.5,
                    "reasoning": text
                }
            
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "solar_flare_probability": 0.0,
                "confidence_score": 0.0
            }
    
    async def predict_iss_visibility(
        self,
        location_data: Dict[str, Any],
        forecast_days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Predict ISS passes for visibility.
        
        Args:
            location_data: User location (latitude, longitude)
            forecast_days: Days to forecast ahead
        
        Returns:
            List of predicted ISS passes with visibility details
        """
        try:
            prompt = f"""Based on ISS orbital mechanics and given location data:
Location: {json.dumps(location_data)}
Forecast period: {forecast_days} days

Generate realistic ISS pass predictions with:
1. Pass date/time
2. Rise azimuth and culmination altitude
3. Visibility duration
4. Brightness magnitude
5. Observation difficulty (easy/moderate/challenging)

Return as JSON list of passes."""
            
            response = self.model.generate_content(prompt)
            
            # Extract text safely
            text = ""
            if hasattr(response, "text") and response.text:
                text = response.text
            elif hasattr(response, "candidates") and response.candidates:
                try:
                    text = response.candidates[0].content.parts[0].text
                except (IndexError, AttributeError):
                    text = ""
            
            try:
                passes = json.loads(text)
            except:
                passes = []
            
            return passes
        
        except Exception as e:
            return []
    
    # ============ HELPER METHODS ============
    def _build_context_prompt(
        self,
        context_type: Optional[str],
        context_data: Optional[Dict[str, Any]]
    ) -> str:
        """Build context prompt based on conversation context."""
        
        if not context_type or not context_data:
            return ""
        
        context_prompts = {
            "events": f"Relevant sky events: {json.dumps(context_data)}",
            "weather": f"Space weather alerts: {json.dumps(context_data)}",
            "missions": f"Mission data: {json.dumps(context_data)}",
            "learning": f"Learning context: {json.dumps(context_data)}"
        }
        
        return context_prompts.get(context_type, "")
