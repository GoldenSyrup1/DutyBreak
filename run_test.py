import subprocess, sys, time, asyncio, httpx, os

BASE_URL = "http://127.0.0.1:8000"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(PROJECT_ROOT, "backend", "venv", "Scripts", "python.exe")

TEST_CASES = [
    {"name": "Li-ion batteries CN -> DE", "payload": {"product_description": "Lithium-ion battery packs for electric bicycles", "origin_country": "CN", "destination_country": "DE"}},
    {"name": "Ceramic kitchenware VN -> US", "payload": {"product_description": "Ceramic kitchenware including plates bowls and cups", "origin_country": "VN", "destination_country": "US"}},
    {"name": "Sanctioned route IR -> US", "payload": {"product_description": "Industrial steel pipes", "origin_country": "IR", "destination_country": "US"}},
]

def start_server():
    print("Starting DutyBreak server...")
    log = open(os.path.join(PROJECT_ROOT, "server.log"), "w")
    proc = subprocess.Popen(
        [VENV_PYTHON, "-m", "uvicorn", "backend.main:app", "--port", "8000"],
        cwd=PROJECT_ROOT, stdout=log, stderr=log,
    )
    for i in range(20):
        time.sleep(1)
        try:
            import urllib.request
            urllib.request.urlopen(f"{BASE_URL}/health")
            print("Server ready.")
            return proc
        except:
            print(f"  Waiting... ({i+1}/20)")
    print("Server failed to start. Check server.log for details.")
    proc.kill()
    sys.exit(1)

def print_brief(brief):
    print(f"  HS Code:      {brief.get('hs_code','N/A')}")
    print(f"  Overall Risk: {brief.get('overall_risk','N/A')}")
    print(f"  Summary:      {brief.get('summary','N/A')}")
    t = brief.get("tariff", {})
    print(f"  MFN Rate:     {t.get('mfn_rate','N/A')} | Agreement: {t.get('trade_agreement','N/A')}")
    s = brief.get("sanctions", {})
    print(f"  Sanctions:    {s.get('risk_level','N/A')} — {s.get('recommended_action','N/A')}")
    for item in brief.get("action_items", [])[:3]:
        print(f"    {item}")

async def run_tests():
    async with httpx.AsyncClient() as client:
        for test in TEST_CASES:
            print(f"\n{'='*60}\nTEST: {test['name']}\n{'='*60}")
            try:
                resp = await client.post(f"{BASE_URL}/api/compliance/check", json=test["payload"], timeout=120)
                data = resp.json()
                if data.get("errors"):
                    print(f"  ERRORS: {data['errors']}")
                if data.get("brief"):
                    print("  STATUS: PASS")
                    print_brief(data["brief"])
                else:
                    print("  STATUS: FAIL — empty brief")
            except Exception as e:
                print(f"  ERROR: {e}")

def main():
    print("="*60)
    print("  DutyBreak — Full Pipeline Test")
    print("="*60)
    server = start_server()
    try:
        asyncio.run(run_tests())
    finally:
        print("\nShutting down server...")
        server.kill()
        print("Done.")

if __name__ == "__main__":
    main()