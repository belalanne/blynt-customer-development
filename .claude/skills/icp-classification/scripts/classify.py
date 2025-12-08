"""ICP Classification Helper - Classify companies into Blynt's ICP categories."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ICP(Enum):
    """Blynt ICP Categories."""
    ICP1 = "1"  # Speech/Dictation Products
    ICP2 = "2"  # Meeting AI Assistants
    ICP3 = "3"  # Voice Agents Platforms
    ICP4 = "4"  # Custom Speech/Voice Solutions
    NA = "N/A"  # Not a Fit


class Confidence(Enum):
    """Classification confidence levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class ClassificationResult:
    """Result of ICP classification."""
    icp: ICP
    confidence: Confidence
    signals: list[str]
    reasoning: str
    blynt_fit: str
    value_prop: str


# Signal patterns for each ICP
ICP_SIGNALS = {
    ICP.ICP1: {
        "keywords": [
            "dictation", "speech-to-text", "voice input", "transcription app",
            "medical dictation", "legal transcription", "note-taking",
            "voice typing", "speech recognition app", "accessibility"
        ],
        "companies": [
            "nuance", "dragon", "otter.ai", "speechmatics", "rev.ai"
        ],
        "job_titles": [
            "speech engineer", "asr engineer", "transcription"
        ]
    },
    ICP.ICP2: {
        "keywords": [
            "meeting transcription", "meeting assistant", "call recording",
            "conversation intelligence", "sales call", "meeting notes",
            "video conferencing", "call analytics", "meeting ai"
        ],
        "companies": [
            "otter.ai", "fireflies", "gong", "chorus", "grain", "tldv",
            "jiminny", "avoma", "fathom"
        ],
        "job_titles": [
            "meeting ai", "conversation analytics", "call intelligence"
        ]
    },
    ICP.ICP3: {
        "keywords": [
            "voice agent", "phone agent", "ai phone", "voice bot",
            "conversational ai", "voice assistant", "ivr replacement",
            "ai receptionist", "phone automation", "voice ai platform"
        ],
        "companies": [
            "vapi", "bland", "retell", "vocode", "air.ai", "goodcall",
            "poly.ai", "replicant"
        ],
        "job_titles": [
            "voice ai", "conversational ai", "voice agent"
        ]
    },
    ICP.ICP4: {
        "keywords": [
            "enterprise voice", "custom asr", "white-label voice",
            "voice infrastructure", "proprietary speech", "on-premise voice",
            "regulated industry", "custom voice solution"
        ],
        "companies": [],  # Usually internal/enterprise
        "job_titles": [
            "voice platform", "speech platform", "enterprise voice"
        ]
    }
}

# Negative signals (not a fit)
NEGATIVE_SIGNALS = [
    "text-only", "chatbot without voice", "no audio", "written only",
    "hardware only", "microphone manufacturer", "speaker manufacturer",
    "podcast hosting", "music streaming", "pre-recorded only"
]


def detect_signals(text: str) -> dict[ICP, list[str]]:
    """Detect ICP signals in text.

    Args:
        text: Text to analyze (product description, job posting, etc.)

    Returns:
        Dictionary mapping ICP to list of detected signals
    """
    text_lower = text.lower()
    detected = {icp: [] for icp in ICP if icp != ICP.NA}

    for icp, signals in ICP_SIGNALS.items():
        # Check keywords
        for keyword in signals["keywords"]:
            if keyword in text_lower:
                detected[icp].append(f"keyword: {keyword}")

        # Check company mentions
        for company in signals["companies"]:
            if company in text_lower:
                detected[icp].append(f"competitor: {company}")

        # Check job titles
        for title in signals["job_titles"]:
            if title in text_lower:
                detected[icp].append(f"job_signal: {title}")

    return detected


def check_negative_signals(text: str) -> list[str]:
    """Check for signals that indicate company is not a fit.

    Args:
        text: Text to analyze

    Returns:
        List of detected negative signals
    """
    text_lower = text.lower()
    return [signal for signal in NEGATIVE_SIGNALS if signal in text_lower]


def classify_company(
    description: str,
    job_postings: Optional[str] = None,
    tech_stack: Optional[str] = None
) -> ClassificationResult:
    """Classify a company into an ICP category.

    Args:
        description: Company/product description
        job_postings: Optional job posting text
        tech_stack: Optional tech stack information

    Returns:
        ClassificationResult with ICP, confidence, and reasoning
    """
    # Combine all text
    all_text = description
    if job_postings:
        all_text += " " + job_postings
    if tech_stack:
        all_text += " " + tech_stack

    # Check negative signals first
    negative = check_negative_signals(all_text)
    if negative:
        return ClassificationResult(
            icp=ICP.NA,
            confidence=Confidence.HIGH,
            signals=negative,
            reasoning=f"Negative signals detected: {', '.join(negative)}",
            blynt_fit="None",
            value_prop="N/A - Company does not use real-time voice/speech"
        )

    # Detect positive signals
    detected = detect_signals(all_text)

    # Score each ICP
    scores = {icp: len(signals) for icp, signals in detected.items()}

    # Find best match
    best_icp = max(scores, key=scores.get)
    best_score = scores[best_icp]

    if best_score == 0:
        return ClassificationResult(
            icp=ICP.NA,
            confidence=Confidence.LOW,
            signals=[],
            reasoning="No clear voice/speech signals detected",
            blynt_fit="Unknown - needs manual review",
            value_prop="N/A"
        )

    # Determine confidence
    if best_score >= 3:
        confidence = Confidence.HIGH
    elif best_score >= 2:
        confidence = Confidence.MEDIUM
    else:
        confidence = Confidence.LOW

    # Generate value prop based on ICP
    value_props = {
        ICP.ICP1: "Accurate real-time transcription with custom vocabulary boosting for domain-specific terms",
        ICP.ICP2: "Natural turn-taking for multi-speaker detection, real-time processing for live meetings",
        ICP.ICP3: "Low-latency transcription with interruption handling for natural conversations",
        ICP.ICP4: "Flexible API with enterprise-grade features, customization options"
    }

    fit_scores = {
        ICP.ICP1: "High",
        ICP.ICP2: "High",
        ICP.ICP3: "Very High",
        ICP.ICP4: "Medium-High"
    }

    return ClassificationResult(
        icp=best_icp,
        confidence=confidence,
        signals=detected[best_icp],
        reasoning=f"Detected {best_score} signals for {best_icp.name}",
        blynt_fit=fit_scores.get(best_icp, "Unknown"),
        value_prop=value_props.get(best_icp, "")
    )


# CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python classify.py '<company description>'")
        sys.exit(1)

    description = sys.argv[1]
    result = classify_company(description)

    print(f"ICP: {result.icp.value}")
    print(f"Confidence: {result.confidence.value}")
    print(f"Signals: {result.signals}")
    print(f"Reasoning: {result.reasoning}")
    print(f"Blynt Fit: {result.blynt_fit}")
    print(f"Value Prop: {result.value_prop}")
