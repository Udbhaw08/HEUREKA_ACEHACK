
import asyncio
import httpx
import json

async def test_github_agent(url: str):
    print(f"🚀 Triggering GitHub Agent for: {url}")
    
    payload = {"github_url": url}
    endpoint = "http://localhost:8005/scrape"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            print("\n✅ GitHub Agent Response:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"❌ Failed to trigger GitHub agent: {e}")

if __name__ == "__main__":
    github_url = "https://github.com/Udbhaw08"
    asyncio.run(test_github_agent(github_url))
