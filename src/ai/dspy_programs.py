import dspy
from typing import List, Dict, Any

class CorroborationProgram(dspy.Module):
    def __init__(self, llm):
        super().__init__()
        self.verify = dspy.ChainOfThought(llm=llm)
    
    def forward(self, claim: str, snippets: List[str]) -> Dict[str, Any]:
        prompt = f"Claim: {claim}\nEvidence:\n" + "\n".join(snippets)
        return {"analysis": self.verify(prompt)}

class ClaimVerificationProgram(dspy.Module):
    def __init__(self, llm):
        super().__init__()
        self.verify = dspy.ChainOfThought(llm=llm)
    
    def forward(self, claim: str, evidence: List[str]) -> Dict[str, Any]:
        prompt = f"Verify this claim: {claim}\nEvidence:\n" + "\n".join(evidence)
        return {"verification": self.verify(prompt)}

class EntityLinkingProgram(dspy.Module):
    def __init__(self, llm):
        super().__init__()
        self.link = dspy.ChainOfThought(llm=llm)
    
    def forward(self, entities: List[str], context: str) -> Dict[str, Any]:
        prompt = f"Link these entities: {entities}\nContext: {context}"
        return {"links": self.link(prompt)}
