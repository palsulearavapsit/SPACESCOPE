from celery import shared_task
from datetime import datetime
from app.services.gemini_service import GeminiAIService


@shared_task(bind=True)
def run_gemini_inference(self, inference_type: str, input_data: dict):
    """
    Run Gemini AI inference tasks.
    
    Inference types:
    - predict_solar_storm
    - predict_aurora
    - analyze_image
    - generate_summary
    """
    try:
        ai_service = GeminiAIService()
        
        # Route to appropriate inference method
        if inference_type == "predict_solar_storm":
            # Historical data should be in input_data
            result = ai_service.predict_solar_activity(input_data)
        
        elif inference_type == "analyze_image":
            # image_data and analysis_type in input_data
            result = ai_service.analyze_satellite_image(
                image_data=input_data.get("image_data"),
                analysis_type=input_data.get("analysis_type", "general")
            )
        
        elif inference_type == "generate_summary":
            result = ai_service.summarize_learning_content(
                raw_content=input_data.get("content", ""),
                target_audience=input_data.get("audience", "students")
            )
        
        else:
            return {
                "status": "error",
                "error": f"Unknown inference type: {inference_type}"
            }
        
        return {
            "status": "success",
            "inference_type": inference_type,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as exc:
        print(f"Error running inference: {exc}")
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
