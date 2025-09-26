"""Database models for MCP UI Aggregator."""

from datetime import datetime
from typing import Optional, List
from enum import Enum

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func

Base = declarative_base()


class ComponentType(str, Enum):
    """Component type enumeration."""
    BUTTON = "button"
    INPUT = "input"
    CARD = "card"
    MODAL = "modal"
    NAVIGATION = "navigation"
    LAYOUT = "layout"
    DATA_DISPLAY = "data_display"
    FEEDBACK = "feedback"
    FORM = "form"
    OTHER = "other"


class Namespace(str, Enum):
    """Namespace enumeration."""
    MATERIAL = "material"
    SHADCN = "shadcn"
    CHAKRA = "chakra"
    ANTD = "antd"
    MANTINE = "mantine"


class Component(Base):
    """UI Component model."""
    
    __tablename__ = "components"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    namespace = Column(String(50), nullable=False, index=True)
    component_type = Column(String(50), nullable=False, index=True)
    
    # Metadata
    title = Column(String(500), nullable=False)
    description = Column(Text)
    tags = Column(Text)  # JSON string of tags
    
    # Documentation
    documentation_url = Column(String(1000))
    api_reference_url = Column(String(1000))
    examples_url = Column(String(1000))
    
    # Code
    import_statement = Column(Text)
    basic_usage = Column(Text)
    
    # Search
    search_vector = Column(Text)  # For full-text search
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    code_examples = relationship("CodeExample", back_populates="component", cascade="all, delete-orphan")
    docs_sections = relationship("DocumentationSection", back_populates="component", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('name', 'namespace', name='uq_component_name_namespace'),
        Index('ix_component_search', 'name', 'title', 'description'),
        Index('ix_component_namespace_type', 'namespace', 'component_type'),
    )
    
    def __repr__(self) -> str:
        return f"<Component {self.namespace}/{self.name}>"


class CodeExample(Base):
    """Code example for a component."""
    
    __tablename__ = "code_examples"
    
    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey("components.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    code = Column(Text, nullable=False)
    language = Column(String(50), default="typescript")
    
    # Example metadata
    is_basic = Column(Boolean, default=False)
    is_advanced = Column(Boolean, default=False)
    framework = Column(String(50))  # react, vue, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    component = relationship("Component", back_populates="code_examples")
    
    def __repr__(self) -> str:
        return f"<CodeExample {self.title} for {self.component.name}>"


class DocumentationSection(Base):
    """Documentation section for a component."""
    
    __tablename__ = "documentation_sections"
    
    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey("components.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    section_type = Column(String(50), nullable=False)  # props, usage, examples, etc.
    order_index = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    component = relationship("Component", back_populates="docs_sections")
    
    # Constraints
    __table_args__ = (
        Index('ix_docs_component_type', 'component_id', 'section_type'),
        Index('ix_docs_order', 'component_id', 'order_index'),
    )
    
    def __repr__(self) -> str:
        return f"<DocumentationSection {self.title} for {self.component.name}>"


class IngestionLog(Base):
    """Log of ingestion operations."""
    
    __tablename__ = "ingestion_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    namespace = Column(String(50), nullable=False, index=True)
    source_url = Column(String(1000), nullable=False)
    
    # Status
    status = Column(String(50), nullable=False)  # started, completed, failed
    components_processed = Column(Integer, default=0)
    components_created = Column(Integer, default=0)
    components_updated = Column(Integer, default=0)
    
    # Error info
    error_message = Column(Text)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    def __repr__(self) -> str:
        return f"<IngestionLog {self.namespace} - {self.status}>"