import json
import logging
from app.core.config import get_settings
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord


def extract_product_data(ocr_results: list[OCRWord]) -> ProductLabelData:
    settings = get_settings()
    
    # Combine OCR words into a structured text representation (or just a space-separated string)
    text = " ".join(word.text for word in ocr_results)
    
    if not settings.groq_api_key or not text.strip():
        logging.warning("Groq API key not set or no OCR text found. Returning empty/mock data.")
        return ProductLabelData(product_name="Unknown Product")

    try:
        from groq import Groq  # type: ignore

        client = Groq(api_key=settings.groq_api_key)
        
        system_prompt = """
You are a regulatory compliance AI. Extract the following fields from the product label OCR text.
Return ONLY a valid JSON object matching this schema exactly:
{
  "product_name": "string (the name of the product)",
  "mrp": float (the Maximum Retail Price, just the number),
  "net_weight_value": float (just the number),
  "net_weight_unit": "string (e.g. g, kg, ml, L)",
  "manufacturer": "string (company name and address if present)",
  "batch_number": "string (batch or lot number)",
  "customer_care_phone": "string",
  "banned_qualifiers": ["string"] (Any misleading terms like 'Extra', 'Premium', 'Wholesome', 'Pure' modifying basic names if present)
}
If a field is not found in the text, use null (or empty list for banned_qualifiers).
"""

        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"OCR Text:\n{text}"},
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        result_content = response.choices[0].message.content
        if result_content:
            data = json.loads(result_content)
            return ProductLabelData(**data)
            
    except Exception as e:
        logging.error(f"LLM extraction failed: {e}")
        
    # Fallback if API fails
    return ProductLabelData(product_name="Extraction Failed")

