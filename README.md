# FastAPI MCP Server

FastAPI ile HTTP üzerinden çalışan basit bir Model Context Protocol (MCP)
server geliştirme projesidir. Proje, MCP'nin temel parçalarını öğrenmek amacıyla
adım adım oluşturulmuştur.

Uygulama şu anda:

- FastAPI üzerinden bir sağlık kontrolü endpoint'i sunar.
- MCP server'ı `/mcp/` adresinde Streamable HTTP ile yayınlar.
- `add` isimli örnek bir MCP tool'u sağlar.
- MCP bağlantısını ve tool çağrısını gösteren örnek bir Python istemcisi içerir.

## Kullanılan Teknolojiler

- Python 3.14+
- FastAPI
- MCP Python SDK
- Uvicorn
- uv

## Proje Yapısı

```text
FastAPI_MCP_Server/
|-- src/
|   `-- fastapi_mcp_server/
|       |-- __init__.py
|       |-- main.py
|       |-- mcp_server.py
|       `-- client.py
|-- .python-version
|-- pyproject.toml
|-- uv.lock
`-- README.md
```

- `main.py`: FastAPI uygulamasını oluşturur ve MCP uygulamasını `/mcp` yoluna bağlar.
- `mcp_server.py`: MCP server nesnesini ve sunulan tool'ları tanımlar.
- `client.py`: MCP server'a bağlanan örnek istemciyi içerir.
- `pyproject.toml`: Proje bilgilerini ve bağımlılıkları tanımlar.
- `uv.lock`: Bağımlılıkların çözümlenmiş sürümlerini sabitler.

## Kurulum

Proje dizininde bağımlılıkları kurun:

```powershell
uv sync
```

`uv`, proje için `.venv` sanal ortamını oluşturur ve `pyproject.toml` içinde
tanımlanan bağımlılıkları kurar.

## Server'ı Çalıştırma

```powershell
uv run uvicorn fastapi_mcp_server.main:app --reload
```

Server varsayılan olarak aşağıdaki adreste çalışır:

```text
http://127.0.0.1:8000
```

`--reload` seçeneği, kaynak kod değiştiğinde geliştirme server'ını otomatik
olarak yeniden başlatır.

## HTTP Endpoint'leri

| Yöntem | Adres | Açıklama |
| --- | --- | --- |
| `GET` | `/health` | Uygulamanın çalıştığını doğrular. |
| MCP | `/mcp/` | MCP Streamable HTTP bağlantı noktasıdır. |
| `GET` | `/docs` | FastAPI Swagger arayüzünü açar. |

Sağlık kontrolü:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Beklenen cevap:

```json
{
  "status": "ok"
}
```

## MCP Tool'u

Server şu anda `add` isimli bir tool sunar:

```python
@mcp.tool()
def add(x: int, y: int) -> int:
    """Add two numbers together."""
    return x + y
```

MCP SDK; fonksiyon adını, type hint'leri ve docstring'i kullanarak tool'un adını,
açıklamasını ve JSON giriş şemasını oluşturur.

## Örnek MCP İstemcisi

Önce Uvicorn server'ının çalıştığından emin olun. Ardından ikinci bir terminalde:

```powershell
uv run python -m fastapi_mcp_server.client
```

Beklenen çıktı:

```text
Tools: ['add']
Result: 8
```

İstemcinin gerçekleştirdiği işlemler:

1. `/mcp/` adresine Streamable HTTP bağlantısı kurar.
2. `ClientSession` oluşturur.
3. `initialize` ile MCP oturumunu başlatır.
4. `list_tools` ile mevcut tool'ları keşfeder.
5. `call_tool` ile `add` tool'unu çağırır.
6. Server'ın döndürdüğü sonucu ekrana yazdırır.

## FastAPI ve MCP Birlikte Nasıl Çalışıyor?

```text
MCP Client
    |
    | Streamable HTTP
    v
FastAPI /mcp/
    |
    v
MCP Server
    |
    v
add(x, y)
```

MCP uygulaması bağımsız bir ASGI uygulamasına dönüştürülür ve FastAPI içerisine
mount edilir. FastAPI lifespan mekanizması, uygulama açık olduğu sürece MCP
session manager'ın çalışmasını sağlar.

## `Missing session ID` Mesajı

Tarayıcıda doğrudan `http://127.0.0.1:8000/mcp/` adresini açarsanız şu hatayı
görebilirsiniz:

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "error": {
    "code": -32600,
    "message": "Bad Request: Missing session ID"
  }
}
```

Bu, endpoint'in bozuk olduğu anlamına gelmez. Tarayıcı bir MCP istemcisi değildir
ve gerekli başlangıç görüşmesini yapmadan normal HTTP isteği gönderir. MCP
endpoint'i `ClientSession` gibi protokolü uygulayan bir istemciyle kullanılmalıdır.

## VS Code'a MCP Server Ekleme

VS Code, Streamable HTTP üzerinden çalışan MCP server'lara bağlanabilir. Önce
Uvicorn server'ını çalıştırın:

```powershell
uv run uvicorn fastapi_mcp_server.main:app --reload
```

Ardından proje kökünde `.vscode/mcp.json` dosyasını oluşturun:

```json
{
  "servers": {
    "fastapiMcpServer": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp/"
    }
  }
}
```

VS Code içinde bağlantıyı etkinleştirmek için:

1. `Ctrl+Shift+P` ile Command Palette'i açın.
2. `MCP: List Servers` komutunu çalıştırın.
3. `fastapiMcpServer` server'ını seçin.
4. Gerekirse `Start` veya `Restart` komutunu çalıştırın.
5. Chat görünümündeki tool seçiminden `add` aracını etkinleştirin.

Agent modunda örnek kullanım:

```text
MCP add aracını kullanarak 18 ile 24'ü topla.
```

HTTP yapılandırması yalnızca VS Code'un çalışan server'a bağlanmasını sağlar;
Uvicorn sürecini otomatik olarak başlatmaz. Bu nedenle geliştirme sırasında
Uvicorn ayrı bir terminalde açık kalmalıdır.

VS Code bir Dev Container, WSL veya SSH oturumu içinde çalışıyorsa
`127.0.0.1`, yerel Windows makinesini değil ilgili uzak ortamı ifade edebilir.
Bu durumda server adresinin o ortamdan erişilebilir olması gerekir.

Daha fazla bilgi için [VS Code MCP yapılandırma referansına](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)
bakabilirsiniz.

## MCP Akışı

```text
initialize -> tools/list -> tools/call -> result
```

- `initialize`: İstemci ve server arasında MCP oturumunu başlatır.
- `tools/list`: Server'ın sunduğu tool'ları ve giriş şemalarını getirir.
- `tools/call`: Seçilen tool'u verilen argümanlarla çalıştırır.
- `result`: Tool'un metinsel veya yapılandırılmış sonucunu döndürür.
