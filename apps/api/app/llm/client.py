import re
from app.core.config import get_settings
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord


def _extract_mrp(text: str) -> float | None:
    patterns = [
        r"(?:mrp|rs\.?|inr|₹)\s*:?\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d{1,2})?)\s*(?:\/-)?",
        r"(\d+(?:\.\d{1,2})?)\s*(?:\/-)?\s*(?:rs\.?|inr|₹)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                val = float(m.group(1))
                if 0 < val < 100000:
                    return val
            except ValueError:
                pass
    return None


def _extract_net_weight(text: str) -> tuple[float | None, str | None]:
    pattern = r"(?:net\s*(?:wt\.?|weight|qty\.?|quantity)?)\s*:?\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        try:
            val = float(m.group(1))
            unit = m.group(2).lower()
            return val, unit
        except ValueError:
            pass

    gen_pattern = r"\b(\d+(?:\.\d+)?)\s*(g|kg|ml|l|gm|pcs|pc|pieces)\b"
    m2 = re.search(gen_pattern, text, re.IGNORECASE)
    if m2:
        try:
            val = float(m2.group(1))
            unit = m2.group(2).lower()
            if unit == "gm":
                unit = "g"
            return val, unit
        except ValueError:
            pass

    return None, None


def _extract_batch_number(text: str) -> str | None:
    pattern = r"(?:batch|lot|b\.?\s*no|lot\.?\s*no|b\/n|fssai\s*lic\.?\s*no\.?)\s*:?\s*([A-Za-z0-9\/-]+)"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


def _extract_mfd_date(text: str) -> str | None:
    pattern = r"(?:mfg|mfd|pkd|packed|date of mfg)\s*\.?\s*:?\s*(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}|\d{2}[\/\.-]\d{2}[\/\.-]\d{2,4}|\d{2}[\/\.-]\d{4})"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


def _extract_expiry_date(text: str) -> str | None:
    pattern = r"(?:exp|expiry|best\s*before|use\s*by)\s*:?\s*(\d+\s*(?:days?|months?|years?|hrs?|hours?)|\d{2}[\/\.-]\d{2}[\/\.-]\d{2,4}|\d{2}[\/\.-]\d{4})"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


def _extract_customer_care(text: str) -> str | None:
    phone_pattern = r"(?:customer\s*care|help|mob|mobile|phone|tel|ph|contact)\s*\.?\s*:?\s*([\d\s,-]{8,25})"
    m = re.search(phone_pattern, text, re.IGNORECASE)
    if m:
        raw = m.group(1).strip()
        nums = re.findall(r"\b\d{8,12}\b", raw)
        if nums:
            return ", ".join(nums[:2])
        return raw
    m2 = re.search(r"\b\d{10}\b", text)
    if m2:
        return m2.group(0)
    return None


def _extract_manufacturer(text_lines: list[str]) -> str | None:
    for line in text_lines:
        if re.search(r"(?:mfg|manufactured|marketed|packed)\s*by", line, re.IGNORECASE):
            clean = re.sub(r"^(?:mfg|manufactured|marketed|packed)\s*by\s*:?", "", line, flags=re.IGNORECASE).strip()
            if clean:
                return clean
        if re.search(r"\b(?:bakers|bakery|foods|industries|ltd|pvt|corp|enterprises|mill|flour)\b", line, re.IGNORECASE):
            return line.strip()
    return text_lines[0].strip() if text_lines else None


def _extract_product_name(text_lines: list[str]) -> str | None:
    for line in text_lines:
        clean = line.strip()
        if re.search(r"\b(?:buns|burger|bread|flour|biscuit|cookies|butter|paneer|curd|oil|atta|rice|sugar|tea|coffee|juice)\b", clean, re.IGNORECASE):
            return clean
    for line in text_lines:
        clean = line.strip()
        if not re.search(r"(?:mrp|batch|mfg|exp|net|weight|customer|care|rs\.|inr|₹|b\.no|pkd|fssai|mob)", clean, re.IGNORECASE):
            if 3 < len(clean) < 40:
                return clean
    return text_lines[0].strip() if text_lines else "Product Label"



def _extract_banned_qualifiers(text: str) -> list[str]:
    banned_keywords = ["100% pure", "medicinal", "health cure", "miracle", "extra wholesome", "100% natural"]
    found = []
    for kw in banned_keywords:
        if kw in text.lower():
            found.append(kw.title())
    return found


def extract_product_data(ocr_results: list[OCRWord]) -> ProductLabelData:
    settings = get_settings()
    text_lines = [word.text for word in ocr_results]
    full_text = " ".join(text_lines)

    if settings.groq_api_key:
        try:
            import json
            from groq import Groq  # type: ignore

            client = Groq(api_key=settings.groq_api_key)
            prompt = (
                "Extract structured fields from product label text as JSON.\n"
                "JSON format:\n"
                "{\n"
                '  "product_name": string or null,\n'
                '  "mrp": float or null,\n'
                '  "net_weight_value": float or null,\n'
                '  "net_weight_unit": string or null,\n'
                '  "manufacturer": string or null,\n'
                '  "batch_number": string or null,\n'
                '  "manufacturing_date": string or null,\n'
                '  "expiry_date": string or null,\n'
                '  "customer_care_phone": string or null,\n'
                '  "banned_qualifiers": array of strings\n'
                "}\n\n"
                f"OCR Text:\n{full_text}"
            )
            response = client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "system", "content": "You are a JSON extractor for package compliance labels."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            parsed = json.loads(content)

            net_val, net_unit = _extract_net_weight(full_text)
            return ProductLabelData(
                product_name=parsed.get("product_name") or _extract_product_name(text_lines),
                mrp=parsed.get("mrp") if parsed.get("mrp") is not None else _extract_mrp(full_text),
                net_weight_value=parsed.get("net_weight_value") if parsed.get("net_weight_value") is not None else net_val,
                net_weight_unit=parsed.get("net_weight_unit") or net_unit,
                manufacturer=parsed.get("manufacturer") or _extract_manufacturer(text_lines),
                batch_number=parsed.get("batch_number") or _extract_batch_number(full_text),
                manufacturing_date=parsed.get("manufacturing_date") or _extract_mfd_date(full_text),
                expiry_date=parsed.get("expiry_date") or _extract_expiry_date(full_text),
                customer_care_phone=parsed.get("customer_care_phone") or _extract_customer_care(full_text),
                banned_qualifiers=parsed.get("banned_qualifiers") or _extract_banned_qualifiers(full_text),
            )
        except Exception:
            pass

    net_val, net_unit = _extract_net_weight(full_text)
    return ProductLabelData(
        product_name=_extract_product_name(text_lines),
        mrp=_extract_mrp(full_text),
        net_weight_value=net_val,
        net_weight_unit=net_unit,
        manufacturer=_extract_manufacturer(text_lines),
        batch_number=_extract_batch_number(full_text),
        manufacturing_date=_extract_mfd_date(full_text),
        expiry_date=_extract_expiry_date(full_text),
        customer_care_phone=_extract_customer_care(full_text),
        banned_qualifiers=_extract_banned_qualifiers(full_text),
    )

