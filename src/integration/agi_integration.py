#!/usr/bin/env python3
"""
AGI Integration Module for Living Truth Engine
Connects Living Truth Engine with main AGI system components
Migrated from living_truth_agent with LivingTruthEngine integration.

Features:
- AGI system component integration
- Cross-validation of findings
- Confidence score calculation
- Integrated insights generation
- Recommendation systems
- MCP tool integration
"""

import sys
import os
import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict

# Import LivingTruthEngine configuration and components
from src.config import get_config, config
from src.analysis.hybrid_retrieval import HybridRetriever, AdvancedSearchEngine
from src.analysis.research_analysis import ResearchAnalysisSystem
from src.analysis.notebook_agent import AdvancedNotebookAgent

# Setup logging
logger = logging.getLogger(__name__)


@dataclass
class AGIAnalysisResult:
    """Structured result for AGI analysis."""

    query: str
    analysis_type: str
    living_truth_results: Dict[str, Any]
    agi_results: Dict[str, Any]
    integrated_insights: Dict[str, Any]
    confidence_scores: Dict[str, float]
    recommendations: List[str]
    cross_validation: Dict[str, Any]
    timestamp: str


@dataclass
class AGIComponent:
    """AGI component information."""

    name: str
    status: str
    description: str
    capabilities: List[str]
    confidence: float


class AGILivingTruthIntegration:
    """
    Integration layer between Living Truth Engine and main AGI system.

    Features:
    - AGI system component integration
    - Cross-validation of findings
    - Confidence score calculation
    - Integrated insights generation
    - Recommendation systems
    - MCP tool integration
    """

    def __init__(self):
        """Initialize the AGI Living Truth Integration."""
        self.config = get_config()
        self.agi_available = False
        self.living_truth_engine = None
        self.agi_components = {}

        # Initialize Living Truth Engine components
        self._init_living_truth_engine()

        # Initialize AGI components if available
        self._init_agi_components()

        logger.info("✅ AGILivingTruthIntegration initialized successfully")

    def _init_living_truth_engine(self):
        """Initialize Living Truth Engine components."""
        try:
            self.living_truth_engine = HybridRetriever()
            self.advanced_search = AdvancedSearchEngine()
            self.research_analysis = ResearchAnalysisSystem()
            self.notebook_agent = AdvancedNotebookAgent()

            logger.info("✅ Living Truth Engine components initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Living Truth Engine: {e}")
            self.living_truth_engine = None

    def _init_agi_components(self):
        """Initialize main AGI system components (placeholder for future integration)."""  # noqa: E501
        try:
            # Placeholder AGI components for future integration
            self.agi_components = {
                "scanner": AGIComponent(
                    name="Scanner",
                    status="available",
                    description="Pattern recognition and fractal analysis",
                    capabilities=[
                        "pattern_recognition",
                        "fractal_analysis",
                        "confidence_scoring",
                    ],
                    confidence=0.85,
                ),
                "memory": AGIComponent(
                    name="Memory",
                    status="available",
                    description="Pattern storage and similarity matching",
                    capabilities=[
                        "pattern_storage",
                        "similarity_matching",
                        "knowledge_retrieval",
                    ],
                    confidence=0.90,
                ),
                "path_manager": AGIComponent(
                    name="Path Manager",
                    status="available",
                    description="Reasoning paths and adapter chains",
                    capabilities=["reasoning_paths", "adapter_chains", "optimization"],
                    confidence=0.80,
                ),
                "dreaming": AGIComponent(
                    name="Dreaming",
                    status="available",
                    description="Creative exploration and novel paths",
                    capabilities=[
                        "creative_exploration",
                        "novel_paths",
                        "insight_generation",
                    ],
                    confidence=0.75,
                ),
                "communication": AGIComponent(
                    name="Communication",
                    status="available",
                    description="Task routing and component coordination",
                    capabilities=[
                        "task_routing",
                        "component_coordination",
                        "status_management",
                    ],
                    confidence=0.88,
                ),
                "breadcrumbs": AGIComponent(
                    name="Breadcrumbs",
                    status="available",
                    description="Interaction tracking and confidence trends",
                    capabilities=[
                        "interaction_tracking",
                        "confidence_trends",
                        "audit_trail",
                    ],
                    confidence=0.92,
                ),
            }

            self.agi_available = True
            logger.info("✅ AGI components initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize AGI components: {e}")
            self.agi_available = False

    def analyze_with_agi_integration(
        self, query: str, analysis_type: str = "comprehensive"
    ) -> AGIAnalysisResult:
        """
        Perform comprehensive analysis using both Living Truth Engine and AGI system.

        Args:
            query: The query to analyze
            analysis_type: Type of analysis ("comprehensive", "biblical", "pattern", "creative")

        Returns:
            AGIAnalysisResult containing analysis results from both systems
        """  # noqa: E501
        try:
            logger.info(
                f"Starting AGI-integrated analysis: {query} (type: {analysis_type})"
            )

            # Living Truth Engine Analysis
            lt_results = {}
            if self.living_truth_engine:
                lt_results = self._living_truth_analysis(query, analysis_type)

            # AGI System Analysis
            agi_results = {}
            if self.agi_available:
                agi_results = self._agi_system_analysis(query, analysis_type)

            # Integrate insights
            integrated_insights = self._integrate_insights(lt_results, agi_results)

            # Cross-validate findings
            cross_validation = self._cross_validate_findings(lt_results, agi_results)

            # Calculate confidence scores
            confidence_scores = self._calculate_integrated_confidence(
                {
                    "living_truth_engine": lt_results,
                    "agi_system": agi_results,
                    "integrated_insights": integrated_insights,
                    "cross_validation": cross_validation,
                }
            )

            # Generate recommendations
            recommendations = self._generate_recommendations(
                {
                    "living_truth_engine": lt_results,
                    "agi_system": agi_results,
                    "integrated_insights": integrated_insights,
                    "confidence_scores": confidence_scores,
                }
            )

            # Create result
            result = AGIAnalysisResult(
                query=query,
                analysis_type=analysis_type,
                living_truth_results=lt_results,
                agi_results=agi_results,
                integrated_insights=integrated_insights,
                confidence_scores=confidence_scores,
                recommendations=recommendations,
                cross_validation=cross_validation,
                timestamp=self._get_timestamp(),
            )

            logger.info("✅ AGI-integrated analysis completed successfully")
            return result

        except Exception as e:
            logger.error(f"❌ AGI-integrated analysis failed: {e}")
            raise

    def _living_truth_analysis(self, query: str, analysis_type: str) -> Dict[str, Any]:
        """Perform Living Truth Engine analysis."""
        try:
            results = {
                "hybrid_retrieval": {},
                "advanced_search": {},
                "research_analysis": {},
                "notebook_agent": {},
            }

            # Hybrid retrieval analysis
            if self.living_truth_engine:
                results["hybrid_retrieval"] = {
                    "biblical_evidence": self.living_truth_engine.search_biblical_evidence(  # noqa: E501
                        query
                    ),
                    "survivor_testimonies": self.living_truth_engine.search_survivor_testimonies(  # noqa: E501
                        query
                    ),
                    "elite_networks": self.living_truth_engine.search_elite_networks(
                        query
                    ),
                    "temporal_patterns": self.living_truth_engine.search_temporal_patterns(  # noqa: E501
                        query
                    ),
                }

            # Advanced search analysis
            if hasattr(self, "advanced_search"):
                results["advanced_search"] = {
                    "biblical_search": self.advanced_search.biblical_evidence_search(
                        query
                    ),
                    "survivor_search": self.advanced_search.survivor_testimony_search(
                        query
                    ),
                    "network_search": self.advanced_search.elite_network_search(query),
                    "temporal_search": self.advanced_search.temporal_pattern_search(
                        query
                    ),
                }

            # Research analysis
            if hasattr(self, "research_analysis"):
                results["research_analysis"] = {
                    "claims": self.research_analysis.extract_claims_from_transcript(
                        {"text": query}
                    ),
                    "entities": self.research_analysis.extract_entities_from_text(
                        query
                    ),
                    "relationships": self.research_analysis.build_entity_network(),
                }

            # Notebook agent analysis
            if hasattr(self, "notebook_agent"):
                results["notebook_agent"] = {
                    "query_processing": self.notebook_agent.process_query(query),
                    "study_guide": self.notebook_agent._generate_study_guide(),
                    "document_summary": self.notebook_agent._summarize_documents(),
                }

            return results

        except Exception as e:
            logger.error(f"Living Truth Engine analysis error: {e}")
            return {"error": str(e)}

    def _agi_system_analysis(self, query: str, analysis_type: str) -> Dict[str, Any]:
        """Perform AGI system analysis."""
        try:
            results = {}

            for component_name, component in self.agi_components.items():
                if component.status == "available":
                    results[component_name] = {
                        "capabilities": component.capabilities,
                        "confidence": component.confidence,
                        "analysis": self._simulate_agi_component_analysis(
                            component, query, analysis_type
                        ),
                    }

            return results

        except Exception as e:
            logger.error(f"AGI system analysis error: {e}")
            return {"error": str(e)}

    def _simulate_agi_component_analysis(
        self, component: AGIComponent, query: str, analysis_type: str
    ) -> Dict[str, Any]:
        """Simulate AGI component analysis (placeholder for future integration)."""
        try:
            # Placeholder analysis based on component capabilities
            analysis = {
                "input_query": query,
                "analysis_type": analysis_type,
                "component_capabilities": component.capabilities,
                "confidence_score": component.confidence,
                "patterns_detected": [],
                "insights_generated": [],
                "recommendations": [],
            }

            # Simulate different analysis types
            if analysis_type == "biblical":
                analysis["patterns_detected"] = [
                    "biblical_references",
                    "theological_patterns",
                ]
                analysis["insights_generated"] = [
                    "spiritual_significance",
                    "moral_implications",
                ]
            elif analysis_type == "pattern":
                analysis["patterns_detected"] = [
                    "behavioral_patterns",
                    "temporal_patterns",
                ]
                analysis["insights_generated"] = ["trend_analysis", "prediction_models"]
            elif analysis_type == "creative":
                analysis["patterns_detected"] = [
                    "creative_patterns",
                    "innovation_patterns",
                ]
                analysis["insights_generated"] = [
                    "creative_solutions",
                    "novel_approaches",
                ]
            else:  # comprehensive
                analysis["patterns_detected"] = [
                    "multi_dimensional_patterns",
                    "integrated_patterns",
                ]
                analysis["insights_generated"] = [
                    "comprehensive_insights",
                    "holistic_understanding",
                ]

            return analysis

        except Exception as e:
            logger.error(f"AGI component analysis simulation error: {e}")
            return {"error": str(e)}

    def _integrate_insights(
        self, lt_results: Dict[str, Any], agi_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Integrate insights from both systems."""
        try:
            integrated_insights = {
                "combined_patterns": [],
                "enhanced_insights": [],
                "cross_system_validation": {},
                "synthesis_analysis": {},
            }

            # Combine patterns from both systems
            if "research_analysis" in lt_results:
                lt_patterns = lt_results["research_analysis"].get("claims", [])
                integrated_insights["combined_patterns"].extend(lt_patterns)

            if agi_results:
                for component_name, component_data in agi_results.items():
                    if "analysis" in component_data:
                        agi_patterns = component_data["analysis"].get(
                            "patterns_detected", []
                        )
                        integrated_insights["combined_patterns"].extend(agi_patterns)

            # Enhance insights through cross-system analysis
            integrated_insights["enhanced_insights"] = [
                "Multi-system pattern recognition enhances accuracy",
                "Cross-validation improves confidence in findings",
                "Integrated analysis provides comprehensive understanding",
            ]

            # Cross-system validation
            integrated_insights["cross_system_validation"] = {
                "living_truth_engine_available": bool(lt_results),
                "agi_system_available": bool(agi_results),
                "integration_success": bool(lt_results and agi_results),
            }

            # Synthesis analysis
            integrated_insights["synthesis_analysis"] = {
                "total_patterns": len(integrated_insights["combined_patterns"]),
                "total_insights": len(integrated_insights["enhanced_insights"]),
                "integration_quality": "high"
                if bool(lt_results and agi_results)
                else "partial",
            }

            return integrated_insights

        except Exception as e:
            logger.error(f"Insight integration error: {e}")
            return {"error": str(e)}

    def _cross_validate_findings(
        self, lt_results: Dict[str, Any], agi_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cross-validate findings between systems."""
        try:
            validation = {
                "validation_status": "success",
                "confidence_boost": 0.0,
                "conflicting_findings": [],
                "corroborated_findings": [],
                "validation_score": 0.0,
            }

            # Check for corroborated findings
            lt_patterns = set()
            if "research_analysis" in lt_results:
                claims = lt_results["research_analysis"].get("claims", [])
                for claim in claims:
                    if hasattr(claim, "text"):
                        lt_patterns.add(claim.text)

            agi_patterns = set()
            if agi_results:
                for component_data in agi_results.values():
                    if "analysis" in component_data:
                        patterns = component_data["analysis"].get(
                            "patterns_detected", []
                        )
                        agi_patterns.update(patterns)

            # Find corroborated patterns
            corroborated = lt_patterns.intersection(agi_patterns)
            validation["corroborated_findings"] = list(corroborated)

            # Calculate validation score
            total_patterns = len(lt_patterns.union(agi_patterns))
            if total_patterns > 0:
                validation["validation_score"] = len(corroborated) / total_patterns
                validation["confidence_boost"] = validation["validation_score"] * 0.2

            return validation

        except Exception as e:
            logger.error(f"Cross-validation error: {e}")
            return {"error": str(e)}

    def _calculate_integrated_confidence(
        self, results: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate integrated confidence scores."""
        try:
            confidence_scores = {
                "living_truth_engine": 0.0,
                "agi_system": 0.0,
                "integrated_analysis": 0.0,
                "cross_validation": 0.0,
                "overall_confidence": 0.0,
            }

            # Living Truth Engine confidence
            if results.get("living_truth_engine"):
                confidence_scores["living_truth_engine"] = 0.85

            # AGI system confidence
            if results.get("agi_system"):
                agi_components = results["agi_system"]
                total_confidence = sum(
                    component.get("confidence", 0.0)
                    for component in agi_components.values()
                )
                confidence_scores["agi_system"] = (
                    total_confidence / len(agi_components) if agi_components else 0.0
                )

            # Cross-validation confidence
            if results.get("cross_validation"):
                validation_score = results["cross_validation"].get(
                    "validation_score", 0.0
                )
                confidence_scores["cross_validation"] = validation_score

            # Integrated analysis confidence
            if results.get("integrated_insights"):
                integration_quality = (
                    results["integrated_insights"]
                    .get("synthesis_analysis", {})
                    .get("integration_quality", "partial")
                )
                confidence_scores["integrated_analysis"] = (
                    0.9 if integration_quality == "high" else 0.7
                )

            # Overall confidence (weighted average)
            weights = {
                "living_truth_engine": 0.3,
                "agi_system": 0.3,
                "integrated_analysis": 0.2,
                "cross_validation": 0.2,
            }

            overall_confidence = sum(
                confidence_scores[key] * weights[key] for key in weights.keys()
            )
            confidence_scores["overall_confidence"] = overall_confidence

            return confidence_scores

        except Exception as e:
            logger.error(f"Confidence calculation error: {e}")
            return {"error": str(e)}

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis results."""
        try:
            recommendations = []

            # Base recommendations
            recommendations.append("Continue monitoring for pattern evolution")
            recommendations.append("Validate findings through multiple sources")
            recommendations.append(
                "Consider temporal analysis for trend identification"
            )

            # Confidence-based recommendations
            confidence_scores = results.get("confidence_scores", {})
            overall_confidence = confidence_scores.get("overall_confidence", 0.0)

            if overall_confidence > 0.8:
                recommendations.append(
                    "High confidence in findings - proceed with action"
                )
                recommendations.append(
                    "Consider advanced pattern analysis for deeper insights"
                )
            elif overall_confidence > 0.6:
                recommendations.append(
                    "Moderate confidence - additional validation recommended"
                )
                recommendations.append("Expand analysis scope for better understanding")
            else:
                recommendations.append("Low confidence - extensive validation required")
                recommendations.append("Consider alternative analysis approaches")

            # Cross-validation recommendations
            cross_validation = results.get("cross_validation", {})
            validation_score = cross_validation.get("validation_score", 0.0)

            if validation_score > 0.7:
                recommendations.append(
                    "Strong cross-validation - findings are reliable"
                )
            elif validation_score > 0.4:
                recommendations.append("Partial cross-validation - mixed reliability")
            else:
                recommendations.append(
                    "Weak cross-validation - findings need verification"
                )

            return recommendations

        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
            return ["Error generating recommendations"]

    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis results."""
        from datetime import datetime

        return datetime.now().isoformat()

    def get_agi_components_status(self) -> Dict[str, Any]:
        """Get status of all AGI components."""
        try:
            status = {
                "agi_available": self.agi_available,
                "components": {},
                "overall_status": "operational"
                if self.agi_available
                else "unavailable",
            }

            for component_name, component in self.agi_components.items():
                status["components"][component_name] = {
                    "status": component.status,
                    "confidence": component.confidence,
                    "capabilities": component.capabilities,
                }

            return status

        except Exception as e:
            logger.error(f"AGI components status error: {e}")
            return {"error": str(e)}

    def get_integration_status(self) -> Dict[str, Any]:
        """Get overall integration status."""
        try:
            status = {
                "living_truth_engine": {
                    "available": bool(self.living_truth_engine),
                    "components": [
                        "hybrid_retriever",
                        "advanced_search",
                        "research_analysis",
                        "notebook_agent",
                    ],
                },
                "agi_system": {
                    "available": self.agi_available,
                    "components": list(self.agi_components.keys()),
                },
                "integration_quality": "high"
                if (self.living_truth_engine and self.agi_available)
                else "partial",
                "total_components": len(self.agi_components)
                + 4,  # 4 Living Truth Engine components
            }

            return status

        except Exception as e:
            logger.error(f"Integration status error: {e}")
            return {"error": str(e)}

    def cross_validate_findings(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Cross-validate findings from multiple sources.

        Args:
            findings: List of findings to validate

        Returns:
            Dictionary with validation results
        """
        try:
            logger.info(f"Cross-validating {len(findings)} findings")

            validation_results = {
                "total_findings": len(findings),
                "validated_findings": 0,
                "validation_errors": 0,
                "confidence_scores": [],
                "cross_references": [],
                "validation_summary": {},
            }

            for i, finding in enumerate(findings):
                try:
                    # Extract key information from finding
                    finding_id = finding.get("id", f"finding_{i}")
                    finding_type = finding.get("type", "unknown")
                    finding_confidence = finding.get("confidence", 0.0)
                    finding_source = finding.get("source", "unknown")

                    # Perform cross-validation logic
                    validation_score = self._validate_single_finding(finding)

                    # Record validation results
                    validation_results["validated_findings"] += 1
                    validation_results["confidence_scores"].append(
                        {
                            "finding_id": finding_id,
                            "original_confidence": finding_confidence,
                            "validation_score": validation_score,
                            "final_confidence": (finding_confidence + validation_score)
                            / 2,
                        }
                    )

                    # Check for cross-references
                    cross_refs = self._find_cross_references(finding, findings)
                    if cross_refs:
                        validation_results["cross_references"].append(
                            {"finding_id": finding_id, "cross_references": cross_refs}
                        )

                except Exception as e:
                    logger.error(f"Error validating finding {i}: {e}")
                    validation_results["validation_errors"] += 1

            # Generate validation summary
            validation_results["validation_summary"] = {
                "success_rate": validation_results["validated_findings"]
                / validation_results["total_findings"]
                if validation_results["total_findings"] > 0
                else 0,
                "average_confidence": sum(
                    [
                        score["final_confidence"]
                        for score in validation_results["confidence_scores"]
                    ]
                )
                / len(validation_results["confidence_scores"])
                if validation_results["confidence_scores"]
                else 0,
                "cross_reference_count": len(validation_results["cross_references"]),
            }

            logger.info(
                f"✅ Cross-validation completed: {validation_results['validated_findings']}/{validation_results['total_findings']} findings validated"  # noqa: E501
            )
            return validation_results

        except Exception as e:
            logger.error(f"Error in cross-validation: {e}")
            return {"error": str(e)}

    def _validate_single_finding(self, finding: Dict[str, Any]) -> float:
        """Validate a single finding and return validation score."""
        try:
            # Basic validation logic
            validation_score = 0.0

            # Check for required fields
            required_fields = ["id", "type", "confidence", "source"]
            for field in required_fields:
                if field in finding:
                    validation_score += 0.25

            # Check confidence range
            confidence = finding.get("confidence", 0.0)
            if 0.0 <= confidence <= 1.0:
                validation_score += 0.25

            # Check for supporting evidence
            if finding.get("evidence"):
                validation_score += 0.25

            # Check for timestamp
            if finding.get("timestamp"):
                validation_score += 0.25

            return validation_score

        except Exception as e:
            logger.error(f"Error validating single finding: {e}")
            return 0.0

    def _find_cross_references(
        self, finding: Dict[str, Any], all_findings: List[Dict[str, Any]]
    ) -> List[str]:
        """Find cross-references for a finding."""
        try:
            cross_refs = []
            finding_id = finding.get("id", "")
            finding_type = finding.get("type", "")

            for other_finding in all_findings:
                if other_finding.get("id") == finding_id:
                    continue

                # Check for type similarity
                if other_finding.get("type") == finding_type:
                    cross_refs.append(other_finding.get("id", ""))

                # Check for source similarity
                if other_finding.get("source") == finding.get("source"):
                    cross_refs.append(other_finding.get("id", ""))

            return list(set(cross_refs))  # Remove duplicates

        except Exception as e:
            logger.error(f"Error finding cross-references: {e}")
            return []

    def calculate_confidence_scores(self, results: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate confidence scores for analysis results.

        Args:
            results: Dictionary containing analysis results

        Returns:
            Dictionary with confidence scores
        """
        try:
            logger.info("Calculating confidence scores for analysis results")

            # Use the existing integrated confidence calculation
            confidence_scores = self._calculate_integrated_confidence(results)

            # Add additional confidence metrics if needed
            if isinstance(confidence_scores, dict) and "error" not in confidence_scores:
                # Add component-specific confidence scores
                confidence_scores["component_breakdown"] = {
                    "living_truth_engine": confidence_scores.get(
                        "living_truth_engine", 0.0
                    ),
                    "agi_system": confidence_scores.get("agi_system", 0.0),
                    "integrated_analysis": confidence_scores.get(
                        "integrated_analysis", 0.0
                    ),
                    "cross_validation": confidence_scores.get("cross_validation", 0.0),
                }

                # Add confidence level classification
                overall_confidence = confidence_scores.get("overall_confidence", 0.0)
                if overall_confidence >= 0.8:
                    confidence_scores["confidence_level"] = "high"
                elif overall_confidence >= 0.6:
                    confidence_scores["confidence_level"] = "medium"
                else:
                    confidence_scores["confidence_level"] = "low"

                logger.info(
                    f"✅ Confidence scores calculated: {confidence_scores['confidence_level']} confidence"  # noqa: E501
                )

            return confidence_scores

        except Exception as e:
            logger.error(f"Error calculating confidence scores: {e}")
            return {"error": str(e)}

    def close(self):
        """Clean up resources."""
        try:
            # Clean up Living Truth Engine components
            if self.living_truth_engine:
                # Add cleanup logic if needed
                pass

            # Clean up AGI components
            self.agi_components.clear()

            logger.info("✅ AGI integration resources cleaned up")

        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")


def main():
    """Main function for testing the AGI integration."""
    try:
        # Initialize integration
        integration = AGILivingTruthIntegration()

        # Test analysis
        result = integration.analyze_with_agi_integration(
            query="Analyze patterns in survivor testimony",
            analysis_type="comprehensive",
        )

        # Print results
        print(f"Analysis completed: {result.query}")
        print(
            f"Overall confidence: {result.confidence_scores.get('overall_confidence', 0.0):.2f}"  # noqa: E501
        )
        print(f"Recommendations: {len(result.recommendations)}")

        # Get status
        status = integration.get_integration_status()
        print(f"Integration status: {status}")

    except Exception as e:
        logger.error(f"Main function error: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
