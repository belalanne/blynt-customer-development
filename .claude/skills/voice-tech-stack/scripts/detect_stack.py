"""Voice Tech Stack Detection - Identify voice/speech providers from text."""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class StackCategory(Enum):
    """Voice tech stack categories."""
    TRANSPORT = "Transport Protocol"
    REALTIME_FRAMEWORK = "Real-time Framework"
    AGENTIC_FRAMEWORK = "Agentic Framework"
    ASR = "ASR Provider"
    LLM = "LLM Provider"
    TTS = "TTS Provider"
    TELEPHONY = "Telephony"
    MEETING = "Meeting Recording"
    AUDIO = "Audio Processing"


class Confidence(Enum):
    """Detection confidence levels."""
    CONFIRMED = "Confirmed"  # Found in official docs/privacy policy
    HIGH = "High"           # Multiple strong signals
    MEDIUM = "Medium"       # Some signals
    LOW = "Low"            # Weak signals
    INFERRED = "Inferred"  # Based on patterns


@dataclass
class ProviderDetection:
    """A detected provider."""
    name: str
    category: StackCategory
    confidence: Confidence
    evidence: list[str] = field(default_factory=list)


@dataclass
class StackDetectionResult:
    """Result of voice tech stack detection."""
    providers: list[ProviderDetection]
    ignored: list[str]  # Non-voice providers found but ignored


# Provider patterns for detection
PROVIDERS = {
    StackCategory.TRANSPORT: {
        "webrtc": ["webrtc", "web rtc", "peer-to-peer audio", "rtc"],
        "websocket": ["websocket", "ws://", "wss://", "socket.io"],
        "sip": ["sip protocol", "sip trunk", "session initiation"],
        "pstn": ["pstn", "phone network", "telephony network"],
    },
    StackCategory.REALTIME_FRAMEWORK: {
        "LiveKit": ["livekit", "livekit.io", "livekit-server"],
        "Pipecat": ["pipecat", "pipecat-ai", "pipecat.ai"],
        "Daily": ["daily.co", "daily-js", "daily api"],
        "Agora": ["agora.io", "agora sdk", "agora rtc"],
        "Twilio": ["twilio video", "twilio programmable video"],
        "FastRTC": ["fastrtc", "fast-rtc"],
    },
    StackCategory.AGENTIC_FRAMEWORK: {
        "Vapi": ["vapi.ai", "vapi api", "vapi voice"],
        "LiveKit Agents": ["livekit agents", "livekit-agents", "@livekit/agents"],
        "Pipecat Flow": ["pipecat flow", "pipecat-flow"],
        "Retell": ["retell.ai", "retellai", "retell api"],
        "Vocode": ["vocode", "vocode.dev", "vocode-core"],
        "Bland AI": ["bland.ai", "bland ai", "blandai"],
    },
    StackCategory.ASR: {
        "Deepgram": ["deepgram", "deepgram.com", "deepgram-sdk", "nova-2"],
        "Gladia": ["gladia", "gladia.io"],
        "Assembly AI": ["assemblyai", "assembly ai", "assembly-ai"],
        "Azure Speech": ["azure speech", "cognitive services speech", "microsoft speech"],
        "Google Speech": ["google speech", "speech-to-text api", "google cloud speech"],
        "Whisper": ["openai whisper", "whisper api", "whisper model"],
        "Rev AI": ["rev.ai", "rev ai", "revai"],
        "Speechmatics": ["speechmatics", "speechmatics.com"],
    },
    StackCategory.LLM: {
        "OpenAI": ["openai", "gpt-4", "gpt-3.5", "chatgpt api"],
        "Anthropic": ["anthropic", "claude", "claude-3"],
        "Google Gemini": ["gemini", "google gemini", "gemini pro"],
        "Azure OpenAI": ["azure openai", "openai on azure"],
        "Cohere": ["cohere", "cohere.ai", "command model"],
        "Mistral": ["mistral", "mistral ai", "mixtral"],
    },
    StackCategory.TTS: {
        "ElevenLabs": ["elevenlabs", "eleven labs", "11labs"],
        "Play.ht": ["play.ht", "playht", "play ht"],
        "Deepgram Aura": ["deepgram aura", "aura tts"],
        "Azure TTS": ["azure tts", "azure text-to-speech", "cognitive services tts"],
        "Google TTS": ["google tts", "google text-to-speech", "wavenet"],
        "OpenAI TTS": ["openai tts", "openai text-to-speech"],
        "Cartesia": ["cartesia", "cartesia.ai"],
        "LMNT": ["lmnt", "lmnt.com"],
    },
    StackCategory.TELEPHONY: {
        "Twilio Voice": ["twilio voice", "twilio programmable voice", "twilio pstn"],
        "Vonage": ["vonage", "nexmo"],
        "Bandwidth": ["bandwidth.com", "bandwidth api"],
        "SignalWire": ["signalwire", "signal wire"],
        "Plivo": ["plivo", "plivo.com"],
        "Telnyx": ["telnyx", "telnyx.com"],
    },
    StackCategory.MEETING: {
        "Recall.ai": ["recall.ai", "recallai", "recall api"],
        "Fireflies API": ["fireflies api", "fireflies.ai api"],
    },
    StackCategory.AUDIO: {
        "Krisp": ["krisp", "krisp.ai", "krisp noise"],
        "Dolby.io": ["dolby.io", "dolby api", "dolby audio"],
    },
}

# Providers to IGNORE (not voice-specific)
IGNORE_PROVIDERS = [
    "aws", "amazon web services", "ec2", "s3", "lambda",
    "google cloud platform", "gcp", "compute engine",
    "azure", "microsoft azure",
    "cloudflare", "fastly", "akamai",
    "google analytics", "mixpanel", "amplitude", "segment",
    "hubspot", "mailchimp", "intercom", "zendesk",
    "stripe", "braintree", "paypal",
    "auth0", "okta", "firebase auth",
    "postgresql", "mysql", "mongodb", "redis", "dynamodb",
    "datadog", "new relic", "sentry", "splunk",
    "github", "gitlab", "bitbucket",
    "slack", "discord", "teams",
]


def detect_providers(text: str, source_type: str = "unknown") -> StackDetectionResult:
    """Detect voice tech stack providers in text.

    Args:
        text: Text to analyze (privacy policy, job posting, docs, etc.)
        source_type: Type of source for confidence scoring
            - "privacy_policy": High confidence
            - "job_posting": Medium confidence
            - "documentation": High confidence
            - "blog": Medium confidence
            - "unknown": Low confidence

    Returns:
        StackDetectionResult with detected providers and ignored items
    """
    text_lower = text.lower()
    detected: list[ProviderDetection] = []
    ignored: list[str] = []

    # Check for ignored providers
    for provider in IGNORE_PROVIDERS:
        if provider in text_lower:
            ignored.append(provider)

    # Determine base confidence from source type
    base_confidence = {
        "privacy_policy": Confidence.CONFIRMED,
        "subprocessor_list": Confidence.CONFIRMED,
        "documentation": Confidence.HIGH,
        "job_posting": Confidence.MEDIUM,
        "blog": Confidence.MEDIUM,
        "github": Confidence.HIGH,
        "unknown": Confidence.LOW,
    }.get(source_type, Confidence.LOW)

    # Detect voice providers
    for category, providers in PROVIDERS.items():
        for provider_name, patterns in providers.items():
            evidence = []
            for pattern in patterns:
                # Case-insensitive search
                if pattern.lower() in text_lower:
                    # Find context around the match
                    idx = text_lower.find(pattern.lower())
                    start = max(0, idx - 50)
                    end = min(len(text), idx + len(pattern) + 50)
                    context = text[start:end].strip()
                    evidence.append(f"'{pattern}' found: ...{context}...")

            if evidence:
                # Adjust confidence based on evidence strength
                if len(evidence) >= 3:
                    confidence = Confidence.CONFIRMED if base_confidence == Confidence.CONFIRMED else Confidence.HIGH
                elif len(evidence) >= 2:
                    confidence = base_confidence
                else:
                    confidence = Confidence.LOW if base_confidence == Confidence.LOW else Confidence.MEDIUM

                detected.append(ProviderDetection(
                    name=provider_name,
                    category=category,
                    confidence=confidence,
                    evidence=evidence
                ))

    return StackDetectionResult(providers=detected, ignored=ignored)


def format_stack_report(result: StackDetectionResult) -> str:
    """Format detection result as a readable report.

    Args:
        result: StackDetectionResult to format

    Returns:
        Formatted string report
    """
    lines = ["# Voice Tech Stack Detection Report\n"]

    # Group by category
    by_category: dict[StackCategory, list[ProviderDetection]] = {}
    for provider in result.providers:
        if provider.category not in by_category:
            by_category[provider.category] = []
        by_category[provider.category].append(provider)

    # Output by category
    for category in StackCategory:
        if category in by_category:
            lines.append(f"\n## {category.value}\n")
            for provider in by_category[category]:
                lines.append(f"- **{provider.name}** ({provider.confidence.value})")
                for evidence in provider.evidence[:2]:  # Limit evidence shown
                    lines.append(f"  - {evidence[:100]}...")

    # Ignored providers
    if result.ignored:
        lines.append(f"\n## Ignored (non-voice infrastructure)\n")
        lines.append(f"- {', '.join(result.ignored[:10])}")
        if len(result.ignored) > 10:
            lines.append(f"- ...and {len(result.ignored) - 10} more")

    return "\n".join(lines)


def extract_from_url_patterns(urls: list[str]) -> list[ProviderDetection]:
    """Extract provider hints from URL patterns.

    Args:
        urls: List of URLs found in text

    Returns:
        List of provider detections based on URL patterns
    """
    detections = []
    url_patterns = {
        "deepgram.com": ("Deepgram", StackCategory.ASR),
        "assemblyai.com": ("Assembly AI", StackCategory.ASR),
        "gladia.io": ("Gladia", StackCategory.ASR),
        "elevenlabs.io": ("ElevenLabs", StackCategory.TTS),
        "play.ht": ("Play.ht", StackCategory.TTS),
        "livekit.io": ("LiveKit", StackCategory.REALTIME_FRAMEWORK),
        "daily.co": ("Daily", StackCategory.REALTIME_FRAMEWORK),
        "twilio.com": ("Twilio", StackCategory.TELEPHONY),
        "vapi.ai": ("Vapi", StackCategory.AGENTIC_FRAMEWORK),
        "retell.ai": ("Retell", StackCategory.AGENTIC_FRAMEWORK),
    }

    for url in urls:
        url_lower = url.lower()
        for pattern, (name, category) in url_patterns.items():
            if pattern in url_lower:
                detections.append(ProviderDetection(
                    name=name,
                    category=category,
                    confidence=Confidence.HIGH,
                    evidence=[f"URL reference: {url}"]
                ))

    return detections


# CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_stack.py '<text to analyze>' [source_type]")
        print("Source types: privacy_policy, job_posting, documentation, blog, github")
        sys.exit(1)

    text = sys.argv[1]
    source_type = sys.argv[2] if len(sys.argv) > 2 else "unknown"

    result = detect_providers(text, source_type)
    print(format_stack_report(result))
