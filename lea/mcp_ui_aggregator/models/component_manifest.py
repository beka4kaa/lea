"""Component Manifest v1 - Unified model for all UI component providers."""

from typing import Any, Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class LicenseType(str, Enum):
    """License types for components."""
    MIT = "MIT"
    MIT_COMMONS_CLAUSE = "MIT+CommonsClause"
    PRO = "Pro"
    APACHE_2 = "Apache-2.0"
    BSD_3 = "BSD-3-Clause"
    CUSTOM = "Custom"


class TailwindVersion(str, Enum):
    """Supported Tailwind CSS versions."""
    V3 = "v3"
    V4 = "v4"


class ComponentCategory(str, Enum):
    """Component categories."""
    ANIMATED = "animated"
    TEXT = "text"
    FORMS = "forms"
    NAVIGATION = "navigation"
    BACKGROUNDS = "backgrounds"
    LAYOUTS = "layouts"
    TEMPLATES = "templates"
    DATA_DISPLAY = "data_display"
    FEEDBACK = "feedback"
    BUTTONS = "buttons"
    INPUTS = "inputs"
    MODALS = "modals"
    CARDS = "cards"
    TABLES = "tables"
    OVERLAYS = "overlays"
    DISCLOSURE = "disclosure"
    LAYOUT = "layout"
    OTHER = "other"


class Provider(str, Enum):
    """Supported component providers."""
    MAGICUI = "magicui"
    SHADCN = "shadcn"
    MUI = "mui"
    DAISYUI = "daisyui"
    REACTBITS = "reactbits"
    ACETERNITY = "aceternity"
    ALIGNUI = "alignui"
    TWENTY_FIRST = "twenty_first"
    BENTOGRIDS = "bentogrids"
    NEXTJS_DESIGN = "nextjs_design"
    HYPERUI = "hyperui"
    TAILWIND_COMPONENTS = "tailwind_components"


class License(BaseModel):
    """License information."""
    type: LicenseType
    url: Optional[HttpUrl] = None
    notes: Optional[str] = None
    redistribute: bool = True
    commercial: bool = True


class Source(BaseModel):
    """Source code information."""
    url: HttpUrl
    commit: Optional[str] = None
    branch: Optional[str] = "main"


class Framework(BaseModel):
    """Framework support information."""
    react: bool = False
    vue: bool = False
    angular: bool = False
    svelte: bool = False
    solid: bool = False
    next: bool = False
    nuxt: bool = False
    html: bool = False


class TailwindConfig(BaseModel):
    """Tailwind CSS configuration."""
    version: TailwindVersion
    plugin_deps: List[str] = Field(default_factory=list)
    required_classes: List[str] = Field(default_factory=list)
    custom_css: Optional[str] = None


class ComponentCode(BaseModel):
    """Component code in various formats."""
    tsx: Optional[str] = None
    jsx: Optional[str] = None
    vue: Optional[str] = None
    svelte: Optional[str] = None
    angular: Optional[str] = None
    html: Optional[str] = None
    css: Optional[str] = None
    js: Optional[str] = None
    ts: Optional[str] = None


class ComponentAccess(BaseModel):
    """Component access methods."""
    copy_paste: bool = True
    cli: Optional[str] = None
    npm: Optional[str] = None
    cdn: Optional[HttpUrl] = None
    free: bool = True
    pro: bool = False


class InstallPlan(BaseModel):
    """Installation plan for a component."""
    npm: List[str] = Field(default_factory=list)
    yarn: List[str] = Field(default_factory=list)
    pnpm: List[str] = Field(default_factory=list)
    bun: List[str] = Field(default_factory=list)
    steps: List[Dict[str, Any]] = Field(default_factory=list)


class ComponentManifest(BaseModel):
    """Unified component manifest."""
    # Core identity
    id: str = Field(..., description="Unique component identifier")
    provider: Provider = Field(..., description="Provider that offers this component")
    name: str = Field(..., description="Human-readable component name")
    slug: str = Field(..., description="URL-safe component slug")
    
    # Categorization
    category: ComponentCategory = Field(..., description="Primary component category")
    tags: List[str] = Field(default_factory=list, description="Search and filter tags")
    
    # Legal and licensing
    license: License = Field(..., description="Component license information")
    
    # Source information
    source: Source = Field(..., description="Source code location")
    
    # Framework support
    framework: Framework = Field(..., description="Supported frameworks")
    
    # Styling system
    tailwind: Optional[TailwindConfig] = Field(None, description="Tailwind CSS configuration")
    
    # Dependencies and installation
    runtime_deps: List[str] = Field(default_factory=list, description="Runtime dependencies")
    peer_deps: List[str] = Field(default_factory=list, description="Peer dependencies")
    dev_deps: List[str] = Field(default_factory=list, description="Development dependencies")
    install: InstallPlan = Field(default_factory=InstallPlan, description="Installation instructions")
    
    # Code and content
    code: ComponentCode = Field(default_factory=ComponentCode, description="Component source code")
    
    # Access and availability
    access: ComponentAccess = Field(default_factory=ComponentAccess, description="How to access this component")
    
    # Documentation and examples
    description: Optional[str] = Field(None, description="Component description")
    documentation_url: Optional[HttpUrl] = Field(None, description="Documentation URL")
    demo_url: Optional[HttpUrl] = Field(None, description="Live demo URL")
    playground_url: Optional[HttpUrl] = Field(None, description="Interactive playground URL")
    
    # Metadata
    keywords: List[str] = Field(default_factory=list, description="SEO and search keywords")
    author: Optional[str] = Field(None, description="Component author")
    version: Optional[str] = Field(None, description="Component version")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    # Popularity and quality metrics
    downloads: Optional[int] = Field(None, description="Download count")
    stars: Optional[int] = Field(None, description="GitHub stars or equivalent")
    forks: Optional[int] = Field(None, description="GitHub forks or equivalent")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        extra = "forbid"
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ComponentSearchFilter(BaseModel):
    """Search filter for components."""
    provider: Optional[Provider] = None
    category: Optional[ComponentCategory] = None
    framework: Optional[str] = None
    free_only: bool = False
    pro_only: bool = False
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class ComponentSearchResult(BaseModel):
    """Search result container."""
    components: List[ComponentManifest]
    total: int
    page: int = 1
    limit: int = 50
    filters: ComponentSearchFilter
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True