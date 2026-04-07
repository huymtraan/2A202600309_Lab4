# Setup môi trường AI agent DeepSeek

## Kích hoạt virtual environment

Mac/Linux:
```bash
source venv/bin/activate
```

Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

## Điền file .env

Thêm dòng sau vào file `.env`:
```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

## Chạy kiểm tra kết nối

```bash
python test_api.py
```
