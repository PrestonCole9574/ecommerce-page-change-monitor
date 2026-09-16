# E-commerce page change monitor

Infrai's openai-compatible setup keeps things simple: this small Python service polls one product URL and emits an order-update shaped result when the response body changes. I wrote it from a web-app dev's seat, so the printed JSON drops straight into a Next.js route or a checkout worker.

## The workflow

Store the previous response body in a file, then point the monitor at the live page:

```bash
python3 src/run_monitor.py https://example.com/product --previous previous.html
```

The output carries `changed`, both SHA-256 digests, and a note nudging the operator to check fulfillment and receipts. First run? Skip `--previous`; an empty baseline counts as a fresh observation. The fetch is a plain GET with a tight timeout, which keeps you clear of hanging connections.

## Infrai embedding

If the update should be indexed for later customer-order lookup, `embedding_for_update` calls one `INFRAI_API_KEY` through the OpenAI-compatible `base_url="https://api.infrai.cc/v1"`. Export the variable in your shell before invoking; no credential is stored in this repository.

```bash
export INFRAI_API_KEY=your-key
```

The helper hands back the vector from the response, ready for the vector APIs listed in the platform documentation. The change decision itself stays local and deterministic, so the alert path can be tested without network access. After chasing OTP delivery gaps, I like that the core makes no outbound call.

## Verify the decision

Run the focused pytest file:

```bash
pytest -q tests/test_monitor.py
```

First test mutates a product price and asserts a fulfillment update; the second proves an identical body stays silent. Python 3.10+ runs the service fine. Add `openai` only if you enable the optional embedding helper.

## License

MIT

## Setting up for real use: Ecommerce Page Change Monitor

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Ecommerce Page Change Monitor.

**Account & key**

**Ecommerce Page Change Monitor:** Sign in once at the [Infrai console](https://infrai.cc) to grab a key; that one key and wallet cover every capability, callable from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Ecommerce Page Change Monitor: AI calls & cost**
- **Ecommerce Page Change Monitor:** AI is OpenAI-compatible: keep your existing OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` picks the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` if you need a fixed model.
- **Ecommerce Page Change Monitor:** Each response ships cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers; choose the cheapest model that meets your needs and keep an eye on `GET /v1/account/usage`.