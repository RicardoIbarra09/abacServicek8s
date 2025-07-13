# xolo_client/client.py

import httpx
from typing import List, Optional, Dict, Any
from config.settings import settings

class XoloPolicyClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.api_base_url
        self.client = httpx.Client(base_url=self.base_url)

    def list_policies(self) -> List[Dict[str, Any]]:
        return self.client.get("/api/v4/policies/").json()

    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        return self.client.get(f"/api/v4/policies/{policy_id}").json()

    def create_policies(self, policies: List[dict]) -> Dict[str, Any]:
        return self.client.post("/api/v4/policies/", json=policies).json()

    def delete_policy(self, policy_id: str) -> Dict[str, Any]:
        return self.client.delete(f"/api/v4/policies/{policy_id}").json()

    def update_policy(self, policy_id: str, updated_policy: dict) -> Dict[str, Any]:
        return self.client.put(f"/api/v4/policies/{policy_id}", json=updated_policy).json()

    def prepare_communities(self) -> Dict[str, Any]:
        return self.client.post("/api/v4/policies/prepare").json()

    def evaluate_request(self, access_request: dict) -> Dict[str, Any]:
        return self.client.post("/api/v4/policies/evaluate", json=access_request).json()

    def evaluate_batch_requests(self, access_requests: List[dict]) -> List[Dict[str, Any]]:
        return self.client.post("/api/v4/policies/evaluate/batch", json=access_requests).json()

    def inject_policy(self, policy: dict) -> Dict[str, Any]:
        return self.client.post("/api/v4/policies/inject", json=policy).json()
