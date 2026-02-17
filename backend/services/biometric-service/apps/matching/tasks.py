from celery import shared_task
import time
import random

@shared_task
def match_face(citizen_id, image_path):
    """
    Simulates matching a captured face against the stored biometric template.
    In a real system, this would:
    1. Load the stored template for citizen_id.
    2. Generate an embedding for image_path.
    3. Calculate cosine similarity.
    """
    # Simulate processing delay (GPU inference)
    time.sleep(2)
    
    # Simulate match score (0.0 to 1.0)
    # For demo purposes, 90% chance of success if ID is valid-ish
    match_score = random.uniform(0.7, 0.99) 
    
    # Threshold usually 0.75
    is_match = match_score > 0.75
    
    return {
        'citizen_id': citizen_id,
        'match_score': match_score,
        'is_match': is_match,
        'status': 'COMPLETED'
    }

@shared_task
def verify_liveness(session_id, video_path):
    """
    Simulates liveness detection to prevent deepfake fraud.
    Checks for:
    - Texture analysis (skin reflection)
    - Micro-expressions
    - Depth estimation
    """
    # Simulate heavy processing
    time.sleep(3)
    
    # Simulate Fraud Prevention Checks
    # 5% chance of detecting a deepfake/spoof
    is_spoof = random.random() < 0.05
    
    return {
        'session_id': session_id,
        'is_live': not is_spoof,
        'liveness_score': random.uniform(0.8, 1.0) if not is_spoof else random.uniform(0.0, 0.4),
        'fraud_detected': is_spoof,
        'status': 'COMPLETED'
    }
