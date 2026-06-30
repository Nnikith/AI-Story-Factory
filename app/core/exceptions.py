class StoryFactoryError(Exception):
    """Base exception."""


class ConfigurationError(StoryFactoryError):
    """Configuration problems."""


class TimelineError(StoryFactoryError):
    """Timeline problems."""


class ImageGenerationError(StoryFactoryError):
    """Image generation failed."""


class VoiceGenerationError(StoryFactoryError):
    """Voice generation failed."""


class RendererError(StoryFactoryError):
    """Renderer failed."""