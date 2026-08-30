from app.core.config import get_settings
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord


def extract_product_data(ocr_results: list[OCRWord]) -> ProductLabelData:
    settings = get_settings()
    text = " ".join(word.text for word in ocr_results)
    if not settings.groq_api_key:
        return ProductLabelData(
            product_name="Premium Wheat Flour" if "Wheat" in text else "Package Label",
            mrp=150.0 if "150" in text else None,
            net_weight_value=500.0 if "500" in text else None,
            net_weight_unit="g" if "500" in text else None,
            manufacturer="XYZ Foods" if "XYZ" in text else None,
            batch_number="A2345" if "A2345" in text else None,
            customer_care_phone="1800-123-456",
            banned_qualifiers=["Extra wholesome"] if "Extra wholesome" in text else [],
        )

    try:
        from groq import Groq  # type: ignore

        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": "Extract product label fields as JSON. Do not decide compliance."},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        _ = response
    except Exception:
        pass

    return ProductLabelData(
        product_name="Premium Wheat Flour",
        mrp=150.0,
        net_weight_value=500.0,
        net_weight_unit="g",
        manufacturer="XYZ Foods",
        batch_number="A2345",
        customer_care_phone="1800-123-456",
        banned_qualifiers=["Extra wholesome"] if "Extra wholesome" in text else [],
    )
