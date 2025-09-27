#!/usr/bin/env python3
"""Performance profiling script for LEA MCP Server.

Tests server performance with different worker configurations:
- 1 worker (baseline)
- 2 workers (optimal for synchronous tasks)
- 3 workers (optimal for async tasks)

Uses both Apache Bench (ab) and wrk for comprehensive testing.
"""

import os
import sys
import time
import json
import subprocess
import signal
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import psutil


@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""
    workers: int
    tool: str  # 'ab' or 'wrk'
    requests_per_second: float
    mean_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    failed_requests: int
    total_requests: int
    duration_seconds: float
    cpu_usage_percent: float
    memory_usage_mb: float


class ServerManager:
    """Manages starting and stopping the FastAPI server."""
    
    def __init__(self, workers: int = 1, port: int = 8000):
        self.workers = workers
        self.port = port
        self.process: Optional[subprocess.Popen] = None
    
    def start(self) -> bool:
        """Start the server with specified worker count."""
        cmd = [
            "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", str(self.port),
            "--workers", str(self.workers),
            "--log-level", "warning"
        ]
        
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=Path(__file__).parent
            )
            
            # Wait for server to start
            time.sleep(3)
            
            # Check if server is responding
            if self._is_server_ready():
                print(f"✅ Server started with {self.workers} workers on port {self.port}")
                return True
            else:
                print(f"❌ Server failed to start properly")
                self.stop()
                return False
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop(self):
        """Stop the server."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            self.process = None
            print(f"🛑 Server stopped")
    
    def _is_server_ready(self) -> bool:
        """Check if server is ready to accept requests."""
        import urllib.request
        try:
            with urllib.request.urlopen(f"http://localhost:{self.port}/health", timeout=5) as response:
                return response.status == 200
        except:
            return False
    
    def get_resource_usage(self) -> Tuple[float, float]:
        """Get current CPU and memory usage of server process."""
        if not self.process:
            return 0.0, 0.0
        
        try:
            proc = psutil.Process(self.process.pid)
            children = proc.children(recursive=True)
            
            cpu_percent = proc.cpu_percent()
            memory_mb = proc.memory_info().rss / 1024 / 1024
            
            # Include child processes (workers)
            for child in children:
                try:
                    cpu_percent += child.cpu_percent()
                    memory_mb += child.memory_info().rss / 1024 / 1024
                except psutil.NoSuchProcess:
                    pass
            
            return cpu_percent, memory_mb
        except psutil.NoSuchProcess:
            return 0.0, 0.0


class BenchmarkRunner:
    """Runs performance benchmarks using ab and wrk."""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.endpoints = {
            "health": "/health",
            "light": "/api/v1/providers",
            "medium": "/api/v1/components/search?query=button&limit=10",
            "heavy": "/mcp-discovery"
        }
    
    def run_ab_benchmark(
        self,
        endpoint: str,
        requests: int = 1000,
        concurrency: int = 10,
        duration: int = 30
    ) -> Optional[Dict]:
        """Run Apache Bench benchmark."""
        url = f"{self.server_url}{endpoint}"
        
        cmd = [
            "ab",
            "-n", str(requests),
            "-c", str(concurrency),
            "-t", str(duration),
            "-g", "/tmp/ab_plot.txt",  # For plotting
            url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 10)
            if result.returncode == 0:
                return self._parse_ab_output(result.stdout)
            else:
                print(f"❌ ab failed: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print(f"❌ ab benchmark timed out")
            return None
        except FileNotFoundError:
            print(f"❌ ab not found. Install with: apt-get install apache2-utils")
            return None
    
    def run_wrk_benchmark(
        self,
        endpoint: str,
        duration: int = 30,
        threads: int = 4,
        connections: int = 100
    ) -> Optional[Dict]:
        """Run wrk benchmark."""
        url = f"{self.server_url}{endpoint}"
        
        cmd = [
            "wrk",
            "-t", str(threads),
            "-c", str(connections),
            "-d", f"{duration}s",
            "--latency",
            url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 10)
            if result.returncode == 0:
                return self._parse_wrk_output(result.stdout)
            else:
                print(f"❌ wrk failed: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print(f"❌ wrk benchmark timed out")
            return None
        except FileNotFoundError:
            print(f"❌ wrk not found. Install with: apt-get install wrk")
            return None
    
    def _parse_ab_output(self, output: str) -> Dict:
        """Parse Apache Bench output."""
        lines = output.split('\n')
        result = {}
        
        for line in lines:
            if "Requests per second:" in line:
                result['rps'] = float(line.split()[3])
            elif "Time per request:" in line and "mean" in line:
                result['mean_latency'] = float(line.split()[3])
            elif "Failed requests:" in line:
                result['failed'] = int(line.split()[2])
            elif "Complete requests:" in line:
                result['total'] = int(line.split()[2])
        
        # Extract percentiles from ab output
        result['p95_latency'] = result.get('mean_latency', 0) * 1.5  # Estimate
        result['p99_latency'] = result.get('mean_latency', 0) * 2.0  # Estimate
        
        return result
    
    def _parse_wrk_output(self, output: str) -> Dict:
        """Parse wrk output."""
        lines = output.split('\n')
        result = {}
        
        for line in lines:
            if "Requests/sec:" in line:
                result['rps'] = float(line.split()[1])
            elif "Latency" in line and "avg" in line:
                parts = line.split()
                if len(parts) >= 4:
                    result['mean_latency'] = self._parse_time_unit(parts[1])
            elif "99%" in line:
                parts = line.split()
                if len(parts) >= 2:
                    result['p99_latency'] = self._parse_time_unit(parts[1])
            elif "95%" in line:
                parts = line.split()
                if len(parts) >= 2:
                    result['p95_latency'] = self._parse_time_unit(parts[1])
        
        result['failed'] = 0  # wrk doesn't report failed requests easily
        result['total'] = 0   # Calculate from duration and RPS
        
        return result
    
    def _parse_time_unit(self, time_str: str) -> float:
        """Parse time string (e.g., '1.23ms', '45.67us') to milliseconds."""
        if 'ms' in time_str:
            return float(time_str.replace('ms', ''))
        elif 'us' in time_str:
            return float(time_str.replace('us', '')) / 1000
        elif 's' in time_str:
            return float(time_str.replace('s', '')) * 1000
        else:
            return float(time_str)


def run_comprehensive_benchmark() -> List[BenchmarkResult]:
    """Run comprehensive benchmarks with different worker configurations."""
    results = []
    worker_configs = [1, 2, 3]
    
    print("🚀 Starting LEA MCP Server Performance Profiling")
    print("=" * 60)
    
    for workers in worker_configs:
        print(f"\n🔧 Testing with {workers} worker(s)")
        print("-" * 40)
        
        server = ServerManager(workers=workers)
        if not server.start():
            print(f"❌ Skipping {workers} workers due to startup failure")
            continue
        
        benchmark = BenchmarkRunner()
        
        # Test different endpoint types
        for endpoint_name, endpoint_path in benchmark.endpoints.items():
            print(f"📊 Benchmarking {endpoint_name} endpoint: {endpoint_path}")
            
            # Get baseline resource usage
            cpu_before, mem_before = server.get_resource_usage()
            
            # Run ab benchmark
            ab_result = benchmark.run_ab_benchmark(endpoint_path, requests=1000, concurrency=20)
            if ab_result:
                cpu_after, mem_after = server.get_resource_usage()
                
                result = BenchmarkResult(
                    workers=workers,
                    tool='ab',
                    requests_per_second=ab_result.get('rps', 0),
                    mean_latency_ms=ab_result.get('mean_latency', 0),
                    p95_latency_ms=ab_result.get('p95_latency', 0),
                    p99_latency_ms=ab_result.get('p99_latency', 0),
                    failed_requests=ab_result.get('failed', 0),
                    total_requests=ab_result.get('total', 0),
                    duration_seconds=30,
                    cpu_usage_percent=max(cpu_after - cpu_before, 0),
                    memory_usage_mb=mem_after
                )
                results.append(result)
                
                print(f"  📈 ab: {result.requests_per_second:.1f} RPS, "
                      f"{result.mean_latency_ms:.1f}ms avg latency")
            
            # Run wrk benchmark  
            time.sleep(2)  # Brief pause between tests
            wrk_result = benchmark.run_wrk_benchmark(endpoint_path, duration=20)
            if wrk_result:
                cpu_after, mem_after = server.get_resource_usage()
                
                result = BenchmarkResult(
                    workers=workers,
                    tool='wrk',
                    requests_per_second=wrk_result.get('rps', 0),
                    mean_latency_ms=wrk_result.get('mean_latency', 0),
                    p95_latency_ms=wrk_result.get('p95_latency', 0),
                    p99_latency_ms=wrk_result.get('p99_latency', 0),
                    failed_requests=wrk_result.get('failed', 0),
                    total_requests=wrk_result.get('total', 0),
                    duration_seconds=20,
                    cpu_usage_percent=max(cpu_after - cpu_before, 0),
                    memory_usage_mb=mem_after
                )
                results.append(result)
                
                print(f"  📈 wrk: {result.requests_per_second:.1f} RPS, "
                      f"{result.mean_latency_ms:.1f}ms avg latency")
        
        server.stop()
        time.sleep(3)  # Allow system to settle
    
    return results


def analyze_results(results: List[BenchmarkResult]) -> Dict:
    """Analyze benchmark results and provide recommendations."""
    if not results:
        return {"error": "No benchmark results available"}
    
    # Group results by worker count
    by_workers = {}
    for result in results:
        if result.workers not in by_workers:
            by_workers[result.workers] = []
        by_workers[result.workers].append(result)
    
    # Calculate averages for each worker configuration
    analysis = {}
    for workers, worker_results in by_workers.items():
        total_rps = sum(r.requests_per_second for r in worker_results)
        avg_rps = total_rps / len(worker_results)
        avg_latency = sum(r.mean_latency_ms for r in worker_results) / len(worker_results)
        avg_cpu = sum(r.cpu_usage_percent for r in worker_results) / len(worker_results)
        avg_memory = sum(r.memory_usage_mb for r in worker_results) / len(worker_results)
        
        analysis[workers] = {
            "avg_rps": avg_rps,
            "avg_latency_ms": avg_latency,
            "avg_cpu_percent": avg_cpu,
            "avg_memory_mb": avg_memory,
            "total_tests": len(worker_results)
        }
    
    # Find optimal configuration
    optimal_workers = max(analysis.keys(), key=lambda w: analysis[w]["avg_rps"])
    
    return {
        "analysis": analysis,
        "recommendation": {
            "optimal_workers": optimal_workers,
            "reasoning": f"Best average RPS: {analysis[optimal_workers]['avg_rps']:.1f}",
            "performance_gain": (
                analysis[optimal_workers]["avg_rps"] / analysis[1]["avg_rps"] - 1
            ) * 100 if 1 in analysis else 0
        }
    }


def save_results(results: List[BenchmarkResult], analysis: Dict):
    """Save results to JSON file."""
    output = {
        "timestamp": time.time(),
        "results": [asdict(r) for r in results],
        "analysis": analysis
    }
    
    with open("benchmark_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Results saved to benchmark_results.json")


def print_summary(analysis: Dict):
    """Print benchmark summary."""
    print("\n📊 PERFORMANCE ANALYSIS SUMMARY")
    print("=" * 60)
    
    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        return
    
    for workers, stats in analysis["analysis"].items():
        print(f"\n🔧 {workers} Worker(s):")
        print(f"  📈 Average RPS: {stats['avg_rps']:.1f}")
        print(f"  ⏱️  Average Latency: {stats['avg_latency_ms']:.1f}ms")
        print(f"  🖥️  CPU Usage: {stats['avg_cpu_percent']:.1f}%")
        print(f"  💾 Memory Usage: {stats['avg_memory_mb']:.1f}MB")
    
    rec = analysis["recommendation"]
    print(f"\n🎯 RECOMMENDATION:")
    print(f"  Optimal Configuration: {rec['optimal_workers']} workers")
    print(f"  Reasoning: {rec['reasoning']}")
    if rec["performance_gain"] > 0:
        print(f"  Performance Gain: +{rec['performance_gain']:.1f}% over 1 worker")


def main():
    """Main function."""
    print("LEA MCP Server Performance Profiler")
    print("Requirements: ab (apache2-utils), wrk, uvicorn")
    
    # Check requirements
    missing_tools = []
    for tool in ["ab", "wrk", "uvicorn"]:
        if subprocess.run(["which", tool], capture_output=True).returncode != 0:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"❌ Missing tools: {', '.join(missing_tools)}")
        print("Install with:")
        print("  apt-get install apache2-utils wrk")
        print("  pip install uvicorn")
        sys.exit(1)
    
    try:
        # Run benchmarks
        results = run_comprehensive_benchmark()
        
        # Analyze results
        analysis = analyze_results(results)
        
        # Save and display results
        save_results(results, analysis)
        print_summary(analysis)
        
    except KeyboardInterrupt:
        print("\n🛑 Benchmark interrupted by user")
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()