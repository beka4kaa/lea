"""Analytics and monitoring for MCP UI Aggregator."""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics for API endpoints and operations."""
    operation: str
    duration_ms: float
    timestamp: datetime
    status: str = "success"  # success, error, timeout
    user_id: Optional[str] = None
    namespace: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UsageAnalytics:
    """Usage analytics for business intelligence."""
    endpoint: str
    method: str
    user_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    response_time_ms: float = 0
    status_code: int = 200
    namespace: Optional[str] = None
    component_name: Optional[str] = None
    search_query: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None


class PerformanceMonitor:
    """Monitor performance and collect metrics."""
    
    def __init__(self, max_metrics: int = 10000):
        self.metrics: deque = deque(maxlen=max_metrics)
        self.endpoint_stats: Dict[str, List[float]] = defaultdict(list)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.start_time = datetime.utcnow()
    
    def record_metric(self, metric: PerformanceMetrics):
        """Record a performance metric."""
        self.metrics.append(metric)
        
        # Update endpoint statistics
        self.endpoint_stats[metric.operation].append(metric.duration_ms)
        
        # Keep only last 1000 measurements per endpoint for memory efficiency
        if len(self.endpoint_stats[metric.operation]) > 1000:
            self.endpoint_stats[metric.operation] = self.endpoint_stats[metric.operation][-1000:]
        
        # Track errors
        if metric.status == "error":
            self.error_counts[metric.operation] += 1
        
        # Log slow operations
        if metric.duration_ms > 5000:  # 5 seconds
            logger.warning(f"Slow operation detected: {metric.operation} took {metric.duration_ms}ms")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics."""
        now = datetime.utcnow()
        uptime = (now - self.start_time).total_seconds()
        
        endpoint_summary = {}
        for endpoint, durations in self.endpoint_stats.items():
            if durations:
                endpoint_summary[endpoint] = {
                    "count": len(durations),
                    "avg_ms": sum(durations) / len(durations),
                    "min_ms": min(durations),
                    "max_ms": max(durations),
                    "p95_ms": self._percentile(durations, 95),
                    "p99_ms": self._percentile(durations, 99),
                    "error_count": self.error_counts.get(endpoint, 0),
                    "error_rate": self.error_counts.get(endpoint, 0) / len(durations) * 100
                }
        
        return {
            "uptime_seconds": uptime,
            "total_metrics": len(self.metrics),
            "endpoints": endpoint_summary,
            "recent_errors": [
                m for m in list(self.metrics)[-100:] 
                if m.status == "error"
            ]
        }
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of a list of numbers."""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        return sorted_data[int(index)]
    
    def get_slow_operations(self, threshold_ms: float = 1000) -> List[PerformanceMetrics]:
        """Get operations that took longer than threshold."""
        return [m for m in self.metrics if m.duration_ms > threshold_ms]


class UsageAnalyzer:
    """Analyze usage patterns for business intelligence."""
    
    def __init__(self, max_records: int = 50000):
        self.usage_records: deque = deque(maxlen=max_records)
        self.daily_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    
    def record_usage(self, analytics: UsageAnalytics):
        """Record usage analytics."""
        self.usage_records.append(analytics)
        
        # Update daily statistics
        date_key = analytics.timestamp.strftime("%Y-%m-%d")
        self.daily_stats[date_key]["total_requests"] += 1
        
        if analytics.namespace:
            self.daily_stats[date_key][f"namespace_{analytics.namespace}"] += 1
        
        if analytics.endpoint:
            self.daily_stats[date_key][f"endpoint_{analytics.endpoint}"] += 1
    
    def get_usage_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get usage summary for the last N days."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days-1)
        
        summary = {
            "period": f"{start_date} to {end_date}",
            "total_requests": 0,
            "unique_users": set(),
            "top_endpoints": defaultdict(int),
            "top_namespaces": defaultdict(int),
            "top_components": defaultdict(int),
            "daily_breakdown": {}
        }
        
        # Analyze recent records
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        recent_records = [r for r in self.usage_records if r.timestamp > cutoff_time]
        
        for record in recent_records:
            summary["total_requests"] += 1
            
            if record.user_id:
                summary["unique_users"].add(record.user_id)
            
            if record.endpoint:
                summary["top_endpoints"][record.endpoint] += 1
            
            if record.namespace:
                summary["top_namespaces"][record.namespace] += 1
            
            if record.component_name:
                summary["top_components"][record.component_name] += 1
        
        # Convert sets to counts
        summary["unique_users"] = len(summary["unique_users"])
        
        # Sort top items
        summary["top_endpoints"] = dict(sorted(summary["top_endpoints"].items(), 
                                             key=lambda x: x[1], reverse=True)[:10])
        summary["top_namespaces"] = dict(sorted(summary["top_namespaces"].items(), 
                                               key=lambda x: x[1], reverse=True)[:10])
        summary["top_components"] = dict(sorted(summary["top_components"].items(), 
                                               key=lambda x: x[1], reverse=True)[:10])
        
        # Add daily breakdown from stored stats
        for i in range(days):
            date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
            summary["daily_breakdown"][date] = dict(self.daily_stats.get(date, {}))
        
        return summary
    
    def get_popular_components(self, namespace: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get most popular components."""
        component_counts = defaultdict(int)
        component_namespaces = {}
        
        for record in self.usage_records:
            if record.component_name:
                if namespace is None or record.namespace == namespace:
                    component_counts[record.component_name] += 1
                    component_namespaces[record.component_name] = record.namespace
        
        # Sort by popularity
        popular = sorted(component_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        return [
            {
                "component": name,
                "namespace": component_namespaces.get(name),
                "usage_count": count,
                "popularity_score": count / max(component_counts.values()) * 100
            }
            for name, count in popular
        ]
    
    def get_search_insights(self) -> Dict[str, Any]:
        """Get insights about search behavior."""
        search_queries = [r.search_query for r in self.usage_records 
                         if r.search_query and r.endpoint == "search"]
        
        if not search_queries:
            return {"total_searches": 0}
        
        # Analyze search patterns
        query_counts = defaultdict(int)
        for query in search_queries:
            query_counts[query.lower()] += 1
        
        # Common words in searches
        word_counts = defaultdict(int)
        for query in search_queries:
            for word in query.lower().split():
                if len(word) > 2:  # Ignore very short words
                    word_counts[word] += 1
        
        top_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return {
            "total_searches": len(search_queries),
            "unique_queries": len(query_counts),
            "top_queries": [{"query": q, "count": c} for q, c in top_queries],
            "common_search_terms": [{"word": w, "count": c} for w, c in top_words],
            "avg_query_length": sum(len(q) for q in search_queries) / len(search_queries)
        }


# Global instances
performance_monitor = PerformanceMonitor()
usage_analyzer = UsageAnalyzer()


# Decorator for monitoring performance
def monitor_performance(operation_name: str):
    """Decorator to monitor performance of functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "success"
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                logger.error(f"Error in {operation_name}: {e}")
                raise
            finally:
                duration = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                metric = PerformanceMetrics(
                    operation=operation_name,
                    duration_ms=duration,
                    timestamp=datetime.utcnow(),
                    status=status
                )
                
                performance_monitor.record_metric(metric)
        
        return wrapper
    return decorator


# Async version of the decorator
def monitor_async_performance(operation_name: str):
    """Decorator to monitor performance of async functions."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "success"
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                logger.error(f"Error in {operation_name}: {e}")
                raise
            finally:
                duration = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                metric = PerformanceMetrics(
                    operation=operation_name,
                    duration_ms=duration,
                    timestamp=datetime.utcnow(),
                    status=status
                )
                
                performance_monitor.record_metric(metric)
        
        return wrapper
    return decorator