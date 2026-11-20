"""High-precision multilingual concept checks for schema routing and SQL safety.

This is a deliberately conservative lexicon, not a claim to translate every
Indian-language sentence. Only positively identified concepts trigger guards.
"""

import re
from typing import Set

import sqlglot
from sqlglot import exp

from indicsql.schema.phonetic import normalize_indic_phonetics, transliterate_indic_to_latin

# Curated inflection stems. Native stems match within their own writing system.
# English/Hinglish terms use word boundaries to avoid incidental substring matches.
_CONCEPTS = {
    "farmer": (
        "farmer", "farmers", "kisan", "kisano", "kisaan", " రైతు", "రైతు",
        "விவசாயி", "விவசாயிகள", "किसान", "शेतकर", "कृषक",
        "কৃষক", "চাষি", "চাষী", "raitu", "raithu", "vivasaayi", "shetkari",
    ),
    "literacy": (
        "literate", "literacy", "illiterate", "sakshar", "saakshar",
        "సాక్షర", "అక్షరాస్య", "చదువుకున్న", "అక్షరాస్యత",
        "கல்வியறிவு", "எழுத்தறிவு", "படித்த", "साक्षर", "साक्षरता",
        "शिक्षित", "निरक्षर", "সাক্ষর", "সাক্ষরতা", "শিক্ষিত", "নিরক্ষর",
        "aksharasy", "aksharaasy", "ezhutharivu", "kalviyarivu",
    ),
    "beneficiaries": (
        "beneficiaries", "beneficiary", "labharthi", "labharthiyo",
        "లబ్ధిదార", "లబ్ధి", "பயனாள", "लाभार्थ", "लाभान्वित",
        "উপকারভোগ", "সুবিধাভোগ", "లాభार्थ",
    ),
    "female": (
        "female", "women", "woman", "girls", "महिला", "स्त्री",
        "মহিলা", "নারী", "பெண்", "மகளிர்", "మహిళ", "స్త్రీ",
    ),
    "male": (
        "male", "men", "man", "boys", "पुरुष", "पुरूष", "পুরুষ",
        "ஆண்", "పురుష", "మగ",
    ),
    "student": (
        "student", "students", "विद्यार्थ", "छात्र", "विद्यार्थी",
        "শিক্ষার্থী", "ছাত্র", "மாணவர", "மாணவி", "విద్యార్థ",
    ),
    "crop_production": (
        "crop production", "production of crops", "crop yield", "फसल उत्पादन",
        "पीक उत्पादन", "শস্য উৎপাদন", "ফসল উৎপাদন",
        "பயிர் உற்பத்தி", "పంట ఉత్పత్తి",
    ),
}


def extract_query_concepts(text: str) -> Set[str]:
    """Extract concepts without guessing from unrelated words."""
    if not text or not text.strip():
        return set()
    enriched = " ".join((
        text.casefold(),
        normalize_indic_phonetics(text).casefold(),
        transliterate_indic_to_latin(text).casefold(),
    ))
    result: Set[str] = set()
    for concept, stems in _CONCEPTS.items():
        for stem in stems:
            term = stem.strip().casefold()
            if term.isascii():
                if re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", enriched):
                    result.add(concept)
                    break
            elif term in enriched:
                result.add(concept)
                break
    return result


def metric_mismatch_reason(question: str, sql: str, dialect: str = "duckdb") -> str | None:
    """Reject SQL provably missing a specifically requested metric.

    This check is only applied to explicitly recognizable metrics. SQL AST columns
    rather than SQL text are inspected to avoid matching comments or literals.
    """
    concepts = extract_query_concepts(question)
    requested = []
    if "literacy" in concepts:
        requested.append(("literacy", ("literacy", "literate", "illiterate")))
    if "beneficiaries" in concepts and "literacy" not in concepts:
        requested.append(("beneficiaries", ("beneficiar", "benefit_count")))
    if "student" in concepts and "farmer" not in concepts:
        requested.append(("student enrollment", ("student", "enrollment", "enrolment")))
    if "crop_production" in concepts:
        requested.append(("crop production", ("production", "yield")))
    if not requested:
        return None

    try:
        ast = sqlglot.parse_one(sql, read=dialect)
    except Exception:
        return "Cannot verify SQL metric alignment because generated SQL is not parseable."
    if not isinstance(ast, (exp.Select, exp.Union)):
        return "Cannot verify metric alignment: generated SQL is not read-only SELECT."
    columns = {node.name.casefold() for node in ast.find_all(exp.Column)}
    for name, accepted in requested:
        if not any(any(token in column for token in accepted) for column in columns):
            return (
                f"Requested {name} metric does not match the columns referenced "
                "by generated SQL. No query was executed."
            )
    if "literacy" in concepts:
        if "female" in concepts and not any("female" in c for c in columns):
            return "Requested female literacy metric does not match generated SQL. No query was executed."
        if "male" in concepts and not any("male" in c for c in columns):
            return "Requested male literacy metric does not match generated SQL. No query was executed."
    return None
