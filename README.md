# Project Aegis — 企業級雲端前後端隔離與自動化運維架構實作

本專案實作了一套基於 AWS 的**非對稱式雲端安全隔離架構**。透過將核心應用服務（FastAPI）安置於完全不接觸外網的私有子網路（Private Subnet），並透過自建 NAT 實例與公有負載平衡器（ALB）實現極致的安全隔離與自動化運維監控閉環。

---

## 系統架構圖 (Architecture)

>  本架構圖使用 Mermaid 語法繪製，GitHub 將自動渲染。

```mermaid
graph TD
    User((使用者)) -->|HTTP Port 80| ALB[Aegis-Public-ALB]
    
    subgraph AWS_Cloud [AWS Tokyo Region]
        subgraph VPC [VPC: 10.0.0.0/16]
            
            subgraph Public_Subnet [Public Subnet: 10.0.1.0/24]
                ALB
                NAT[Aegis-NAT-Instance]
            end
            
            subgraph Private_Subnet [Private Subnet: 10.0.2.0/24]
                App[Aegis-App-Server <br> 10.0.2.x]
                Docker[Docker Container: <br> FastAPI aegis-web]
                App --- Docker
            end
            
        end
        
        CloudWatch[Amazon CloudWatch]
        SNS[Amazon SNS: Email Alert]
    end

    %% 流量流向
    ALB -->|安全組閉環僅允許 ALB 流量| App
    App -->|出站路由 0.0.0.0/0| NAT
    NAT -->|網路轉發| IGW((Internet Gateway))
    
    %% 監控流向
    App -.->|CPU Utilization 監控| CloudWatch
    CloudWatch -.->|CPU >= 60% 觸發警報| SNS
