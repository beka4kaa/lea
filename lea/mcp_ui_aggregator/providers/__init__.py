"""Component providers package."""

from .registry import registry, get_provider, register_provider, get_all_providers
from .base import BaseProvider, HTTPProvider, GitHubProvider

# Import all providers to ensure they are registered
from .magicui import MagicUIProvider
from .shadcn import ShadcnUIProvider
from .daisyui import DaisyUIProvider
from .reactbits import ReactBitsProvider
from .aceternity import AceternityProvider
from .alignui import AlignUIProvider
from .twenty_first import TwentyFirstProvider
from .bentogrids import BentoGridsProvider
from .nextjs_design import NextJSDesignProvider
from .hyperui import HyperUIProvider
from .tailwind_components import TailwindComponentsProvider

__all__ = [
    "registry",
    "get_provider", 
    "register_provider",
    "get_all_providers",
    "BaseProvider",
    "HTTPProvider", 
    "GitHubProvider",
    "MagicUIProvider",
    "ShadcnUIProvider",
    "DaisyUIProvider",
    "ReactBitsProvider",
    "AceternityProvider",
    "AlignUIProvider",
    "TwentyFirstProvider",
    "BentoGridsProvider",
    "NextJSDesignProvider",
    "HyperUIProvider",
    "TailwindComponentsProvider"
]