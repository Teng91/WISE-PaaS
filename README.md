# 產學計畫-研華股份有限公司與臺灣大學生農學院
- 相關資料: https://hackmd.io/@bhIA534oS4WfxIHxC2EFfA/r1WMd493j/%2FuLrh41wxQSyjc2ASdNxXQg
## 程式碼功能概述
1. EdgeAgent 初始化與連線
   - 使用 EdgeAgentOptions 和 DCCSOptions 配置 EdgeAgent，並連接到 Advantech 的 WISE-PaaS 平台
   - 透過 credentialKey 和 apiUrl 驗證連線
2. 數據讀取與處理
   - 從多個 CSV 檔案中讀取環境數據（如溫度、濕度、光照）和害蟲數據
   - 根據感測器類型，將數據轉換為適合上傳的格式，並附上時間戳記
3. 數據上傳
   - 將處理後的數據封裝為 EdgeData，並透過 EdgeAgent 的 sendData 方法上傳到雲端
4. 定時執行
   - 使用無窮迴圈，每隔 5 秒執行一次數據讀取與上傳
## 程式碼關鍵技術
1. Advantech WISE-PaaS SDK
   - 使用 wisepaasdatahubedgesdk 套件來與 WISE-PaaS 平台進行互動
   - 透過 EdgeAgent 和 EdgeTag 將數據封裝並上傳
2. HTTP 請求
   - 使用 requests 套件向遠端伺服器發送 HTTP GET 請求，取得資料庫數量（getNumberOfDbs 函數）
3. 資料處理
   - 使用 pandas 讀取和處理 CSV 檔案中的數據
   - 將數據轉換為適合上傳的格式（例如，時間戳記格式化、數據類型轉換）
4. 時間處理
   - 使用 datetime 模組處理時間戳，確保數據的時間格式符合要求
5. 無窮迴圈與延遲
   - 使用 while 迴圈和 time.sleep 實現定時執行
