cat << 'EOF' > app.py
from fastapi import FastAPI
import uvicorn
import time

app = FastAPI(title="Project Aegis 維運監控微服務")

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Aegis App Server 運作正常！"}

@app.get("/cpu-burn")
def burn_cpu(duration: int = 15):
    """故意消耗 CPU 資源的端點，用來模擬線上故障，測試之後的 CloudWatch 告警"""
    start_time = time.time()
    print(f" 開始壓測 CPU，預計持續 {duration} 秒...")
    while time.time() - start_time < duration:
        _ = 10000 * 10000  
    return {"message": f" CPU 壓測完成，持續了 {duration} 秒！"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
EOF
